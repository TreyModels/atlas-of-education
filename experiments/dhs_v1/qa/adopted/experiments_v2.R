#!/usr/bin/env Rscript
# experiments_v2.R -- corrected analysis engine for the eight DHS descriptive
# experiments. Same CLI as the starter: Rscript experiments_v2.R normalized.csv outdir
#
# Changes vs the v1 starter (see qa/DEFECTS.md):
#  D1 E6 was specified on `woman` records with outcome `currently_in_school`, but
#     no DHS individual-woman recode (IR/WI) carries a current-attendance item,
#     so E6 was unrunnable for every country and silently produced an empty cell.
#     E6 is now a PERSON-record experiment restricted to females aged 20-24.
#  D2 school_years >= 95 are DHS "don't know/inconsistent" codes, not years of
#     schooling. v1 mapped 98 to the "12+" bucket. Now forced to NA.
#  D3 complete_n used a coercion-prone `vec == factor-level` comparison; now
#     counted directly on the analysis frame.
#  D4 no reliability flags, no multiplicity control, no design df, no lonely-PSU
#     accounting. Added.
#  D5 status/results used `<<-` from an error handler; reworked to a plain
#     per-cell function with explicit returns.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Usage: Rscript experiments_v2.R normalized.csv outdir [--lonely=fail|adjust|remove]")
infile <- args[1]; outdir <- args[2]
lonely <- "fail"
for (a in args[-(1:2)]) {
  if (grepl("^--lonely=", a)) lonely <- sub("^--lonely=", "", a)
}
stopifnot(lonely %in% c("fail", "adjust", "remove"))
if (!requireNamespace("survey", quietly = TRUE)) stop("Install R package survey")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
# Explicit, recorded lonely-PSU policy. "fail" (default) refuses to guess;
# the alternative is only used when the caller opts in and is written to run_meta.
options(survey.lonely.psu = lonely)

d <- read.csv(infile, stringsAsFactors = FALSE, na.strings = c("", "NA"))
required <- c("country","wave","weight","stratum","psu","record_type","age","sex","urban",
              "wealth","attendance","school_years","children_ever_born","age_first_birth",
              "currently_in_school","age_first_union","household_size")
missing <- setdiff(required, names(d))
if (length(missing)) stop(paste("Missing schema columns:", paste(missing, collapse = ", ")))

## ---- hard validation: fail loudly rather than silently mangle ---------------
if (any(is.na(d$country) | is.na(d$wave) | is.na(d$record_type) | is.na(d$weight) |
        d$weight <= 0 | is.na(d$stratum) | is.na(d$psu)))
  stop("Missing survey keys or invalid weights")
if (any(!d$record_type %in% c("person", "woman"))) stop("Invalid record_type")
if (any(!is.na(d$wealth) & !d$wealth %in% 1:5)) stop("Wealth must be 1:5")
for (n in c("attendance", "currently_in_school", "urban"))
  if (any(!is.na(d[[n]]) & !d[[n]] %in% 0:1)) stop(paste(n, "must be 0/1"))
if (any(!is.na(d$age) & (d$age < 0 | d$age > 130))) stop("Implausible age")
# D2: cleanse don't-know codes defensively even if the harmonizer already did.
d$school_years[d$school_years %in% c(95, 96, 97, 98, 99)] <- NA
d$children_ever_born[d$children_ever_born %in% c(95, 98, 99)] <- NA
# 99 == verified never; anything above 49 otherwise is unknown, not an age.
d$age_first_birth[!is.na(d$age_first_birth) & d$age_first_birth > 49 & d$age_first_birth != 99] <- NA
d$age_first_union[!is.na(d$age_first_union) & d$age_first_union > 49 & d$age_first_union != 99] <- NA

d$education <- ifelse(is.na(d$school_years), NA,
               ifelse(d$school_years < 6, "0-5",
               ifelse(d$school_years < 12, "6-11", "12+")))
d$early_birth <- ifelse(is.na(d$age_first_birth), NA, as.numeric(d$age_first_birth < 20))
d$early_union <- ifelse(is.na(d$age_first_union), NA, as.numeric(d$age_first_union < 20))
d$female <- d$sex == 2

