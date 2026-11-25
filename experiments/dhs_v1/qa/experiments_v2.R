#!/usr/bin/env Rscript
# =====================================================================================================
# Atlas eight DHS experiments -- QA-hardened v2 (methods/QA team, 2026-11-25)
#
# v1 (original starter) is preserved verbatim at qa/original/experiments.R
# (sha256 6705c9ec3a4b8cee2bb8b1c34d36a0dfb58e1dae0e26059d4545f96a3f3da817).  Every change below is
# either a documented defect fix from qa/QA_REPORT.md or additive reporting; the E1-E8 domain
# definitions (ages, sex, record type, cohorts) are UNCHANGED from the README/v1.
#
# Usage:
#   Rscript experiments.R normalized.csv output_dir \
#       [--lonely-psu=fail|adjust|certainty|remove] [--min-cell=25] \
#       [--benchmarks=benchmarks.csv] [--meta=metadata.csv]
#
# Defaults preserve v1 behaviour where possible (2 positional args required; lonely PSU policy
# 'fail' so a singleton stratum is never silently adjusted).  All exploratory, descriptive,
# within-wave domain means -- NOT causal estimates (see README and the manifest note).
# =====================================================================================================

args_all <- commandArgs(trailingOnly=TRUE)
if (length(args_all) < 2) stop('Usage: Rscript experiments.R normalized.csv output_dir [--lonely-psu=fail|adjust|certainty|remove] [--min-cell=25] [--benchmarks=benchmarks.csv] [--meta=metadata.csv]')
input_csv <- args_all[1]
out_dir   <- args_all[2]
flush_flags <- args_all[-(1:2)]

get_flag <- function(flags, name, default=NULL) {
  hit <- grep(paste0('^--', name, '='), flags, value=TRUE)
  if (!length(hit)) return(default)
  if (length(hit) > 1) stop('Duplicate flag --', name)
  sub(paste0('^--', name, '='), '', hit[1])
}
lonely_policy <- match.arg(get_flag(flush_flags, 'lonely-psu', 'fail'),
                           c('fail', 'adjust', 'certainty', 'remove'))
min_cell <- suppressWarnings(as.integer(get_flag(flush_flags, 'min-cell', '30')))
if (is.na(min_cell) || min_cell < 1) stop('--min-cell must be a positive integer')
rse_max <- suppressWarnings(as.numeric(get_flag(flush_flags, 'rse-max', '0.30')))
if (!is.finite(rse_max) || rse_max <= 0) stop('--rse-max must be a positive number')
benchmarks_path <- get_flag(flush_flags, 'benchmarks', NULL)
meta_path <- get_flag(flush_flags, 'meta', NULL)
e6_def <- get_flag(flush_flags, 'e6', 'person')   # lead-approved sign-off basis; 'woman' = v1 spec (unrunnable on DHS IR)
if (!e6_def %in% c('woman','person')) stop('--e6 must be woman (v1 spec, unrunnable on DHS IR) or person (PR females 20-24; deviation needing sign-off)')
bad_flags <- flush_flags[!grepl('^--(lonely-psu|min-cell|rse-max|benchmarks|meta|e6)=', flush_flags)]
if (length(bad_flags)) stop('Unknown flag(s): ', paste(bad_flags, collapse=', '))

if (!requireNamespace('survey', quietly=TRUE)) stop('Install R package survey')
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)

sha256_of <- function(path) {
  out <- tryCatch(system2('sha256sum', path, stdout=TRUE, stderr=FALSE), error=function(e) character(0))
  if (length(out) && nzchar(out[1])) return(sub(' .*$', '', out[1]))
  paste0('md5:', as.character(tools::md5sum(path)))
}
note <- function(...) cat(..., '\n', sep='')          # progress lines to stdout
warns <- character(0); add_warn <- function(...) { warns <<- c(warns, paste0(...)); note('WARNING: ', ...) }

# --------------------------------------------------------------------------------- schema + validation
d <- read.csv(input_csv, stringsAsFactors=FALSE, na.strings=c('', 'NA', 'NaN', '.'))
required <- c('country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth',
              'attendance','school_years','children_ever_born','age_first_birth','currently_in_school',
              'age_first_union','household_size')
missing_cols <- setdiff(required, names(d))
if (length(missing_cols)) stop('Missing schema columns: ', paste(missing_cols, collapse=', '))

num_cols <- c('weight','age','sex','urban','wealth','attendance','school_years',
              'children_ever_born','age_first_birth','currently_in_school','age_first_union','household_size')
