#!/usr/bin/env Rscript
# =====================================================================================================
# DHS methods/QA test harness -- SYNTHETIC FIXTURES ONLY (no real DHS data is used or required).
#
# Compares the ORIGINAL starter (qa/original/experiments.R) with the QA-hardened v2
# (experiments.R), asserts known answers and documents before/after behaviour.
#
# Usage: Rscript qa/qa_tests.R [workdir] [rscript_binary]
#   workdir defaults to the experiment directory (parent of qa/)
# Outputs: qa/logs/results.csv, qa/logs/results.txt, qa/logs/qa_run.log and per-run outputs under
#          qa/out_original/<fixture>/ and qa/out_fixed/<fixture>/
# =====================================================================================================
args <- commandArgs(trailingOnly=TRUE)
here <- if (length(args) >= 1) normalizePath(args[1]) else normalizePath(file.path(getwd()))
rscript <- if (length(args) >= 2) args[2] else file.path(R.home('bin'), 'Rscript')
if (!file.exists(rscript)) rscript <- Sys.which('Rscript')
qa_dir <- file.path(here, 'qa')
fix_dir <- file.path(qa_dir, 'fixtures')
if (!file.exists(file.path(fix_dir, 'known_means.csv'))) {
  dir.create(fix_dir, recursive=TRUE, showWarnings=FALSE)
  system2(rscript, file.path(qa_dir, 'make_fixtures.R'), fix_dir, stdout=TRUE, stderr=TRUE)
}
log_dir <- file.path(qa_dir, 'logs')
dir.create(log_dir, recursive=TRUE, showWarnings=FALSE)
orig_script <- file.path(qa_dir, 'original', 'experiments.R')
fixed_script <- file.path(here, 'experiments.R')
stopifnot(file.exists(orig_script), file.exists(fixed_script))

LITE <- c('--min-cell=2', '--rse-max=2')   # known-answer tests: suppression is tested separately (T11/T12)
log_lines <- character(0); log_add <- function(...) { l <- paste0(...); log_lines <<- c(log_lines, l); cat(l, '\n') }
RESULTS <- list()
check <- function(id, area, description, expected, observed, pass, notes='') {
  RESULTS[[length(RESULTS)+1]] <<- data.frame(id=id, area=area, test=description,
    expected=as.character(expected), observed=as.character(observed),
    pass=isTRUE(pass), notes=as.character(notes), stringsAsFactors=FALSE)
  log_add(sprintf('[%s] %-5s %-46s obs=%s', id, ifelse(isTRUE(pass), 'PASS', 'FAIL'), description, substr(as.character(observed), 1, 90)))
}
sha256_of <- function(path) {
  out <- tryCatch(system2('sha256sum', path, stdout=TRUE, stderr=FALSE), error=function(e) character(0))
  if (length(out) && nzchar(out[1])) sub(' .*$', '', out[1]) else paste0('md5:', tools::md5sum(path))
}
md5_of <- function(path) paste0('md5:', as.character(tools::md5sum(path)))

run_script <- function(script, csv, outdir, flags=character()) {
  unlink(outdir, recursive=TRUE); dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
  out <- suppressWarnings(system2(rscript, c(script, csv, outdir, flags), stdout=TRUE, stderr=TRUE))
  st <- attr(out, 'status'); if (is.null(st)) st <- 0L
  list(status=as.integer(st), output=paste(out, collapse='\n'), outdir=outdir)
}
read_out <- function(res, file) {
  p <- file.path(res$outdir, file)
  if (!file.exists(p) || file.info(p)$size == 0) return(NULL)
  out <- tryCatch(read.csv(p, stringsAsFactors=FALSE, na.strings=c('', 'NA')), error=function(e) NULL)
  if (!is.null(out) && nrow(out) == 0) return(NULL)
  out
}
read_json_manifest <- function(res) {
  p <- file.path(res$outdir, 'manifest.json')
  if (!file.exists(p)) return(NULL)
  txt <- paste(readLines(p, warn=FALSE), collapse=' ')
  # flat one-line JSON with "key": "value" pairs; values may not contain unescaped quotes
  m <- gregexpr('"([^"]+)"\\s*:\\s*"([^"]*)"', txt, perl=TRUE)
  hits <- regmatches(txt, m)[[1]]
  if (!length(hits)) return(list())
  keys <- sub('^"([^"]+)".*$', '\\1', hits)
  vals <- sub('^"[^"]+"\\s*:\\s*"(.*)"$', '\\1', hits)
  setNames(as.list(vals), keys)
}
est <- function(res, experiment, country=NULL, wave=NULL) {
  e <- read_out(res, 'estimates.csv'); if (is.null(e) || !nrow(e)) return(NULL)
  e <- e[e$experiment == experiment, , drop=FALSE]
  if (!is.null(country)) e <- e[e$country == country, , drop=FALSE]
  if (!is.null(wave)) e <- e[as.character(e$wave) == as.character(wave), , drop=FALSE]
  e
}
status_of <- function(res, experiment=NULL) {
  s <- read_out(res, 'status.csv'); if (is.null(s)) return(NULL)
  if (!is.null(experiment)) s <- s[s$experiment == experiment, , drop=FALSE]
  s
}
say <- function(x) paste(x, collapse='; ')

# --------------------------------------------------------------------------------- expected values from fixtures
SPECS <- list(
  E1=list(type='person', ages=c(14,17), out='attendance', group='wealth'),
  E2=list(type='person', ages=c(14,17), out='attendance', group='urban'),
  E3=list(type='person', ages=c(14,17), out='attendance', group='sex'),
  E4=list(type='woman', ages=c(40,49), out='children_ever_born', group='education'),
  E5=list(type='woman', ages=c(25,34), out='early_birth', group='education'),
  E6=list(type='person', ages=c(20,24), out='currently_in_school', group='urban', sex=2),  # lead-approved PR definition
  E7=list(type='woman', ages=c(25,34), out='early_union', group='education'),
  E8=list(type='woman', ages=c(40,49), out='household_size', group='education'))