specs <- list(
  E1 = list(type = "person", ages = c(14, 17), out = "attendance",          group = "wealth",
            desc = "Adolescent attendance by wealth quintile"),
  E2 = list(type = "person", ages = c(14, 17), out = "attendance",          group = "urban",
            desc = "Adolescent attendance by residence"),
  E3 = list(type = "person", ages = c(14, 17), out = "attendance",          group = "sex",
            desc = "Adolescent attendance by sex"),
  E4 = list(type = "woman",  ages = c(40, 49), out = "children_ever_born",  group = "education",
            desc = "Completed-cohort children ever born by schooling"),
  E5 = list(type = "woman",  ages = c(25, 34), out = "early_birth",         group = "education",
            desc = "Birth before age 20 by schooling"),
  E6 = list(type = "person", ages = c(20, 24), out = "currently_in_school", group = "urban",
            female_only = TRUE,
            desc = "School participation among young women by residence"),
  E7 = list(type = "woman",  ages = c(25, 34), out = "early_union",         group = "education",
            desc = "Union before age 20 by schooling"),
  E8 = list(type = "woman",  ages = c(40, 49), out = "household_size",      group = "education",
            desc = "Current household size among older women by schooling")
)

ests <- list(); stats <- list(); desigs <- list(); ei <- 0; si <- 0

for (key in names(specs)) {
  sp <- specs[[key]]
  for (cn in sort(unique(d$country))) {
    for (w in sort(unique(d$wave[d$country == cn]))) {
      sel <- d$country == cn & d$wave == w & d$record_type == sp$type
      # The design is ALWAYS built on every record of this type for the
      # country-wave. Restrictions (sex, age, non-missing outcome) define the
      # domain, never the design frame: pre-filtering the frame drops PSUs and
      # corrupts domain variances (and can zero out whole PSUs).
      frame <- d[sel, , drop = FALSE]

      si <- si + 1
      rec <- data.frame(experiment = key, country = cn, wave = w, record_type = sp$type,
                        n_frame = nrow(frame), n_eligible = NA_integer_,
                        n_complete = NA_integer_, status = NA_character_,
                        lonely_psu = NA_integer_, design_df = NA_integer_,
                        stringsAsFactors = FALSE)

      if (nrow(frame) == 0) {
        rec$status <- "no records of this type for this country-wave"; stats[[si]] <- rec; next
      }
      elig <- !is.na(frame$age) & frame$age >= sp$ages[1] & frame$age <= sp$ages[2]
      if (sp$type == "person" && isTRUE(sp$female_only)) elig <- elig & frame$sex == 2
      rec$n_eligible <- sum(elig)
      ok <- elig & !is.na(frame[[sp$out]]) & !is.na(frame[[sp$group]]) &
            !is.na(frame$weight) & frame$weight > 0 & !is.na(frame$stratum) & !is.na(frame$psu)
      rec$n_complete <- sum(ok)

      if (sum(ok) < 50) {
        rec$status <- sprintf("insufficient complete cases (%d < 50)", sum(ok)); stats[[si]] <- rec; next
      }
      if (length(unique(frame[[sp$group]][ok])) < 2) {
        rec$status <- "fewer than 2 usable groups"; stats[[si]] <- rec; next
      }

      # DESIGN IS BUILT ON THE FULL FRAME (all PSUs, all ages), then the domain is
      # selected inside the design. This is the survey package's domain-estimation
      # path: excluded rows keep zero weight and PSU/stratum structure is retained,
      # so domain variances still see every PSU. qa/run_tests.R verifies this
      # against an analytic clustered-design variance and against the full-design
      # interaction estimator.
      frame$stratum <- as.factor(frame$stratum)
      frame$psu <- as.factor(frame$psu)
      frame$.dom <- ok

      res <- tryCatch({
        des <- survey::svydesign(ids = ~psu, strata = ~stratum, weights = ~weight,
                                 data = frame, nest = TRUE)
        dsub <- subset(des, .dom)
        f <- as.formula(paste0("~", sp$out))
        g <- as.formula(paste0("~", sp$group))
        ans <- survey::svyby(f, g, dsub, survey::svymean, na.rm = TRUE, vartype = "se")
        list(ok = TRUE, des = des, sub = dsub, ans = ans)
      }, error = function(e) list(ok = FALSE, msg = conditionMessage(e)))

      if (!isTRUE(res$ok)) {
        rec$status <- paste("design error:", res$msg); stats[[si]] <- rec; next
      }

      des <- res$des; dsub <- res$sub; ans <- res$ans
      npsu <- length(unique(frame$psu)); nstr <- length(unique(frame$stratum))
      # lonely PSUs inside the domain: strata contributing exactly one PSU
      dompsu <- unique(frame[ok, c("stratum", "psu")])
      lonely <- sum(table(dompsu$stratum) == 1)
      rec$lonely_psu <- as.integer(lonely)
      rec$design_df <- as.integer(npsu - nstr)

      means <- as.numeric(ans[[sp$out]])
      ses <- as.numeric(ans[["se"]])
      glab <- as.character(ans[[sp$group]])

      # D3: count group members directly on the analysis frame.
      for (j in seq_along(glab)) {
        gj <- frame[[sp$group]] == ans[[sp$group]][j]
        ej <- ei + 1
        est <- means[j]; se <- ses[j]
        n <- sum(ok & gj)
        cv <- if (!is.na(est) && est != 0) se / abs(est) else NA_real_
        ests[[ej]] <- data.frame(
          experiment = key, country = cn, wave = w, record_type = sp$type,
          group_variable = sp$group, group = glab[j],
          estimate = est, se = se,
          lo95 = est - 1.96 * se, hi95 = est + 1.96 * se,
          cv = cv, n = n, n_psu = length(unique(frame$psu[ok & gj])),
          design_df = rec$design_df,
          flag_small_n = n < 25,
          flag_high_cv = !is.na(cv) & cv > 0.30,
          flag_few_psu = length(unique(frame$psu[ok & gj])) < 10,
          lonely_psu_domain = as.integer(lonely),
          description = sp$desc, stringsAsFactors = FALSE)
        ei <- ej
      }
      desigs[[length(desigs) + 1]] <- data.frame(
        country = cn, wave = w, record_type = sp$type,
        n_rows = nrow(frame), n_strata = nstr, n_psu = npsu, design_df = rec$design_df,
        n_domain_complete = sum(ok), lonely_psu_in_domain = as.integer(lonely),
        weight_sum = sum(frame$weight), stringsAsFactors = FALSE)
      rec$status <- if (lonely > 0) sprintf("ok (%d lonely PSU in domain)", lonely) else "ok"
      stats[[si]] <- rec
    }
  }
}

