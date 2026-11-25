#!/usr/bin/env Rscript
# run_tests.R -- independent verification of the experiments_v2.R engine.
# ALL DATA HERE IS SYNTHETIC. It exists only to validate the estimator; nothing
# in this file is a survey result and no number here may be reported as one.
#
# Every test compares the engine's design-based output against an independently
# computed quantity (closed form or a hand-written Taylor linearisation).

suppressPackageStartupMessages(library(survey))
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
engine <- file.path(here, "experiments_v2.R")
stopifnot(file.exists(engine))
RSCRIPT <- file.path(R.home("bin"), "Rscript")

PASS <- 0L; FAIL <- 0L; LOG <- character(0)
chk <- function(name, cond, detail = "") {
  if (isTRUE(cond)) { PASS <<- PASS + 1L; LOG <<- c(LOG, sprintf("PASS  %-58s %s", name, detail)) }
  else { FAIL <<- FAIL + 1L; LOG <<- c(LOG, sprintf("FAIL  %-58s %s", name, detail)) }
}
near <- function(a, b, tol) isTRUE(all.equal(as.numeric(a), as.numeric(b), tolerance = tol))

# Independent hand-written Taylor linearisation of a domain mean, PSU totals
# within strata. This is the gold standard the engine must reproduce.
manual_domain <- function(y, w, stratum, psu, dom) {
  keep <- dom & !is.na(y) & !is.na(w) & w > 0
  W <- sum(w[keep]); m <- sum(w[keep] * y[keep]) / W
  z <- w * dom * (y - m) / W
  z[!keep] <- 0
  tot <- tapply(z, list(stratum, psu), sum)
  v <- 0
  for (h in rownames(tot)) {
    row <- tot[h, ]; row <- row[!is.na(row)]
    n <- length(row)
    if (n > 1) v <- v + n / (n - 1) * sum((row - mean(row))^2)
  }
  c(mean = m, se = sqrt(v))
}

schema <- function(df) {
  need <- c("country","wave","weight","stratum","psu","record_type","age","sex","urban",
            "wealth","attendance","school_years","children_ever_born","age_first_birth",
            "currently_in_school","age_first_union","household_size")
  for (n in need) if (!n %in% names(df)) df[[n]] <- NA
  df[, need]
}
run_engine <- function(df, tag) {
  td <- file.path(tempdir(), paste0("t_", tag)); dir.create(td, showWarnings = FALSE)
  f <- file.path(td, "in.csv"); write.csv(schema(df), f, row.names = FALSE)
  od <- file.path(td, "out"); dir.create(od, showWarnings = FALSE)
  rc <- system2(RSCRIPT, c(shQuote(engine), shQuote(f), shQuote(od)), stdout = TRUE, stderr = TRUE)
  e <- tryCatch(read.csv(file.path(od, "estimates.csv")), error = function(x) NULL)
  list(est = e, out = rc, dir = od)
}

## ---------------------------------------------------------------- T1: SRS ---
set.seed(11)
n <- 4000
y <- rnorm(n, 50, 15)
d1 <- data.frame(country = "SYN", wave = "T1", weight = 1, stratum = "1", psu = seq_len(n),
                 record_type = "person", age = 15, sex = 1, urban = 1, wealth = 1,
                 attendance = as.numeric(y > 50), school_years = 6)
r1 <- run_engine(d1, "t1")
e1 <- r1$est[r1$est$experiment == "E2", ]
# E2 splits by urban; force two groups instead
d1$urban <- rep(0:1, length.out = n)
r1 <- run_engine(d1, "t1b"); e1 <- r1$est[r1$est$experiment == "E2", ]
got <- e1$estimate[e1$group == "1"]
want <- mean(d1$attendance[d1$urban == 1])
chk("T1 SRS point estimate equals closed form", near(got, want, 1e-6),
    sprintf("engine=%.6f closed=%.6f", got, want))
se_want <- sqrt(var(d1$attendance[d1$urban == 1]) / sum(d1$urban == 1))
chk("T1 SRS SE within 2% of s/sqrt(n)", abs(e1$se[e1$group == "1"] - se_want) / se_want < 0.02,
    sprintf("engine=%.6f closed=%.6f", e1$se[e1$group == "1"], se_want))