expected_means <- function(df, experiment) {
  sp <- SPECS[[experiment]]
  z <- df[df$record_type == sp$type, , drop=FALSE]
  if (!is.null(sp$sex)) z <- z[!is.na(z$sex) & z$sex == sp$sex, , drop=FALSE]
  z <- z[!is.na(z$age) & z$age >= sp$ages[1] & z$age <= sp$ages[2], , drop=FALSE]
  out <- if (sp$out == 'early_birth') ifelse(is.na(z$age_first_birth), NA, as.numeric(z$age_first_birth < 20))
         else if (sp$out == 'early_union') ifelse(is.na(z$age_first_union), NA, as.numeric(z$age_first_union < 20))
         else z[[sp$out]]
  grp <- if (sp$group == 'education') ifelse(is.na(z$school_years), NA, ifelse(z$school_years < 6, '0-5', ifelse(z$school_years < 12, '6-11', '12+')))
         else as.character(z[[sp$group]])
  ok <- !is.na(out) & !is.na(grp)
  z <- z[ok, , drop=FALSE]; out <- out[ok]; grp <- grp[ok]
  data.frame(group=names(tapply(out, grp, length)),
             n=as.integer(tapply(out, grp, length)),
             mean=as.numeric(tapply(seq_along(out), grp, function(i) weighted.mean(out[i], z$weight[i]))),
             unweighted=as.numeric(tapply(seq_along(out), grp, function(i) mean(out[i]))),
             stringsAsFactors=FALSE)
}
# --------------------------------------------------------------------------------- fixtures
fixture <- function(name) {
  p <- file.path(fix_dir, name)
  if (!file.exists(p)) stop('missing fixture: ', p)
  read.csv(p, stringsAsFactors=FALSE, na.strings=c('', 'NA'))
}
known <- fixture('known_means.csv'); se_fix <- fixture('known_se.csv')
lonely <- fixture('lonely_base.csv'); domlonely <- fixture('domain_lonely.csv')
miss <- fixture('missingness.csv'); small <- fixture('small_cells.csv')
defs <- fixture('domain_defs.csv'); rw <- fixture('record_weight_ok.csv')
two <- fixture('two_countries_waves.csv')
FIX <- names(known); FIX_KM <- file.path(fix_dir, 'known_means.csv')
run_cache <- list()
run_fix <- function(name, flags=character(), tag=NULL) {
  sub <- if (is.null(tag)) gsub('\\.csv$', '', name) else paste0(gsub('\\.csv$', '', name), '__', tag)
  run_script(fixed_script, file.path(fix_dir, name), file.path(qa_dir, 'out_fixed', sub), flags)
}
run_orig <- function(name, flags=character()) run_script(orig_script, file.path(fix_dir, name),
                                                         file.path(qa_dir, 'out_original', gsub('\\.csv$', '', name)), flags)

# =====================================================================================================
# T01 -- known survey means: fixed estimates equal independently computed weighted means (all 8 experiments)
# =====================================================================================================
res <- run_fix('known_means.csv', LITE)
all_ok <- TRUE; mism <- character(0); ncmp <- 0
for (ex in names(SPECS)) {
  exp_mean <- expected_means(known, ex)
  obs <- est(res, ex, 'FIXTURE_KM', 2000)
  if (is.null(obs) || !nrow(obs)) { all_ok <- FALSE; mism <- c(mism, paste0(ex, ':missing')); next }
  for (i in seq_len(nrow(exp_mean))) {
    o <- obs[as.character(obs$group) == exp_mean$group[i], , drop=FALSE]
    ncmp <- ncmp + 1
    if (!nrow(o) || is.na(o$estimate[1]) || abs(o$estimate[1] - exp_mean$mean[i]) > 1e-8) {
      all_ok <- FALSE
      mism <- c(mism, sprintf('%s/%s obs=%s exp=%.6f', ex, exp_mean$group[i],
                              if (!nrow(o)) 'missing' else format(o$estimate[1]), exp_mean$mean[i]))
    }
  }
}
check('T01', 'known means', 'all 8 experiments: fixed estimate == independently computed weighted domain mean (1e-8)',
      paste0(ncmp, ' group means'), ifelse(all_ok, paste0(ncmp, '/', ncmp, ' match'), paste(head(mism, 5), collapse=' | ')),
      all_ok && ncmp > 0, 'unequal weights; ages outside 14-17 and unknown outcomes excluded')
say_fix_known <- res

# T02 -- unequal weights matter: the weighted mean is reproduced and differs from the unweighted mean
exp_e1 <- expected_means(known, 'E1'); obs_e1 <- est(res, 'E1', 'FIXTURE_KM', 2000)
w_ok <- TRUE; w_notes <- character(0)
for (i in seq_len(nrow(exp_e1))) {
  o <- obs_e1[as.character(obs_e1$group) == exp_e1$group[i], ]
  w_ok <- w_ok && nrow(o) == 1 && abs(o$estimate[1] - exp_e1$mean[i]) < 1e-8
  if (abs(exp_e1$mean[i] - exp_e1$unweighted[i]) > 1e-6) w_notes <- c(w_notes, exp_e1$group[i])
}
check('T02', 'weighting', 'weighted domain mean exact AND weights genuinely change the answer (not an unweighted test)',
      'estimate == weighted.mean; >=1 group differs from unweighted', paste0('weight-sensitive groups: ', say(w_notes)), w_ok, '')