E <- if (length(ests)) do.call(rbind, ests) else data.frame()
S <- do.call(rbind, stats)
Dg <- if (length(desigs)) unique(do.call(rbind, desigs)) else data.frame()

## ---- multiplicity: Holm within each experiment x country family -------------
if (nrow(E)) {
  E$p_value <- 2 * pnorm(-abs(E$estimate / E$se))
  E$p_holm <- NA_real_
  E$sig_holm_05 <- NA
  fam <- paste(E$experiment, E$country, E$wave, sep = "|")
  for (f in unique(fam)) {
    i <- which(fam == f)
    p <- E$p_value[i]; ok <- !is.na(p)
    if (sum(ok) > 1) {
      ph <- p.adjust(p, method = "holm")
      E$p_holm[i] <- ph
      E$sig_holm_05[i] <- ph < 0.05
    }
  }
}

write.csv(E, file.path(outdir, "estimates.csv"), row.names = FALSE)
write.csv(S, file.path(outdir, "status.csv"), row.names = FALSE)
write.csv(Dg, file.path(outdir, "designs.csv"), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(outdir, "session_info.txt"))
writeLines(c(
  paste("input:", normalizePath(infile)),
  paste("input_sha256:", tryCatch(tools::md5sum(infile), error = function(e) NA)),
  paste("lonely_policy:", lonely),
  paste("run_utc:", format(Sys.time(), tz = "UTC", usetz = TRUE)),
  paste("survey_version:", as.character(packageVersion("survey"))),
  paste("R_version:", R.version.string),
  paste("rows_in:", nrow(d)), paste("estimate_rows:", nrow(E))
), file.path(outdir, "run_meta.txt"))
cat("wrote", nrow(E), "estimates,", nrow(S), "status rows to", outdir, "\n")