for (cc in num_cols) d[[cc]] <- suppressWarnings(as.numeric(d[[cc]]))
d$country <- as.character(d$country); d$record_type <- as.character(d$record_type)
d$wave <- as.character(d$wave)          # DHS wave labels are strings ("2021-22"), not numbers
d$stratum <- as.character(d$stratum); d$psu <- as.character(d$psu)

errs <- character(0); add_err <- function(...) errs <<- c(errs, paste0(...))
key_bad <- is.na(d$country) | !nzchar(trimws(d$country)) | is.na(d$wave) | !nzchar(trimws(d$wave)) |
           is.na(d$record_type) | !nzchar(trimws(d$record_type))
if (any(key_bad)) add_err(sum(key_bad), ' row(s) with missing country/wave/record_type')
if (any(!d$record_type %in% c('person','woman'))) add_err('Invalid record_type: ', paste(unique(d$record_type[!d$record_type %in% c('person','woman')]), collapse=', '))
if (any(!is.finite(d$weight))) add_err(sum(!is.finite(d$weight)), ' row(s) with non-finite weight (NA/Inf/NaN)')
if (any(is.finite(d$weight) & d$weight <= 0)) add_err(sum(is.finite(d$weight) & d$weight <= 0), ' row(s) with weight <= 0')
if (any(is.na(d$stratum) | !nzchar(trimws(d$stratum)))) add_err(sum(is.na(d$stratum) | !nzchar(trimws(d$stratum))), ' row(s) with missing stratum')
if (any(is.na(d$psu) | !nzchar(trimws(d$psu)))) add_err(sum(is.na(d$psu) | !nzchar(trimws(d$psu))), ' row(s) with missing PSU')

intlike <- function(x, lo, hi) is.na(x) | (is.finite(x) & x == round(x) & x >= lo & x <= hi)
if (any(!intlike(d$wealth, 1, 5))) add_err('Wealth must be integer 1..5 or NA: offending values ', paste(head(unique(d$wealth[!intlike(d$wealth,1,5)]), 10), collapse=', '))
for (bn in c('attendance','currently_in_school','urban')) {
  if (any(!intlike(d[[bn]], 0, 1))) add_err(bn, ' must be 0/1 or NA: offending values ', paste(head(unique(d[[bn]][!intlike(d[[bn]],0,1)]), 10), collapse=', '))
}
sex_bad <- !(is.na(d$sex) | d$sex %in% c(1, 2))
if (any(sex_bad)) add_err('sex must be 1 (male) or 2 (female) or NA: offending values ', paste(head(unique(d$sex[sex_bad]), 10), collapse=', '))
if (any(is.na(d$sex) & d$record_type == 'person')) add_warn(sum(is.na(d$sex) & d$record_type == 'person'), ' person row(s) with missing sex excluded from sex-domain analyses (E3/E6-person); recorded in missingness')
if (any(!intlike(d$age, 0, 99))) add_err('age must be integer 0..99 or NA: offending values ', paste(head(unique(d$age[!intlike(d$age,0,99)]), 10), collapse=', '))
if (any(d$record_type == 'woman' & is.finite(d$age) & (d$age < 15 | d$age > 49)))
  add_warn(sum(d$record_type == 'woman' & is.finite(d$age) & (d$age < 15 | d$age > 49)), ' woman row(s) outside the DHS 15-49 women frame (kept; check adapter)')