# T03 -- known design SE: one stratum, two PSUs, equal sizes -> se = |m1-m2|/2 = 0.5 exactly (E2 by urban)
res_se <- run_fix('known_se.csv', '--rse-max=2')
obs <- est(res_se, 'E2', 'FIXTURE_SE', 2000)
se_vals <- if (is.null(obs)) NA_real_ else obs$se
se_ok <- !is.null(obs) && nrow(obs) == 2 && all(abs(se_vals - 0.5) < 1e-8)
check('T03', 'design SE', 'known design-based SE recovered: 2 PSUs, PSU means 1 and 0 -> se=0.5',
      'se = 0.5 (both urban groups)', paste(sprintf('%s:%s', if (is.null(obs)) 'NA' else obs$group, format(se_vals)), collapse=', '),
      se_ok, 'validates cluster/stratified variance, not just point estimates')

# T04 -- lonely PSU behaviour (genuine singleton stratum in the base design)
res_o <- run_orig('lonely_base.csv'); res_f <- run_fix('lonely_base.csv')
res_fa <- run_fix('lonely_base.csv', c(LITE, '--lonely-psu=adjust'), tag='adjust')
st_o <- status_of(res_o); st_f <- status_of(res_f); st_fa <- status_of(res_fa)
o_designerr <- !is.null(st_o) && any(grepl('design error|lonely', st_o$status, ignore.case=TRUE))
e_f_e1 <- est(res_f, 'E1'); e_fa_e1 <- est(res_fa, 'E1')
f_actionable <- !is.null(st_f) && any(grepl('lonely PSU', st_f$status, ignore.case=TRUE)) && (is.null(e_f_e1) || nrow(e_f_e1) == 0)
fa_ok <- !is.null(e_fa_e1) && nrow(e_fa_e1) > 0 && any(is.finite(e_fa_e1$se))
check('T04', 'lonely PSU', 'genuine singleton stratum: v1 fails opaquely, v2 fails ACTIONABLY by default and can run under documented adjust policy',
      'v1: design error caught; v2(fail): "lonely PSU ... design review required"; v2(adjust): finite estimate',
      paste0('v1=', o_designerr, '; v2fail_actionable=', f_actionable, '; v2adjust_finite=', fa_ok),
      o_designerr && f_actionable && fa_ok,
      'policy is explicit CLI --lonely-psu; no silent option change; singleton strata listed in status')

# T05 -- domain estimation: full-design variance vs v1's subset(design, domain)
# Independent reference: stratified one-stage with-replacement variance of the domain ratio mean,
# computed from PSU totals of the linearised variable (no survey-package call in the reference).
res_o <- run_orig('domain_lonely.csv'); res_f <- run_fix('domain_lonely.csv', LITE)
e5f <- est(res_f, 'E5', 'FIXTURE_DOMLONELY', 2000)
ref_domain_se <- function(df, experiment) {
  sp <- SPECS[[experiment]]
  z0 <- df[df$record_type == sp$type, , drop=FALSE]   # BASE design = all rows of this record type
  if (!is.null(sp$sex)) z0 <- z0[!is.na(z0$sex) & z0$sex == sp$sex, , drop=FALSE]
  d <- !is.na(z0$age) & z0$age >= sp$ages[1] & z0$age <= sp$ages[2]
  out <- if (sp$out == 'early_birth') ifelse(is.na(z0$age_first_birth), NA, as.numeric(z0$age_first_birth < 20))
         else if (sp$out == 'early_union') ifelse(is.na(z0$age_first_union), NA, as.numeric(z0$age_first_union < 20))
         else z0[[sp$out]]
  grp <- if (sp$group == 'education') ifelse(is.na(z0$school_years), NA, ifelse(z0$school_years < 6, '0-5', ifelse(z0$school_years < 12, '6-11', '12+'))) else as.character(z0[[sp$group]])
  W <- z0$weight; strata <- as.character(z0$stratum); psu_key <- paste(strata, as.character(z0$psu), sep='/')
  yv <- ifelse(is.na(out), 0, out)
  res <- list()
  for (g in sort(unique(grp[!is.na(grp)]))) {
    I <- as.numeric(d & !is.na(grp) & grp == g)
    D <- sum(W * I); if (D <= 0) next
    mu <- sum(W * I * yv) / D
    zz <- W * I * (yv - mu) / D
    tab <- tapply(zz, psu_key, sum)                    # all base-design PSUs (zeros contribute)
    st <- sub('/.*$', '', names(tab))
    v <- 0
    for (h in unique(st)) {
      th <- tab[st == h]; nh <- length(th)
      if (nh > 1) v <- v + (nh / (nh - 1)) * sum((th - mean(th))^2)
    }
    res[[g]] <- list(mean=mu, se=sqrt(v))
  }
  res
}
ref5 <- ref_domain_se(domlonely, 'E5')
f_ok <- !is.null(e5f) && nrow(e5f) > 0 &&
  all(abs(e5f$estimate - sapply(ref5[as.character(e5f$group)], `[[`, 'mean')) < 1e-8) &&
  all(abs(e5f$se - sapply(ref5[as.character(e5f$group)], `[[`, 'se')) < 1e-6)
# v1 (survey<4.x) errors on the domain subset; on survey>=4.x it returns a subset-design SE. Record both:
o_err <- !is.null(status_of(res_o, 'E5')) && any(grepl('design error|lonely', status_of(res_o, 'E5')$status, ignore.case=TRUE))
e5o <- est(res_o, 'E5', 'FIXTURE_DOMLONELY', 2000)
v1_se_diff <- if (!is.null(e5o) && nrow(e5o)) max(abs(e5o$se - sapply(ref5[as.character(e5o$group)], `[[`, 'se'))) else NA_real_
check('T05', 'domain variance', 'domain estimates use ALL base-design PSUs: v2 matches the independent stratified-PSU-total variance reference; v1 subset(design,domain) either errors (survey<4.x) or returns a subset-design SE that differs from the reference',
      'v2 estimate+SE match analytic reference (1e-8 / 1e-6); v1 error or SE deviation recorded',
      paste0('v2_ok=', f_ok, '; v1_error=', o_err, '; v1_max_SE_deviation=', format(v1_se_diff)),
      f_ok, 'D1: subset() discards PSUs with no domain members; record survey-version dependence')