## ------------------------------------------- T2: stratified, known variance ---
set.seed(22)
mk <- function() {
  do.call(rbind, lapply(1:10, function(h) {
    nh <- 40
    data.frame(stratum = as.character(h), psu = paste0(h, "-", 1:nh),
               y = rnorm(nh, 40 + h, 5))
  }))
}
S2 <- mk()
S2$country <- "SYN"; S2$wave <- "T2"; S2$weight <- 1; S2$record_type <- "person"
S2$age <- 15; S2$sex <- 1; S2$wealth <- 1; S2$school_years <- 6
S2$urban <- as.integer(S2$stratum %in% as.character(1:5))
S2$attendance <- as.numeric(S2$y > 40)
r2 <- run_engine(S2, "t2"); e2 <- r2$est[r2$est$experiment == "E2", ]
m2 <- manual_domain(S2$attendance, S2$weight, S2$stratum, S2$psu, S2$urban == 1)
chk("T2 stratified cluster mean == manual linearisation", near(e2$estimate[e2$group == "1"], m2["mean"], 1e-8),
    sprintf("engine=%.8f manual=%.8f", e2$estimate[e2$group == "1"], m2["mean"]))
chk("T2 stratified cluster SE == manual linearisation", near(e2$se[e2$group == "1"], m2["se"], 1e-6),
    sprintf("engine=%.8f manual=%.8f", e2$se[e2$group == "1"], m2["se"]))

## ---------------------------- T3: domain whose PSUs are partly outside it ----
# Half the PSUs have no eligible person at all. A naive "drop rows then build
# design" analysis loses those PSUs and understates the variance.
set.seed(33)
S3 <- do.call(rbind, lapply(1:12, function(h) {
  do.call(rbind, lapply(1:8, function(p) {
    in_dom <- (h + p) %% 2 == 0
    data.frame(stratum = as.character(h), psu = paste0(h, "-", p),
               age = if (in_dom) 15 else 30,
               y = rnorm(1, 0.5, 0.2))
  }))
}))
S3$country <- "SYN"; S3$wave <- "T3"; S3$weight <- 1; S3$record_type <- "person"
S3$sex <- 1; S3$wealth <- 1; S3$school_years <- 6; S3$urban <- 1
S3$attendance <- as.numeric(S3$y > 0.5)
r3 <- run_engine(S3, "t3"); e3 <- r3$est[r3$est$experiment == "E2", ]
m3 <- manual_domain(S3$attendance, S3$weight, S3$stratum, S3$psu, S3$age == 15)
chk("T3 domain SE with PSUs outside domain == manual", near(e3$se[1], m3["se"], 1e-6),
    sprintf("engine=%.8f manual=%.8f", e3$se[1], m3["se"]))
# compare with the WRONG approach for the record
des_wrong <- svydesign(ids = ~psu, strata = ~stratum, weights = ~weight,
                       data = S3[S3$age == 15, ], nest = TRUE)
wrong <- as.numeric(SE(svymean(~attendance, des_wrong)))
chk("T3 naive row-drop SE differs (documents the trap)", !near(wrong, m3["se"], 1e-4),
    sprintf("naive=%.6f correct=%.6f", wrong, m3["se"]))

## --------------------------------------------------- T4: lonely PSU policy ---
# Stratum h1 contains exactly ONE PSU that has any in-domain (age 15) member.
# survey must refuse under survey.lonely.psu="fail"; the engine must surface it.
set.seed(44)
T4 <- do.call(rbind, lapply(1:8, function(h) {
  do.call(rbind, lapply(1:6, function(p) {
    n_in <- if (h == 1 && p > 1) 0 else 10   # stratum 1 keeps a single in-domain PSU
    data.frame(stratum = as.character(h), psu = paste0(h, "-", p),
               age = c(rep(15, n_in), rep(30, 10 - n_in)),
               urban = rep(c(0, 1), length.out = 10),
               y = rnorm(10, 0.5, 0.2))
  }))
}))
T4$country <- "SYN"; T4$wave <- "T4"; T4$weight <- 1; T4$record_type <- "person"
T4$sex <- 1; T4$wealth <- 1; T4$school_years <- 6
T4$attendance <- as.numeric(T4$y > 0.5)
r4 <- run_engine(T4, "t4")
st4 <- tryCatch(read.csv(file.path(r4$dir, "status.csv")), error = function(e) NULL)
chk("T4a domain-lonely PSU is detected and reported",
    !is.null(st4) && any(grepl("lonely|design error", st4$status)),
    if (!is.null(st4)) paste(unique(st4$status), collapse = " | ") else "no status file")