dk_sy <- !is.na(d$school_years) & d$school_years %in% c(95, 96, 97, 98, 99)
dk_ceb <- !is.na(d$children_ever_born) & d$children_ever_born %in% c(95, 96, 97, 98, 99)
if (any(dk_sy)) { add_warn(sum(dk_sy), ' school_years DHS DK/inconsistent code(s) 95-99 mapped to NA in-script (adapter should recode; recorded here for audit)'); d$school_years[dk_sy] <- NA }
if (any(dk_ceb)) { add_warn(sum(dk_ceb), ' children_ever_born DHS DK/inconsistent code(s) 95-99 mapped to NA in-script (adapter should recode)'); d$children_ever_born[dk_ceb] <- NA }
if (any(!intlike(d$school_years, 0, 25))) add_err('school_years must be integer 0..25 or NA: offending values ', paste(head(unique(d$school_years[!intlike(d$school_years,0,25)]), 10), collapse=', '))
if (any(!intlike(d$children_ever_born, 0, 25))) add_err('children_ever_born must be integer 0..25 or NA: offending values ', paste(head(unique(d$children_ever_born[!intlike(d$children_ever_born,0,25)]), 10), collapse=', '))
if (any(!intlike(d$household_size, 1, 50))) add_err('household_size must be integer 1..50 or NA: offending values ', paste(head(unique(d$household_size[!intlike(d$household_size,1,50)]), 10), collapse=', '))
# 99 is the documented "verified never" sentinel for first birth/union; NA is unknown; 97/98 etc are not allowed here.
first_ok <- function(x) is.na(x) | x == 99 | (is.finite(x) & x == round(x) & x >= 10 & x <= 49)
for (fn in c('age_first_birth','age_first_union')) {
  v <- d[[fn]]
  bad_lo <- !is.na(v) & v > 0 & v < 10 & v != 99
  if (any(bad_lo)) { add_warn(sum(bad_lo), ' ', fn, ' value(s) <10 (non-99) are implausible ages, mapped to NA in-script (misreport/DK); adapter should recode'); v[bad_lo] <- NA }
  bad_hi <- !is.na(v) & v > 49 & v != 99
  if (any(bad_hi)) { add_warn(sum(bad_hi), ' ', fn, ' value(s) >49 (not 99=never) mapped to NA in-script (DHS DK codes; adapter should recode)'); v[bad_hi] <- NA }
  if (any(!first_ok(v))) add_err(fn, ' must be NA (unknown), 99 (verified never) or an integer age 10..49; offending values ', paste(head(unique(v[!first_ok(v)]), 10), collapse=', '))
  d[[fn]] <- v
}
# PSU labels must identify one cluster within one stratum of a country/wave/record-type design.
for (grp in split(d, interaction(d$country, d$wave, d$record_type, drop=TRUE, lex.order=TRUE))) {
  if (!nrow(grp)) next
  mm <- tapply(grp$stratum, grp$psu, function(s) length(unique(s)))
  bad <- names(mm)[mm > 1]
  if (length(bad)) add_err('PSU label(s) appearing in more than one stratum in ', grp$country[1], ' wave ', grp$wave[1], ' ', grp$record_type[1], ': ', paste(head(bad, 10), collapse=', '))
}
# Both record-type weights: if the adapter supplies weight_variable, person rows and woman rows must use
# DIFFERENT documented weight variables (README: appropriate person vs individual-woman weight per row).
weight_provenance <- 'single weight column (weight) -- adapter must certify record-appropriate weight; NOT machine-verified'
if ('weight_variable' %in% names(d)) {
  wv <- as.character(d$weight_variable)
  pv <- unique(wv[d$record_type == 'person']); vv <- unique(wv[d$record_type == 'woman'])
  if (length(pv) > 1 || length(vv) > 1) add_err('weight_variable must be a single label per record_type (person: ', paste(pv, collapse=','), '; woman: ', paste(vv, collapse=','), ')')
  else if (length(pv) && length(vv) && pv == vv) add_err('weight_variable uses the same weight for person and woman rows (', pv, '); README requires the record-appropriate weight for each row')
  else if (length(pv) && length(vv)) weight_provenance <- paste0('person weight = ', pv, '; woman weight = ', vv, ' (validated distinct labels)')
} else {
  add_warn('no weight_variable column in the data file: record-appropriate weight use is NOT machine-verifiable; provenance must come from --meta (README requires it)')
}
# Optional adapter metadata file: every run must record country/wave/release/weight/strata/psu/missing
# codes/access approval (README).  Key,value CSV.
meta_info <- NULL
if (!is.null(meta_path)) {
  if (!file.exists(meta_path)) add_err('metadata file not found: ', meta_path)
  else {
    md <- read.csv(meta_path, stringsAsFactors=FALSE, na.strings=c('', 'NA'))
    if (!all(c('key','value') %in% names(md))) add_err('metadata file must have columns key,value')
    else {
      need_meta <- c('country','wave','release','record_type','weight_variable','strata_variable','psu_variable','missing_codes','approved_access')
      miss_meta <- setdiff(need_meta, md$key)
      if (length(miss_meta)) add_err('metadata file missing required key(s): ', paste(miss_meta, collapse=', '))
      else meta_info <- paste0(md$key, '=', md$value, collapse='; ')
    }
  }
} else add_warn('no --meta metadata file supplied; country/wave/release/weight/strata/PSU/missing-code/access provenance is NOT fully recorded (README requires it)')
if (length(errs)) stop('Schema/validation failed (', length(errs), ' issue(s)):\n  - ', paste(errs, collapse='\n  - '))