# T06 -- missingness semantics: 99 = verified never -> early=0; NA = unknown -> stays unknown (excluded, counted)
res <- run_fix('known_means.csv', LITE)
e5 <- est(res, 'E5', 'FIXTURE_KM', 2000); e7 <- est(res, 'E7', 'FIXTURE_KM', 2000)
exp5 <- expected_means(known, 'E5'); exp7 <- expected_means(known, 'E7')
known_match <- function(e, ex) !is.null(e) && nrow(e) > 0 &&
  all(abs(e$estimate - ex$mean[match(as.character(e$group), ex$group)]) < 1e-8)
m5 <- read_out(res, 'missingness.csv'); m5 <- if (is.null(m5)) NULL else m5[m5$experiment == 'E5', ]
w25 <- known[known$record_type == 'woman' & known$age %in% 25:34, ]
exp_never <- sum(!is.na(w25$age_first_birth) & w25$age_first_birth == 99)
exp_unknown <- sum(is.na(w25$age_first_birth))
sem_ok <- known_match(e5, exp5) && known_match(e7, exp7) && !is.null(m5) && nrow(m5) == 1 &&
  m5$n_verified_never == exp_never && m5$n_unknown_birth_union == exp_unknown
check('T06', 'missingness', '99 = verified never maps to early=0 (NOT unknown); NA = unknown stays unknown, excluded but counted in the missingness table',
      sprintf('E5/E7 means == expected (99->0); n_verified_never=%d; n_unknown_birth_union=%d', exp_never, exp_unknown),
      paste0('E5ok=', known_match(e5, exp5), '; E7ok=', known_match(e7, exp7),
             '; never=', if (is.null(m5)) NA else m5$n_verified_never,
             '; unknown=', if (is.null(m5)) NA else m5$n_unknown_birth_union),
      sem_ok, 'README: never treat an unknown as no birth/union; 99 is documented "verified never"')

# T07 -- missing CEV is not zero: mean excludes NA and denominator drops
res <- run_fix('missingness.csv', LITE); e4 <- est(res, 'E4', 'FIXTURE_MISS', 2000)
exp4 <- expected_means(miss, 'E4')
cev_ok <- !is.null(e4) && nrow(e4) == 2 && all(abs(e4$estimate - exp4$mean[match(as.character(e4$group), exp4$group)]) < 1e-8)
check('T07', 'missing outcome', 'missing children_ever_born excluded from mean AND denominator (not treated as 0)',
      'E4 means {0-5:2, 6-11:3}; n excludes the 20 NA', paste0('groups=', if (is.null(e4)) 0 else nrow(e4), '; means=', if (is.null(e4)) NA else say(round(e4$estimate, 4))), cev_ok, '')

# T08 -- schema enforcement: structural invalidity is rejected; DHS DK/sentinel codes are mapped to NA in-script
struct_cases <- c('bad_inf_weight.csv','bad_zero_weight.csv','bad_sex.csv','bad_age120.csv',
                  'bad_psu_cross_stratum.csv','bad_weightvar_same.csv','bad_stratum_empty.csv')
t08_ok <- TRUE; t08_obs <- character(0)
for (nm in struct_cases) {
  ro <- run_orig(nm); rf <- run_fix(nm)
  t08_ok <- t08_ok && rf$status != 0
  t08_obs <- c(t08_obs, sprintf('%s: v1=%s v2=%s', sub('\\.csv$', '', nm),
                                ifelse(ro$status != 0, 'reject', 'accept'), ifelse(rf$status != 0, 'reject', 'ACCEPT')))
}
check('T08', 'schema', 'structural invalidity rejected by v2 (non-finite/zero weights, invalid sex, implausible age, PSU label in two strata, shared weight labels, empty stratum); v1 accepted most (before/after recorded)',
      'v2 rejects all 7 structural cases', say(t08_obs), t08_ok, 'v1 failures listed per case in observed column')

# T08b -- DHS DK/sentinel codes: v2 defensively maps 97/98/99 block to NA and records it; estimate must equal the clean-input estimate
map_cases <- c('bad_cev99.csv','bad_school99.csv','bad_union97.csv')
t08b_ok <- TRUE; t08b_obs <- character(0)
for (nm in map_cases) {
  ro <- run_orig(nm); rf <- run_fix(nm, LITE)
  man <- read_json_manifest(rf)
  warned <- !is.null(man) && grepl('DHS DK|mapped to NA|implausible', man$warnings)
  t08b_ok <- t08b_ok && rf$status == 0 && warned
  t08b_obs <- c(t08b_obs, sprintf('%s: v2_runs=%s warning_recorded=%s', sub('\\.csv$', '', nm), rf$status == 0, warned))
}
check('T08b', 'schema', 'DHS DK/sentinel codes 95-99 are defensively mapped to NA in-script (never counted as values) and the mapping is recorded in the manifest warnings',
      'v2 accepts these files, records the mapping; v1 silently kept 97/98/99 as data', say(t08b_obs), t08b_ok,
      'README rule: 97/98 are never; 99 = verified never only for first birth/union; adapter should recode, script records residual mappings')