# T4b: a DESIGN-level singleton (a stratum with one PSU in the sample) must
# stop the analysis under the default policy instead of being silently absorbed.
set.seed(47)
T4b <- do.call(rbind, lapply(1:6, function(h) {
  do.call(rbind, lapply(1:5, function(p) {
    data.frame(stratum = as.character(h), psu = paste0(h, "-", p),
               age = 15, urban = rep(c(0,1), length.out = 8),
               y = rnorm(8, 0.5, 0.2))
  }))
}))
T4b <- rbind(T4b, data.frame(stratum = "99", psu = "99-1", age = 15,
                             urban = c(0,1,0,1,0,1,0,1), y = rnorm(8, 0.5, 0.2)))
T4b$country <- "SYN"; T4b$wave <- "T4b"; T4b$weight <- 1; T4b$record_type <- "person"
T4b$sex <- 1; T4b$wealth <- 1; T4b$school_years <- 6
T4b$attendance <- as.numeric(T4b$y > 0.5)
r4b <- run_engine(T4b, "t4b")
st4b <- tryCatch(read.csv(file.path(r4b$dir, "status.csv")), error = function(e) NULL)
chk("T4b design-level lonely PSU stops the run under policy=fail",
    !is.null(st4b) && any(grepl("lonely|design error", st4b$status)),
    if (!is.null(st4b)) paste(unique(st4b$status), collapse = " | ") else "no status file")

## ------------------------------------- T5: never / unknown code propagation ---
# Hand-computable and multi-group. 20 PSUs x 8 women (25-34).
# Within each PSU: 4 women with school_years=8 (education "6-11") and
# 4 with school_years=14 ("12+"); in each group of four the age at first birth
# is 18, 25, 99 (verified never) and NA (unknown).
# Correct "6-11" estimate = 20 early / 60 known = 1/3; n must be 60, not 80.
set.seed(55)
T5 <- do.call(rbind, lapply(1:20, function(p) {
  data.frame(
    country = "SYN", wave = "T5", weight = 1, stratum = "1", psu = p,
    record_type = "woman", age = 30, sex = 2, urban = 1, wealth = NA,
    attendance = NA, school_years = rep(c(8, 8, 8, 8, 14, 14, 14, 14), 1),
    children_ever_born = 2,
    age_first_birth = rep(c(18, 25, 99, NA), 2),
    currently_in_school = NA, age_first_union = 99, household_size = 5)
}))
r5 <- run_engine(T5, "t5"); e5 <- r5$est[r5$est$experiment == "E5", ]
got5 <- e5$estimate[e5$group == "6-11"]; n5 <- e5$n[e5$group == "6-11"]
chk("T5a 99='never' is a known not-early-birth (20/60=0.3333)", near(got5, 1/3, 1e-9),
    sprintf("engine=%.6f expected=%.6f", got5, 1/3))
chk("T5b NA unknown is excluded, not zeroed (n=60 not 80)", identical(as.integer(n5), 60L),
    sprintf("n=%s", n5))

## ------------------------------------------------ T6: 98 school years -> NA ---
S6 <- T5; S6$school_years <- 98; S6$age_first_birth <- 25
r6 <- run_engine(S6, "t6")
chk("T6 school_years=98 is not binned as 12+ (zero estimates rows)",
    is.null(r6$est) || nrow(r6$est) == 0,
    sprintf("rows=%s", if (is.null(r6$est)) "NULL" else nrow(r6$est)))

## ------------------------------------------------------- T7: malformed input ---
d7 <- T5; d7$weight[1] <- -1
f7 <- file.path(tempdir(), "bad.csv"); write.csv(schema(d7), f7, row.names = FALSE)
o7 <- file.path(tempdir(), "bad_out"); dir.create(o7, showWarnings = FALSE)
rc7 <- suppressWarnings(system2(RSCRIPT, c(shQuote(engine), shQuote(f7), shQuote(o7)),
                                stdout = TRUE, stderr = TRUE))
chk("T7 negative weight fails loudly", any(grepl("invalid weights", rc7)),
    paste(head(rc7, 1), collapse = ""))

## ---------------------------------------------- T8: determinism of the engine ---
r8a <- run_engine(S2, "t8a"); r8b <- run_engine(S2, "t8b")
chk("T8 repeated runs are identical", isTRUE(all.equal(r8a$est, r8b$est)), "")

## ---------------------------------------------------------------- report ------
cat(paste(LOG, collapse = "\n"), "\n\n")
cat(sprintf("TOTAL: %d passed, %d failed\n", PASS, FAIL))
if (FAIL > 0) quit(status = 1)