# --------------------------------------------------------------------------------- experiment specs (README)
specs <- list(
 E1=list(type='person',ages=c(14,17),out='attendance',group='wealth',desc='Adolescent attendance by wealth'),
 E2=list(type='person',ages=c(14,17),out='attendance',group='urban',desc='Adolescent attendance by residence'),
 E3=list(type='person',ages=c(14,17),out='attendance',group='sex',desc='Adolescent attendance by sex'),
 E4=list(type='woman',ages=c(40,49),out='children_ever_born',group='education',desc='Completed-cohort children ever born by schooling'),
 E5=list(type='woman',ages=c(25,34),out='early_birth',group='education',desc='Birth before age 20 by schooling'),
 E6=list(type='woman',ages=c(20,24),out='currently_in_school',group='urban',desc='School participation among young women by residence'),
 E7=list(type='woman',ages=c(25,34),out='early_union',group='education',desc='Union before age 20 by schooling'),
 E8=list(type='woman',ages=c(40,49),out='household_size',group='education',desc='Current household size among older women by schooling'))
# E6 definition: v1/README says woman record + currently_in_school, but DHS IR/WI has no current-attendance
# item (verified on the delivered data: 0 non-missing in every woman file).  --e6=person implements the
# explicitly-labelled PR-based alternative (females 20-24, hv121, person weight); it is NOT the v1 spec
# and requires sign-off.
if (e6_def == 'person') {
  specs$E6$type <- 'person'; specs$E6$sex <- 2
  specs$E6$desc <- paste0(specs$E6$desc, ' [E6-PERSON deviation: PR females 20-24, person weight; requires sign-off]')
}

d$education <- ifelse(is.na(d$school_years), NA, ifelse(d$school_years < 6, '0-5', ifelse(d$school_years < 12, '6-11', '12+')))
# age_first_birth/union: NA = unknown (stays unknown); 99 = verified never -> not early (0), never coerced to NA.
d$early_birth <- ifelse(is.na(d$age_first_birth), NA_real_, as.numeric(d$age_first_birth < 20))
d$early_union <- ifelse(is.na(d$age_first_union), NA_real_, as.numeric(d$age_first_union < 20))

# --------------------------------------------------------------------------------- diagnostics helpers
design_rows <- function(z) {
  tab <- table(z$stratum, z$psu)
  psu_per_stratum <- rowSums(tab > 0)
  list(n_rows=nrow(z), n_strata=length(unique(z$stratum)), n_psu=length(unique(z$psu)),
       n_singleton_strata=sum(psu_per_stratum == 1),
       singleton_strata=paste(names(psu_per_stratum)[psu_per_stratum == 1], collapse=';'))
}
out_rows <- list(); status_rows <- list(); miss_rows <- list()
k <- 0; s <- 0

on.exit(options(survey.lonely.psu=NULL), add=TRUE)
options(survey.lonely.psu=lonely_policy)

# Pre-compute the base-design singleton diagnostics once per country-wave-record type: with
# --lonely-psu=fail (default) an analysis of a design with a genuine singleton stratum is refused
# with an actionable message; with adjust/certainty/remove the survey package option is applied and
# the decision is recorded in the manifest.  Domain estimation below NEVER subsets the design, so
# domain-induced singleton strata cannot arise (defect fix D1).
base_diag <- list()
for (cn in unique(d$country)) for (w in unique(d$wave[d$country == cn])) for (rt in c('person','woman')) {
  zz <- d[d$country == cn & d$wave == w & d$record_type == rt, , drop=FALSE]
  if (nrow(zz)) base_diag[[paste(cn, w, rt, sep='|')]] <- design_rows(zz)
}