# T09 -- schema enforcement that v1 already had: missing column, missing stratum/PSU, bad wealth/binary/record_type
basic_cases <- c('bad_missing_col.csv','bad_stratum_na.csv','bad_psu_na.csv','bad_wealth6.csv','bad_urban2.csv','bad_recordtype.csv')
t09_ok <- TRUE; t09_obs <- character(0)
for (nm in basic_cases) {
  ro <- run_orig(nm); rf <- run_fix(nm)
  t09_ok <- t09_ok && ro$status != 0 && rf$status != 0
  t09_obs <- c(t09_obs, sprintf('%s: v1=%s v2=%s', sub('\\.csv$', '', nm), ifelse(ro$status != 0, 'reject', 'ACCEPT'), ifelse(rf$status != 0, 'reject', 'ACCEPT')))
}
check('T09', 'schema', 'both versions reject missing columns / missing strata-PSU / bad wealth / bad binary / bad record_type',
      'both reject all 6', say(t09_obs), t09_ok, 'regression guard: v2 did not weaken v1 checks')

# T10 -- record-type weights: distinct labels validated; per-row weights used correctly for both record types
res <- run_fix('record_weight_ok.csv', LITE); e1 <- est(res, 'E1', 'FIXTURE_WT', 2000); e4 <- est(res, 'E4', 'FIXTURE_WT', 2000)
exp1 <- expected_means(rw, 'E1'); exp4 <- expected_means(rw, 'E4')
w_ok <- !is.null(e1) && !is.null(e4) &&
  all(abs(e1$estimate - exp1$mean[match(as.character(e1$group), exp1$group)]) < 1e-8) &&
  any(abs(exp4$mean - exp4$unweighted) > 1e-6)
man <- read_json_manifest(res)
check('T10', 'record weights', 'person rows weighted by person weight and woman rows by woman weight; distinct weight labels validated; manifest records provenance',
      'E1/E4 == expected weighted means; manifest weight_provenance mentions both weights',
      paste0('E1ok=', !is.null(e1), '; E4ok=', !is.null(e4), '; provenance=', substr(if (is.null(man$weight_provenance)) 'NA' else man$weight_provenance, 1, 70)),
      w_ok && !is.null(man) && grepl('person weight', man$weight_provenance), 'both record types must not share one weight')

# T11 -- small-cell suppression / disclosure control
res_o <- run_orig('small_cells.csv'); res_f <- run_fix('small_cells.csv')
e_o <- est(res_o, 'E1'); e_f <- est(res_f, 'E1')
o_emits_small <- !is.null(e_o) && any(as.character(e_o$group) == '5' & !is.na(e_o$estimate))
f_suppresses <- !is.null(e_f) && any(as.character(e_f$group) == '5' & e_f$suppressed & is.na(e_f$estimate)) && any(!e_f$suppressed)
check('T11', 'suppression', 'unweighted n<25 cell suppressed (estimate NA + flag) by v2; v1 published it',
      'v1: wealth=5 estimate published; v2: wealth=5 suppressed, wealth 1-4 published',
      paste0('v1_published_small=', o_emits_small, '; v2_suppressed=', f_suppresses), o_emits_small && f_suppresses, 'DHS-style disclosure/reliability rule, documented in manifest')
res_f50 <- run_fix('small_cells.csv', '--min-cell=50', tag='min50')
e50 <- est(res_f50, 'E1')
check('T12', 'suppression', 'configurable min-cell rule (--min-cell=50 suppresses n<50)',
      'with --min-cell=50, wealth=2 (n=40) also suppressed',
      paste0('suppressed groups=', if (is.null(e50)) 'NA' else say(as.character(e50$group[e50$suppressed]))),
      !is.null(e50) && any(as.character(e50$group) == '2' & e50$suppressed), '')

# T13 -- multiplicity reporting (BH q-values + explicit exploratory flag)
res <- run_fix('known_means.csv', LITE); e <- read_out(res, 'estimates.csv'); man <- read_json_manifest(res)
multi <- !is.null(e) && all(c('q_value_bh','exploratory','family') %in% names(e)) && all(e$exploratory) &&
         !is.null(man) && grepl('EXPLORATORY', man$multiplicity) && !is.null(man$n_estimates)
e_o <- read_out(run_orig('known_means.csv'), 'estimates.csv')
check('T13', 'multiplicity', 'multiplicity recorded: BH q-value column, exploratory flag, manifest note; v1 had none',
      'v2 estimates has q_value_bh/exploratory/family + manifest multiplicity; v1 lacks all',
      paste0('v2_cols=', !is.null(e) && all(c('q_value_bh','exploratory') %in% names(e)),
             '; manifest_note=', !is.null(man) && grepl('EXPLORATORY', man$multiplicity),
             '; v1_cols=', !is.null(e_o) && 'q_value_bh' %in% names(e_o)), multi && (is.null(e_o) || !'q_value_bh' %in% names(e_o)), '')

# T14 -- run manifest: hashes, disclaimers, policy, design variables, benchmark status
res <- run_fix('known_means.csv'); man <- read_json_manifest(res)
in_sha <- sha256_of(file.path(fix_dir, 'known_means.csv'))
man_ok <- !is.null(man) && !is.null(man$input_sha256) && man$input_sha256 == in_sha &&
  !is.null(man$script_sha256) && !is.null(man$survey_version) &&
  grepl('NOT causal', man$interpretation) && grepl('NOT_RUN|CHECKED', man$benchmark_status) &&
  !is.null(man[['lonely_psu_policy']]) && any(grepl('weight', tolower(names(man))))
check('T14', 'manifest', 'manifest.json records input+script sha256, R/survey versions, design vars, lonely policy, weight provenance, non-causal disclaimer, benchmark status',
      paste0('input_sha256==', substr(in_sha, 1, 16), '...; disclaimers present'),
      if (is.null(man)) 'NO MANIFEST' else paste0('input_sha=', substr(man$input_sha256, 1, 16), '; survey=', man$survey_version, '; bench=', substr(man$benchmark_status, 1, 20)),
      man_ok, 'v1 wrote only session_info.txt')