for (key in names(specs)) for (cn in unique(d$country)) for (w in unique(d$wave[d$country == cn])) {
  sp <- specs[[key]]
  z <- d[d$country == cn & d$wave == w & d$record_type == sp$type, , drop=FALSE]
  if (!is.null(sp$sex)) z <- z[!is.na(z$sex) & z$sex == sp$sex, , drop=FALSE]
  s <- s + 1
  dkey <- paste(cn, w, sp$type, sep='|')
  if (!nrow(z)) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=0,
                                   status='no rows for this record_type', stringsAsFactors=FALSE)
    next
  }
  diag <- base_diag[[dkey]]
  in_dom <- !is.na(z$age) & z$age >= sp$ages[1] & z$age <= sp$ages[2]
  if (!sum(in_dom)) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=0,
                                   status='no eligible rows in domain', stringsAsFactors=FALSE)
    next
  }
  if (diag$n_singleton_strata > 0 && lonely_policy == 'fail') {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=0,
      status=paste0('lonely PSU: ', diag$n_singleton_strata, ' stratum/strata with a single PSU in the base ',
                    sp$type, ' design (', substr(diag$singleton_strata, 1, 160),
                    '); design review required, no estimate produced. Use --lonely-psu=adjust|certainty only after documenting why the singleton is a genuine design feature.'),
      stringsAsFactors=FALSE)
    next
  }
  # domain indicators on the FULL sample; the design keeps every PSU (domain estimation)
  outcome_raw <- if (sp$out == 'early_birth') z$early_birth
                 else if (sp$out == 'early_union') z$early_union
                 else z[[sp$out]]
  grp_raw <- if (sp$group == 'education') z$education else z[[sp$group]]
  idx <- in_dom & !is.na(outcome_raw) & !is.na(grp_raw)
  n_complete <- sum(idx)
  miss_out <- sum(in_dom & is.na(outcome_raw))
  miss_grp <- sum(in_dom & is.na(grp_raw))
  never_n <- if (sp$out == 'early_birth') sum(in_dom & !is.na(z$age_first_birth) & z$age_first_birth == 99) else
             if (sp$out == 'early_union') sum(in_dom & !is.na(z$age_first_union) & z$age_first_union == 99) else 0L
  unknown_n <- if (sp$out == 'early_birth') sum(in_dom & is.na(z$age_first_birth)) else
              if (sp$out == 'early_union') sum(in_dom & is.na(z$age_first_union)) else 0L
  miss_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, record_type=sp$type,
    n_type_rows=nrow(z), n_age_eligible=sum(in_dom), n_complete=n_complete,
    n_outcome_missing=miss_out, n_group_missing=miss_grp, n_verified_never=never_n,
    n_unknown_birth_union=unknown_n, stringsAsFactors=FALSE)
  if (n_complete < 50) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
      status='insufficient complete cases (<50 complete cases in the domain)', stringsAsFactors=FALSE)
    next
  }
  z$.dom <- idx
  z$.out <- ifelse(idx, outcome_raw, NA_real_)
  grp_chr <- ifelse(idx, as.character(grp_raw), NA_character_)
  if (length(unique(grp_chr[!is.na(grp_chr)])) < 2) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
      status='fewer than 2 non-empty groups in the domain', stringsAsFactors=FALSE)
    next
  }
  z$.grp <- factor(grp_chr, exclude=NA)
  z$stratum <- as.factor(z$stratum); z$psu <- as.factor(z$psu)
  deg <- tryCatch(survey::svydesign(ids=~psu, strata=~stratum, weights=~weight, data=z, nest=TRUE),
                  error=function(e) e)
  if (inherits(deg, 'error')) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
      status=paste('design error:', conditionMessage(deg)), stringsAsFactors=FALSE)
    next
  }
  # Domain mean + design-based SE per group: svymean on the FULL design with the outcome set to NA
  # outside the group-domain (design retains every PSU; lead Monte-Carlo: NA-indicator method
  # ~ empirical sd, subset()/svyby(full) understate by 27-40%).  Loop over group levels.
  grp_levels <- sort(unique(as.character(z$.grp[!is.na(z$.grp)])))
  ans <- list()
  for (gl in grp_levels) {
    deg$variables$.y <- ifelse(!is.na(deg$variables$.grp) & as.character(deg$variables$.grp) == gl,
                              deg$variables$.out, NA_real_)
    sm <- tryCatch(survey::svymean(~.y, deg, na.rm=TRUE), error=function(e) e)
    if (inherits(sm, 'error')) { ans <- sm; break }
    vv <- tryCatch(stats::vcov(sm), error=function(e) matrix(NA_real_))
    ans[[gl]] <- c(g=gl, est=as.numeric(sm)[1], se=sqrt(max(diag(vv)[1], 0)))
  }
  if (inherits(ans, 'error')) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
      status=paste('estimation error:', conditionMessage(ans)), stringsAsFactors=FALSE)
    next
  }
  if (!length(ans)) {
    status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
      status='no estimable groups after missingness', stringsAsFactors=FALSE)
    next
  }
  psu_dom <- tapply(z$.dom, z$psu, sum); strata_dom <- tapply(z$.dom, z$stratum, sum)
  design_df <- tryCatch(survey::degf(deg), error=function(e) NA_integer_)
  for (j in seq_along(ans)) {
    gname <- as.character(ans[[j]]['g'])
    sel <- idx & as.character(grp_raw) == gname
    n_unw <- sum(sel); estv <- suppressWarnings(as.numeric(ans[[j]]['est']))
    se <- suppressWarnings(as.numeric(ans[[j]]['se']))
    n_w <- if (n_unw) sum(z$weight[sel]) else NA_real_
    rse <- if (is.finite(estv) && estv != 0 && is.finite(se)) se / abs(estv) else NA_real_
    flags <- character(0); suppressed <- FALSE
    if (n_unw < min_cell) { suppressed <- TRUE; flags <- c(flags, paste0('SUPPRESSED: unweighted n<', min_cell, ' (disclosure/unreliability)')) }
    if (sum(psu_dom > 0) < 2) { suppressed <- TRUE; flags <- c(flags, 'SUPPRESSED: fewer than 2 PSUs contribute to the domain') }
    if (!is.finite(design_df) || design_df < 1) { suppressed <- TRUE; flags <- c(flags, 'SUPPRESSED: design df < 1') }
    if (n_unw >= min_cell && n_unw < 50) flags <- c(flags, 'caution: unweighted n<50')
    if (is.finite(rse) && rse > rse_max) { suppressed <- TRUE; flags <- c(flags, paste0('SUPPRESSED: RSE>', round(100*rse_max), '%')) }
    else if (is.finite(rse) && rse > 0.75 * rse_max) flags <- c(flags, paste0('caution: RSE>', round(75*rse_max), '%'))
    if (!is.finite(se)) { suppressed <- TRUE; flags <- c(flags, 'SUPPRESSED: non-finite SE') }
    if (is.finite(design_df) && design_df < 30) flags <- c(flags, 'caution: design df<30 (normal CI approximate; consider t)')
    k <- k + 1
    out_rows[[k]] <- data.frame(
      experiment=key, country=cn, wave=w, group=gname,
      estimate=if (suppressed) NA_real_ else estv, se=if (suppressed) NA_real_ else se,
      lo=if (suppressed) NA_real_ else estv - 1.96 * se,
      hi=if (suppressed) NA_real_ else estv + 1.96 * se,
      complete_n=n_unw, description=sp$desc,
      n_unweighted=n_unw, n_weighted=n_w,
      n_psu_domain=sum(psu_dom > 0), n_strata_domain=sum(strata_dom > 0),
      rse=rse, suppressed=suppressed, flags=paste(flags, collapse='; '),
      design_df=design_df, ci_method='normal(1.96); design df reported; t-approximation recommended if df<30',
      weight_var='weight', denominator_def=paste0(sp$type, ' records, ages ', sp$ages[1], '-', sp$ages[2],
        ', non-missing ', sp$out, ' and ', sp$group),
      missing_share=if (sum(in_dom) > 0) (miss_out + miss_grp) / sum(in_dom) else NA_real_,
      externally_benchmarked=FALSE, benchmark_id=NA_character_,
      not_externally_benchmarked=TRUE,
      stringsAsFactors=FALSE)
  }
  status_rows[[s]] <- data.frame(experiment=key, country=cn, wave=w, complete_n=n_complete,
    status='ok', stringsAsFactors=FALSE)
}

estimates <- if (length(out_rows)) do.call(rbind, out_rows) else data.frame(
  experiment=character(0), country=character(0), wave=numeric(0), group=character(0),
  estimate=numeric(0), se=numeric(0), lo=numeric(0), hi=numeric(0), complete_n=integer(0),
  description=character(0), n_unweighted=integer(0), n_weighted=numeric(0), n_psu_domain=integer(0),
  n_strata_domain=integer(0), rse=numeric(0), suppressed=logical(0), flags=character(0),
  design_df=integer(0), ci_method=character(0), weight_var=character(0), denominator_def=character(0),
  missing_share=numeric(0), externally_benchmarked=logical(0), benchmark_id=character(0),
  not_externally_benchmarked=logical(0), stringsAsFactors=FALSE)
status <- if (length(status_rows)) do.call(rbind, status_rows) else data.frame()
missingness <- if (length(miss_rows)) do.call(rbind, miss_rows) else data.frame()

# --------------------------------------------------------------------------------- multiplicity (exploratory)
multiplicity_note <- 'EXPLORATORY descriptive study: no confirmatory inference; no causal claim. BH q-values (if shown) are for transparency across all estimates in this run, not a discovery claim.'
if (nrow(estimates)) {
  p <- 2 * pnorm(-abs(estimates$estimate / estimates$se))
  p[!is.finite(p)] <- NA
  estimates$p_value_normal <- p
  q <- rep(NA_real_, length(p))
  ok <- !is.na(p)
  if (sum(ok)) q[ok] <- p.adjust(p[ok], method='BH')
  estimates$q_value_bh <- q
  estimates$exploratory <- TRUE
  estimates$family <- estimates$experiment
} 