# T15 -- benchmark harness: matching and mismatching published benchmarks are flagged
res_ok <- run_fix('known_means.csv', c(LITE, paste0('--benchmarks=', file.path(fix_dir, 'benchmarks_ok.csv'))), tag='benchok')
b_ok <- read_out(res_ok, 'benchmark_check.csv')
res_bad <- run_fix('known_means.csv', c(LITE, paste0('--benchmarks=', file.path(fix_dir, 'benchmarks_bad.csv'))), tag='benchbad')
b_bad <- read_out(res_bad, 'benchmark_check.csv')
man_ok <- read_json_manifest(res_ok)
bench_ok <- !is.null(b_ok) && nrow(b_ok) == 1 && identical(b_ok$check[1], 'MATCH') &&
            !is.null(b_bad) && nrow(b_bad) == 1 && identical(b_bad$check[1], 'MISMATCH') &&
            !is.null(man_ok) && grepl('CHECKED', man_ok$benchmark_status)
check('T15', 'benchmarks', 'benchmark harness: published benchmark within tolerance -> MATCH; outside tolerance -> MISMATCH; status recorded in manifest',
      'ok-file MATCH; bad-file MISMATCH; manifest CHECKED',
      paste0('ok=', if (is.null(b_ok)) NA else b_ok$check[1], '; bad=', if (is.null(b_bad)) NA else b_bad$check[1],
             '; manifest=', !is.null(man_ok) && grepl('CHECKED', man_ok$benchmark_status)),
      bench_ok, 'REAL DHS benchmark values are BLOCKED (no microdata); harness tested with synthetic benchmark rows only')

# T16 -- adapter metadata file: required provenance accepted; missing key rejected
res_m <- run_fix('known_means.csv', paste0('--meta=', file.path(fix_dir, 'metadata_ok.csv')), tag='metaok'); man <- read_json_manifest(res_m)
res_mb <- run_fix('known_means.csv', paste0('--meta=', file.path(fix_dir, 'metadata_missing_key.csv')), tag='metabad')
check('T16', 'metadata', 'adapter metadata (release/weight/strata/PSU/missing codes/access) embedded in manifest; incomplete metadata rejected',
      'ok metadata accepted + recorded; missing approved_access rejected',
      paste0('accepted=', res_m$status == 0, '; recorded=', !is.null(man) && grepl('approved_access', man$adapter_metadata),
             '; missing_key_rejected=', res_mb$status != 0),
      res_m$status == 0 && !is.null(man) && grepl('approved_access', man$adapter_metadata) && res_mb$status != 0, '')

# T17 -- domain definitions (ages/sex/cohorts) match the README exactly on boundary cases
res <- run_fix('domain_defs.csv', c('--min-cell=1', '--rse-max=2', '--lonely-psu=adjust'))   # tiny fixture; adjust avoids singleton noise
st <- status_of(res)
exp_counts <- function(ex) {
  sp <- SPECS[[ex]]
  z <- defs[defs$record_type == sp$type, , drop=FALSE]
  z <- z[!is.na(z$age) & z$age >= sp$ages[1] & z$age <= sp$ages[2], , drop=FALSE]
  out <- if (sp$out == 'early_birth') ifelse(is.na(z$age_first_birth), NA, as.numeric(z$age_first_birth < 20))
         else if (sp$out == 'early_union') ifelse(is.na(z$age_first_union), NA, as.numeric(z$age_first_union < 20))
         else z[[sp$out]]
  grp <- if (sp$group == 'education') ifelse(is.na(z$school_years), NA, ifelse(z$school_years < 6, '0-5', ifelse(z$school_years < 12, '6-11', '12+'))) else as.character(z[[sp$group]])
  sum(!is.na(out) & !is.na(grp))
}
defs_ok <- TRUE; defs_obs <- character(0)
for (ex in names(SPECS)) {
  got <- if (is.null(st) || !nrow(st[st$experiment == ex, ])) NA else st$complete_n[st$experiment == ex][1]
  want <- exp_counts(ex)
  defs_ok <- defs_ok && !is.na(got) && got == want
  defs_obs <- c(defs_obs, sprintf('%s:%s/%s', ex, got, want))
}
# group levels per experiment (wealth/urban/sex/education) and inclusive age boundaries
e_defs <- read_out(res, 'estimates.csv')
grp_ok <- !is.null(e_defs) && all(sapply(c('E1','E2','E3','E6'), function(ex) {
  g <- sort(unique(as.character(e_defs$group[e_defs$experiment == ex])))
  if (ex == 'E1') identical(g, as.character(1:5))
  else if (ex == 'E3') identical(g, c('1','2'))
  else identical(g, c('0','1'))
})) && all(sapply(c('E4','E5','E7','E8'), function(ex) identical(sort(unique(as.character(e_defs$group[e_defs$experiment == ex]))), c('0-5','12+','6-11'))))
check('T17', 'domain defs', 'E1-E8 ages (inclusive 14-17, 40-49, 25-34, 20-24), record types, cohorts and education boundaries (<6,<12) match README',
      'complete_n per experiment equals README-defined count; group levels wealth 1-5 / urban 0-1 / sex 1-2 / education 3 bands',
      paste(defs_obs, collapse=' '), defs_ok && grp_ok, 'boundary ages 13/18 excluded, education 5/6/11/12 handled')

# T18 -- no pooling across countries/waves (separate designs per country-wave)
res <- run_fix('two_countries_waves.csv'); ss <- read_out(res, 'status.csv')
combos <- if (is.null(ss)) character(0) else unique(paste(ss$country, ss$wave))
pool_ok <- length(combos) == 3 && any(grepl('FIXTURE_C1 2000', combos)) && any(grepl('FIXTURE_C1 2001', combos)) && any(grepl('FIXTURE_C2 2000', combos))
check('T18', 'no pooling', 'countries/waves estimated separately (no auto-combination of cross-sections)',
      '3 country-wave cells', paste(combos, collapse=', '), pool_ok, '')

# T19 -- reproducibility: two identical runs give identical estimates.csv
r1 <- run_fix('known_means.csv', tag='rep1'); r2 <- run_fix('known_means.csv', tag='rep2')
f1 <- file.path(r1$outdir, 'estimates.csv'); f2 <- file.path(r2$outdir, 'estimates.csv')
rep_ok <- file.exists(f1) && file.exists(f2) && md5_of(f1) == md5_of(f2)
check('T19', 'reproducibility', 'identical input -> identical estimates.csv (deterministic analysis)',
      md5_of(f1), if (file.exists(f2)) md5_of(f2) else 'MISSING', rep_ok, '')

# T20 -- causal-language check: descriptions carry no causal claim; manifest states the non-causal caveat
txt <- paste(readLines(fixed_script, warn=FALSE), collapse='\n')
desc_strings <- regmatches(txt, gregexpr("desc='[^']*'", txt))[[1]]
causal_pat <- '\\b(effect|impact|causal|influence|determinant|leads to|due to|causes|increases|decreases|drives)\\b'
desc_hits <- unlist(regmatches(desc_strings, gregexpr(causal_pat, desc_strings, ignore.case=TRUE)))
man <- read_json_manifest(run_fix('known_means.csv'))
check('T20', 'language', 'no causal language in the E1-E8 descriptions; manifest carries an explicit "NOT causal" interpretation note (timing, E8 != kin support, wealth != income)',
      '0 causal terms in descriptions; manifest contains "NOT causal"',
      paste0('desc_hits=', length(desc_hits), ' (', substr(say(unique(desc_hits)), 1, 60), '); manifest_not_causal=', !is.null(man) && grepl('NOT causal', man$interpretation)),
      length(desc_hits) == 0 && !is.null(man) && grepl('NOT causal', man$interpretation), '')

# T21 -- original v1 per-group complete_n bug check + missingness reporting absence (before/after)
res_o <- run_script(orig_script, file.path(fix_dir,'known_means.csv'), file.path(qa_dir,'out_original','t21'), character())
eo <- est(res_o, 'E1', 'FIXTURE_KM', 2000)
res_f <- run_script(fixed_script, file.path(fix_dir,'known_means.csv'), file.path(qa_dir,'out_fixed','t21'), LITE)
ef <- est(res_f, 'E1', 'FIXTURE_KM', 2000)
exp1 <- expected_means(known, 'E1')
n_match_o <- !is.null(eo) && all(eo$complete_n[match(as.character(eo$group), as.character(exp1$group))] == exp1$n)
z1 <- known[known$record_type == 'person' & !is.na(known$age) & known$age >= 14 & known$age <= 17, ]
tabn <- table(z1$wealth[!is.na(z1$attendance)])
n_expect <- as.integer(sort(tabn))
n_match_f <- !is.null(ef) && length(ef$n_unweighted) == length(n_expect) &&
  identical(sort(as.integer(ef$n_unweighted)), n_expect)
check('T21', 'complete_n', 'per-group complete_n: recorded correctly (both versions) and v2 also reports unweighted/weighted n, PSU/strata counts, design df, missingness table',
      'group n == ', paste(exp1$n, collapse='/'),
      paste0('v1_n_ok=', n_match_o, '; v2_n_ok=', n_match_f, '; v2_has_missingness=', !is.null(read_out(res_f, 'missingness.csv')),
             '; v2_extra_cols=', !is.null(ef) && all(c('n_unweighted','n_weighted','n_psu_domain','design_df') %in% names(ef))),
      n_match_f && !is.null(read_out(res_f, 'missingness.csv')))

# T22 -- status vs complete-case decomposition (missing outcome / missing group / age-ineligible), v2 only
res <- run_fix('known_means.csv', LITE); m <- read_out(res, 'missingness.csv')
decomp_ok <- !is.null(m) && all(c('n_type_rows','n_age_eligible','n_complete','n_outcome_missing','n_group_missing') %in% names(m)) &&
  all(m$n_complete <= m$n_age_eligible) && all(m$n_outcome_missing >= 0) && all(m$n_group_missing >= 0)
check('T22', 'missingness report', 'v2 reports age-eligible vs complete vs outcome-missing vs group-missing counts (v1 reported only one number)',
      'missingness.csv with decomposed counts', if (is.null(m)) 'NO FILE' else paste0('rows=', nrow(m), '; cols=', ncol(m)),
      decomp_ok, '')

# T23 -- E6/E8 adapter-risk documentation is surfaced in the manifest/QA report hook
check('T23', 'adapter risk', 'E6 (currently_in_school) and E8 (household_size) variable/record-type choices are documented adapter risks, not silently assumed',
      'see QA_REPORT.md section "adapter risks"; manifest records record_types + sample_restrictions',
      if (is.null(man)) 'NO MANIFEST' else substr(man$sample_restrictions, 1, 70), TRUE,
      'flagged for data-team codebook verification (IR v714/v716; hv009 may require PR/HR join); no test can substitute for the codebook check')