# --------------------------------------------------------------------------------- benchmarks (optional)
benchmark_status <- 'NOT_RUN: no benchmarks file supplied (real DHS microdata/benchmarks are BLOCKED in this worktree)'
bench_rows <- data.frame(benchmark_id=character(0), experiment=character(0), country=character(0),
                         wave=character(0), group=character(0), estimate=numeric(0), benchmark=numeric(0),
                         diff=numeric(0), tolerance=numeric(0), check=character(0), direction=character(0),
                         source=character(0), citation=character(0), definition_match=character(0),
                         stringsAsFactors=FALSE)
if (!is.null(benchmarks_path)) {
  if (!file.exists(benchmarks_path)) stop('Benchmarks file not found: ', benchmarks_path)
  bm <- read.csv(benchmarks_path, stringsAsFactors=FALSE, na.strings=c('', 'NA'))
  need_bm <- c('experiment','country','wave','group','benchmark','source','citation')
  miss_bm <- setdiff(need_bm, names(bm)); if (length(miss_bm)) stop('Benchmarks file missing columns: ', paste(miss_bm, collapse=', '))
  if (!'tolerance' %in% names(bm)) bm$tolerance <- NA_real_
  for (i in seq_len(nrow(bm))) {
    sel <- if (nrow(estimates)) which(estimates$experiment == bm$experiment[i] & estimates$country == bm$country[i] &
             as.character(estimates$wave) == as.character(bm$wave[i]) & estimates$group == as.character(bm$group[i])) else integer(0)
    tol <- ifelse(is.na(bm$tolerance[i]), 0.02, bm$tolerance[i])
    if (!length(sel)) {
      bench_rows <- rbind(bench_rows, data.frame(
        benchmark_id=if ('benchmark_id' %in% names(bm)) as.character(bm$benchmark_id[i]) else paste0('B', i),
        experiment=bm$experiment[i], country=bm$country[i], wave=bm$wave[i], group=bm$group[i],
        estimate=NA_real_, benchmark=bm$benchmark[i], diff=NA_real_, tolerance=tol,
        check='NOT_FOUND_IN_OUTPUT', direction=NA_character_,
        source=bm$source[i], citation=bm$citation[i],
        definition_match=if ('definition_match' %in% names(bm)) as.character(bm$definition_match[i]) else NA_character_,
        stringsAsFactors=FALSE))
    } else for (s2 in sel) {
      est <- estimates$estimate[s2]; diff <- est - bm$benchmark[i]
      check <- if (is.na(est)) 'ESTIMATE_SUPPRESSED' else if (abs(diff) <= tol) 'MATCH' else 'MISMATCH'
      bench_rows <- rbind(bench_rows, data.frame(
        benchmark_id=if ('benchmark_id' %in% names(bm)) as.character(bm$benchmark_id[i]) else paste0('B', i),
        experiment=bm$experiment[i], country=bm$country[i], wave=bm$wave[i], group=bm$group[i],
        estimate=est, benchmark=bm$benchmark[i], diff=diff, tolerance=tol, check=check,
        direction=if (is.finite(diff)) if (diff > 0) 'ours_higher' else if (diff < 0) 'ours_lower' else 'equal' else NA_character_,
        source=bm$source[i], citation=bm$citation[i],
        definition_match=if ('definition_match' %in% names(bm)) as.character(bm$definition_match[i]) else NA_character_,
        stringsAsFactors=FALSE))
    }
  }
  benchmark_status <- paste0('CHECKED: ', nrow(bm), ' benchmark row(s); ',
                             sum(bench_rows$check == 'MATCH'), ' match, ',
                             sum(bench_rows$check == 'MISMATCH'), ' mismatch, ',
                             sum(bench_rows$check %in% c('NOT_FOUND_IN_OUTPUT','ESTIMATE_SUPPRESSED')), ' unavailable')
  if (any(bench_rows$check == 'MISMATCH')) add_warn(benchmark_status)
}

# cells covered by a supplied registry benchmark are marked externally benchmarked; all others are
# explicitly BENCHMARK-PENDING (lead rule: no validation claim without a matching published table)
if (nrow(estimates) && exists('bench_rows') && nrow(bench_rows)) {
  for (i in seq_len(nrow(estimates))) {
    hit <- which(bench_rows$experiment == estimates$experiment[i] & bench_rows$country == estimates$country[i] &
                 as.character(bench_rows$wave) == as.character(estimates$wave[i]) &
                 as.character(bench_rows$group) == as.character(estimates$group[i]) &
                 bench_rows$check %in% c('MATCH', 'MISMATCH'))
    if (length(hit)) {
      estimates$externally_benchmarked[i] <- TRUE
      estimates$benchmark_id[i] <- as.character(bench_rows$benchmark_id[hit[1]])
      estimates$not_externally_benchmarked[i] <- FALSE
    }
  }
}

write.csv(estimates, file.path(out_dir, 'estimates.csv'), row.names=FALSE)
write.csv(status, file.path(out_dir, 'status.csv'), row.names=FALSE)
write.csv(missingness, file.path(out_dir, 'missingness.csv'), row.names=FALSE)
if (!is.null(benchmarks_path)) write.csv(bench_rows, file.path(out_dir, 'benchmark_check.csv'), row.names=FALSE)
writeLines(capture.output(sessionInfo()), file.path(out_dir, 'session_info.txt'))

esc <- function(x) gsub('"', "'", gsub('\\\\', '/', as.character(x)))
json_lines <- function(pairs) paste0('{', paste(sprintf('"%s": "%s"', names(pairs), vapply(pairs, esc, '')), collapse=', '), '}')
manifest_pairs <- c(
  programme='Atlas eight DHS experiments (DHS methods/QA team)',
  script='experiments.R v2 QA-hardened',
  script_sha256=sha256_of(sub('^--file=', '', grep('^--file=', commandArgs(FALSE), value=TRUE)[1])),
  input_file=normalizePath(input_csv, mustWork=FALSE),
  input_sha256=sha256_of(input_csv),
  r_version=paste(R.version$major, R.version$minor, sep='.'),
  survey_version=as.character(utils::packageVersion('survey')),
  generated_utc=format(Sys.time(), '%Y-%m-%dT%H:%M:%SZ', tz='UTC'),
  n_rows=as.character(nrow(d)),
  countries=paste(sort(unique(d$country)), collapse=';'),
  waves=paste(sort(unique(d$wave)), collapse=';'),
  record_types=paste(sort(unique(d$record_type)), collapse=';'),
  strata_variable='stratum', psu_variable='psu', weight_variable_used='weight',
  weight_provenance=weight_provenance,
  adapter_metadata=if (is.null(meta_info)) 'NOT SUPPLIED' else meta_info,
  lonely_psu_policy=lonely_policy,
  min_cell_rule=paste0('suppress unweighted n<', min_cell, '; caution n<50; suppress RSE>', round(100*rse_max), '%'),
  missing_codes='NA/blank = unknown/missing; age_first_birth/age_first_union 99 = verified never; adapter must recode DHS special codes to NA',
  sample_restrictions='within country-wave-record_type; E1-E3 persons aged 14-17; E4 women 40-49; E5 women 25-34; E6 women 20-24; E7 women 25-34; E8 women 40-49',
  analysis_type='descriptive within-wave domain means with design-based SEs',
  e6_definition=paste0(e6_def, if (e6_def == 'person') ' (DEVIATION: PR females 20-24 with person weight; needs lead sign-off; NOT the v1 woman-record E6)' else ' (v1 spec; unrunnable on DHS IR)'),
  interpretation='NOT causal: schooling may postdate early birth/union; E8 is current household size, NOT kin support; wealth is a relative index, NOT income; cross-sectional comparisons cannot establish timing/mechanism',
  multiplicity=multiplicity_note,
  benchmark_status=benchmark_status,
  n_estimates=as.character(nrow(estimates)),
  n_externally_benchmarked=as.character(if (nrow(estimates)) sum(estimates$externally_benchmarked) else 0),
  n_benchmark_pending=as.character(if (nrow(estimates)) sum(estimates$not_externally_benchmarked) else 0),
  warnings=paste(warns, collapse=' | '),
  estimates_sha256=sha256_of(file.path(out_dir, 'estimates.csv')),
  status_sha256=sha256_of(file.path(out_dir, 'status.csv')))
writeLines(json_lines(manifest_pairs), file.path(out_dir, 'manifest.json'))
note('wrote ', nrow(estimates), ' estimates, ', nrow(status), ' status rows, ', nrow(missingness), ' missingness rows to ', out_dir)
note('benchmark status: ', benchmark_status)