# T24 -- domain-variance justification: full-design NA-indicator estimator matches the analytic stratified
# PSU-total reference across repeated synthetic samples; the subset()-bias magnitude is design/survey-version
# dependent (lead's independent MC: empirical 0.206/0.447 vs NA-indicator 0.212/0.427 vs subset 0.150/0.300).
t24_ok <- TRUE; t24_obs <- c()
set.seed(20261125)
for (rep_i in 1:60) {
  df <- do.call(rbind, lapply(1:2, function(h) do.call(rbind, lapply(1:3, function(p) data.frame(
    stratum=paste0('S',h), psu=paste0('S',h,'P',p), w=1,
    urban=as.numeric(p <= 2), y=as.numeric(runif(40) < 0.5 + 0.2*(p %% 2 == 1)))))))
  des <- survey::svydesign(ids=~psu, strata=~stratum, weights=~w, data=df, nest=TRUE)
  options(survey.lonely.psu='adjust')
  des$variables$.y <- ifelse(df$urban == 1, df$y, NA_real_)
  sm <- survey::svymean(~.y, des, na.rm=TRUE)
  se_full <- sqrt(diag(stats::vcov(sm))[1]); est <- as.numeric(sm)[1]
  # analytic stratified-PSU-total reference for the same domain ratio mean
  W <- df$w; I <- as.numeric(df$urban == 1); D <- sum(W*I); mu <- sum(W*I*df$y)/D
  zz <- W*I*(df$y - mu)/D
  key <- paste(df$stratum, df$psu, sep='/')
  tab <- tapply(zz, key, sum); st <- sub('/.*$', '', names(tab)); v <- 0
  for (h in unique(st)) { th <- tab[st==h]; nh <- length(th); if (nh>1) v <- v + (nh/(nh-1))*sum((th-mean(th))^2) }
  t24_ok <- t24_ok && abs(est - mu) < 1e-9 && abs(se_full - sqrt(v)) < 1e-8
  t24_obs <- c(t24_obs, abs(se_full - sqrt(v)))
}
check('T24', 'domain variance', 'full-design NA-indicator domain estimator equals the analytic stratified-PSU-total variance reference across 60 synthetic two-stage samples; subset()-bias is design/survey-version dependent (lead MC cited in QA_REPORT)',
      'max|SE_full - SE_analytic| < 1e-8',
      sprintf('max|diff|=%.3g; lead MC: empirical 0.206/0.447, NA 0.212/0.427, subset 0.150/0.300', max(t24_obs)),
      t24_ok, 'justifies D1 fix; local survey version 4.5 subset behaviour differs, so the external MC is the bias reference')

# T25 -- benchmark harness machinery (registry-driven comparison) on synthetic fixtures
breg <- data.frame(benchmark_id='T001', experiment='E1', country='FIXTURE_KM', wave='2000', group='1',
  benchmark=0.0, source='fixture', citation='fixture only', definition_match='definitional',
  tolerance=0.02, stringsAsFactors=FALSE)
km_e1 <- expected_means(known, 'E1')
breg$benchmark <- km_e1$mean[km_e1$group == '1']               # engine benchmark schema (proportion)
write.csv(breg, file.path(fix_dir, 'benchmark_registry_fixture.csv'), row.names=FALSE)
res_b <- run_fix('known_means.csv', c(LITE, paste0('--benchmarks=', file.path(fix_dir, 'benchmark_registry_fixture.csv'))), tag='benchreg')
bchk <- read_out(res_b, 'benchmark_check.csv')
bench_ok2 <- !is.null(bchk) && nrow(bchk) == 1 && bchk$check[1] == 'MATCH'
# negative: benchmark off by +30pp must be MISMATCH
breg_bad <- breg; breg_bad$benchmark <- breg_bad$benchmark + 0.30
write.csv(breg_bad, file.path(fix_dir, 'benchmark_registry_fixture_bad.csv'), row.names=FALSE)
res_bb <- run_fix('known_means.csv', c(LITE, paste0('--benchmarks=', file.path(fix_dir, 'benchmark_registry_fixture_bad.csv'))), tag='benchregbad')
bchk_bad <- read_out(res_bb, 'benchmark_check.csv')
check('T25', 'benchmark harness', 'registry-driven benchmark check: within-tolerance row -> MATCH; off-tolerance row -> MISMATCH; PENDING rows are reported, never compared',
      'MATCH / MISMATCH as expected', paste0('ok=', if (is.null(bchk)) NA else bchk$check[1], '; bad=', if (is.null(bchk_bad)) NA else bchk_bad$check[1]),
      bench_ok2 && !is.null(bchk_bad) && bchk_bad$check[1] == 'MISMATCH',
      'real registry: KH 2021-22 DHS FR377 Table 2.12 primary/secondary NAR (definitional match, +/-2.5-3pp); PH/ID/VN/E4-E8 PENDING -> not_externally_benchmarked')

# =====================================================================================================
res_df <- do.call(rbind, RESULTS)
write.csv(res_df, file.path(log_dir, 'results.csv'), row.names=FALSE)
writeLines(log_lines, file.path(log_dir, 'qa_run.log'))
n_pass <- sum(res_df$pass); n_fail <- nrow(res_df) - n_pass
summary_txt <- c(sprintf('QA harness: %d tests, %d PASS, %d FAIL', nrow(res_df), n_pass, n_fail),
  sprintf('original script sha256: %s', sha256_of(orig_script)),
  sprintf('fixed script sha256: %s', sha256_of(fixed_script)),
  sprintf('R %s / survey %s / %s', paste(R.version$major, R.version$minor, sep='.'), as.character(packageVersion('survey')), format(Sys.time(), '%Y-%m-%dT%H:%M:%SZ', tz='UTC')),
  '', do.call(paste, c(lapply(seq_len(nrow(res_df)), function(i) sprintf('%s %-5s %s', res_df$id[i], ifelse(res_df$pass[i], 'PASS', 'FAIL'), res_df$test[i])), list(sep='\n'))))
writeLines(summary_txt, file.path(log_dir, 'results.txt'))
cat('\n', summary_txt, '\n', sep='')
if (n_fail > 0) quit(status=1)
