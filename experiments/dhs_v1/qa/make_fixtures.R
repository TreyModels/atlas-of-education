#!/usr/bin/env Rscript
# =====================================================================================================
# SYNTHETIC QA FIXTURES ONLY -- these are NOT real DHS data and must never be reported as results.
# Generated deterministically (no RNG except fixed cycling) for the methods/QA test harness.
# Every fixture row carries synthetic_fixture = "TRUE"; the fixtures README states the same.
# =====================================================================================================
args <- commandArgs(trailingOnly=TRUE)
outdir <- if (length(args)) args[1] else 'qa/fixtures'
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
base_cols <- c('country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth',
               'attendance','school_years','children_ever_born','age_first_birth','currently_in_school',
               'age_first_union','household_size','synthetic_fixture')

rbind_fix <- function(...) {
  dfs <- list(...)
  cols <- unique(unlist(lapply(dfs, names)))
  dfs <- lapply(dfs, function(d) { for (cc in setdiff(cols, names(d))) d[[cc]] <- NA; d[, cols, drop=FALSE] })
  do.call(rbind, dfs)
}
write_fix <- function(df, name) {
  for (cc in setdiff(base_cols, names(df))) df[[cc]] <- NA
  df$synthetic_fixture <- 'TRUE'
  df <- df[, c(base_cols, setdiff(names(df), base_cols)), drop=FALSE]
  write.csv(df, file.path(outdir, name), row.names=FALSE, na='')
}

mk <- function(n, country='FIXTURE', wave=2000) data.frame(country=country, wave=wave,
  stringsAsFactors=FALSE, row.names=seq_len(n))

# --------------------------------------------------------------------------------- fixture 1: known means
set.seed(1)
np <- 80; psu_ids <- rep(c('S1P1','S1P2','S2P1','S2P2'), each=20)
strata <- rep(c('S1','S1','S2','S2'), each=20)
persons <- data.frame(country='FIXTURE_KM', wave=2000, weight=1 + (seq_len(np) %% 3) * 0.5,
  stratum=strata, psu=psu_ids, record_type='person', age=rep(c(14,15,16,17), np/4),
  sex=rep(c(1,2), np/2), urban=rep(c(1,0), np/2), wealth=rep(1:5, np/5),
  stringsAsFactors=FALSE)
persons$attendance <- as.numeric(persons$weight >= 2)              # within-group mix: weighted mean != unweighted mean
persons$attendance[c(3, 26, 47, 61, 74, 79)] <- NA                 # item missingness (not by group)
persons$age[c(5, 70)] <- 13; persons$age[c(9, 66)] <- 18           # outside 14-17: must be excluded
persons$school_years <- NA; persons$children_ever_born <- NA; persons$age_first_birth <- NA
persons$currently_in_school <- NA; persons$age_first_union <- NA; persons$household_size <- NA

# women: 40-49 cohort (E4, E8); 25-34 (E5, E7); 20-24 (E6) spread over the same 4 PSUs
mk_women <- function(n, ages, country='FIXTURE_KM', wave=2000) {
  data.frame(country=country, wave=wave, weight=1 + (seq_len(n) %% 3) * 0.4,
    stratum=rep(c('S1','S1','S2','S2'), length.out=n), psu=rep(c('S1P1','S1P2','S2P1','S2P2'), length.out=n),
    record_type='woman', age=rep(ages, length.out=n), sex=2, urban=rep(c(1,0), length.out=n),
    wealth=rep(1:5, length.out=n), stringsAsFactors=FALSE)
}
w40 <- mk_women(60, 40:49)
w40$school_years <- rep(c(3, 8, 14), 20)                 # education groups 0-5 / 6-11 / 12+ (20 each)
w40$attendance <- NA; w40$currently_in_school <- NA
w40$children_ever_born <- c(2, 3, 4)[rep(1:3, 20)]       # E4 known means: 2, 3, 4
w40$household_size <- c(6, 5, 4)[rep(1:3, 20)]           # E8 known means: 6, 5, 4
w40$age_first_birth <- c(18, 24, 99)[rep(1:3, 20)]       # early-birth 1 / 0 / 0(never)
w40$age_first_union <- c(16, 22, 99)[rep(1:3, 20)]       # early-union 1 / 0 / 0(never)

w25 <- mk_women(60, 25:34)
w25$school_years <- rep(c(3, 8, 14), 20)
w25$children_ever_born <- c(1, 2, 2)[rep(1:3, 20)]
w25$household_size <- c(5, 4, 4)[rep(1:3, 20)]
w25$age_first_birth <- c(18, 21, 99)[rep(1:3, 20)]
w25$age_first_birth[c(2, 32, 44, 55, 58, 60)] <- NA      # 6 unknown -> stay unknown, excluded from E5 denominator
w25$age_first_union <- c(17, 22, 99)[rep(1:3, 20)]
w25$age_first_union[c(5, 35, 50)] <- NA
w25$attendance <- NA; w25$currently_in_school <- NA

w20 <- mk_women(55, 20:24)
w20$school_years <- rep(c(3, 8, 14), length.out=55)
w20$currently_in_school <- rep(c(1, 0, 1, 0, 1), 11)    # known pattern for E6
w20$currently_in_school[c(7, 21, 40)] <- NA               # item missingness (3)
w20$children_ever_born <- NA; w20$household_size <- NA; w20$age_first_birth <- NA; w20$age_first_union <- NA
w20$attendance <- NA

e6p <- data.frame(country='FIXTURE_KM', wave=2000, weight=1 + (seq_len(60) %% 3) * 0.5,
  stratum=rep(c('S1','S1','S2','S2'), length.out=60), psu=rep(c('S1P1','S1P2','S2P1','S2P2'), length.out=60),
  record_type='person', age=rep(c(20,21,22,23,24), 12), sex=2, urban=rep(c(1,0), 30),
  wealth=rep(1:5, 12), attendance=NA, school_years=NA, children_ever_born=NA, age_first_birth=NA,
  currently_in_school=rep(c(1,0,1,1,0), 12), age_first_union=NA, household_size=NA, stringsAsFactors=FALSE)
e6p$currently_in_school[c(4, 31, 52)] <- NA   # 3 unknown -> complete 57 (>=50)
known <- rbind_fix(persons, w40, w25, w20, e6p); known$synthetic_fixture <- 'TRUE'
write_fix(known, 'known_means.csv')

# --------------------------------------------------------------------------------- fixture 2: known design SE
n <- 80
se_fix <- data.frame(country='FIXTURE_SE', wave=2000, weight=1,
  stratum=rep('S1', n), psu=rep(c('P1','P2'), each=n/2), record_type='person',
  age=rep(14:17, n/4), sex=rep(c(1,2), n/2), urban=rep(c(1,0), n/2), wealth=rep(1:5, n/5),
  attendance=rep(c(1, 0), each=n/2), stringsAsFactors=FALSE)
# E2 by urban: each urban group has PSU means 1 (P1) and 0 (P2), equal sizes -> mean 0.5, se 0.5 exactly.
write_fix(se_fix, 'known_se.csv')

# --------------------------------------------------------------------------------- fixture 3: genuine lonely PSU in base design
lonely <- data.frame(country='FIXTURE_LONELY', wave=2000, weight=1,
  stratum=c(rep('S1', 40), rep('S2', 20)),
  psu=c(rep(c('S1P1','S1P2'), each=20), rep('S2P1', 20)),
  record_type='person', age=rep(c(14,15,16,17), 15), sex=rep(c(1,2), 30),
  urban=rep(c(1,0), 30), wealth=rep(1:5, 12), attendance=rep(c(1,0,1,0,1), 12),
  stringsAsFactors=FALSE)
write_fix(lonely, 'lonely_base.csv')

# --------------------------------------------------------------------------------- fixture 4: domain-only lonely PSU
# Base design (2 strata x 2 PSUs) is fine, but the E5/E7 domain (women 25-34) exists only in one PSU
# per stratum -> v1's subset(design, domain) collapses to one PSU per stratum => lonely PSU error.
dper <- data.frame(country='FIXTURE_DOMLONELY', wave=2000, weight=1,
  stratum=rep(c('S1','S1','S2','S2'), each=20),
  psu=rep(c('S1P1','S1P2','S2P1','S2P2'), each=20),
  record_type='person', age=rep(c(14,15,16,17), 20), sex=rep(c(1,2), 40),
  urban=rep(c(1,0), 40), wealth=rep(1:5, 16), attendance=rep(c(1,0,1,0,1), 16),
  stringsAsFactors=FALSE)
wdom <- data.frame(country='FIXTURE_DOMLONELY', wave=2000, weight=1,
  stratum=rep(c('S1','S2'), each=30), psu=rep(c('S1P1','S2P1'), each=30),
  record_type='woman', age=rep(25:34, 6), sex=2, urban=rep(c(1,0), 30), wealth=rep(1:5, 12),
  school_years=rep(c(3, 8, 14), 20),
  age_first_birth=rep(c(18, 21, 99), 20), age_first_union=rep(c(17, 22, 99), 20),
  children_ever_born=rep(c(1, 2, 2), 20), household_size=rep(c(5, 4, 4), 20),
  stringsAsFactors=FALSE)
w40dl <- data.frame(country='FIXTURE_DOMLONELY', wave=2000, weight=1,
  stratum=rep(c('S1','S1','S2','S2'), each=12), psu=rep(c('S1P1','S1P2','S2P1','S2P2'), each=12),
  record_type='woman', age=rep(40:49, length.out=48), sex=2, urban=rep(c(1,0), 24), wealth=rep(1:5, length.out=48),
  school_years=3, age_first_birth=99, age_first_union=99,
  children_ever_born=rep(c(2,3), 24), household_size=rep(c(5,4), 24),
  currently_in_school=NA, attendance=NA, stringsAsFactors=FALSE)
write_fix(rbind_fix(dper, wdom, w40dl), 'domain_lonely.csv')

# --------------------------------------------------------------------------------- fixture 5: missingness semantics
mw <- data.frame(country='FIXTURE_MISS', wave=2000, weight=1,
  stratum=rep('S1', 90), psu=rep(c('P1','P2'), each=45), record_type='woman',
  age=rep(25:34, 9), sex=2, urban=rep(c(1,0), 45), wealth=rep(1:5, 18),
  school_years=rep(c(3, 8, 14, 3, 8), 18),
  age_first_birth=rep(c(18, 25, 99), 30), age_first_union=rep(c(16, 22, 99), 30),
  children_ever_born=rep(c(2, 3, NA), 30), household_size=rep(c(5, 4, 4), 30),
  currently_in_school=NA, attendance=NA, stringsAsFactors=FALSE)
mw40 <- data.frame(country='FIXTURE_MISS', wave=2000, weight=1,
  stratum=rep('S1', 90), psu=rep(c('P1','P2'), each=45), record_type='woman',
  age=rep(40:49, 9), sex=2, urban=rep(c(1,0), 45), wealth=rep(1:5, 18),
  school_years=rep(c(3, 8, 14), 30),
  children_ever_born=rep(c(2, 3, NA), 30),   # E4: group 0-5 mean 2, group 6-11 mean 3, group 12+ all missing
  household_size=rep(c(6, 5, 4), 30), age_first_birth=99, age_first_union=99,
  currently_in_school=NA, attendance=NA, stringsAsFactors=FALSE)
mw <- rbind_fix(mw, mw40)
# E5 true mean: early_birth values: 18->1, 25->0, 99->0 (never, NOT unknown) -> mean (1+0+0)/3 = 1/3.
# E4 true mean excludes NA CEV: (2+3)/2 = 2.5.
write_fix(mw, 'missingness.csv')

# --------------------------------------------------------------------------------- fixture 6: small cells / suppression
sc <- data.frame(country='FIXTURE_SMALL', wave=2000, weight=1,
  stratum=rep('S1', 154), psu=rep(c('P1','P2'), each=77), record_type='person',
  age=rep(14:17, length.out=154), sex=rep(c(1,2), 77), urban=rep(c(1,0), 77),
  wealth=c(rep(1, 50), rep(2, 40), rep(3, 30), rep(4, 30), rep(5, 4)),
  attendance=rep(c(1,0,1,0,1), length.out=154), stringsAsFactors=FALSE)
write_fix(sc, 'small_cells.csv')

# --------------------------------------------------------------------------------- fixture 7: record-type weights
rw_p <- data.frame(country='FIXTURE_WT', wave=2000, weight=1, weight_variable='person_weight',
  stratum=rep('S1', 80), psu=rep(c('P1','P2'), each=40), record_type='person',
  age=rep(14:17, 20), sex=rep(c(1,2), 40), urban=rep(c(1,0), 40), wealth=rep(1:5, 16),
  attendance=rep(c(1,0,1,0,1), 16), stringsAsFactors=FALSE)
rw_w <- data.frame(country='FIXTURE_WT', wave=2000, weight=1 + (seq_len(60) %% 3) * 2, weight_variable='woman_weight',
  stratum=rep('S1', 60), psu=rep(c('P1','P2'), each=30), record_type='woman',
  age=rep(40:49, 6), sex=2, urban=rep(c(1,0), 30), wealth=rep(1:5, 12),
  school_years=rep(c(3, 8, 14), 20),
  children_ever_born=NA, household_size=c(6, 5, 4)[rep(1:3, 20)],
  age_first_birth=99, age_first_union=99, currently_in_school=NA, attendance=NA,
  stringsAsFactors=FALSE)
rw_w$weight <- ifelse(seq_len(nrow(rw_w)) %% 2 == 0, 5, 1)     # unequal weights by parity
rw_w$children_ever_born <- ifelse(seq_len(nrow(rw_w)) %% 2 == 0, 5, 2)  # outcome correlated with weight
write_fix(rbind_fix(rw_p, rw_w), 'record_weight_ok.csv')
bad_wv <- rbind_fix(rw_p, rw_w); bad_wv$weight_variable[bad_wv$record_type == 'person'] <- 'woman_weight'
write_fix(bad_wv, 'bad_weightvar_same.csv')

# --------------------------------------------------------------------------------- fixture 8: domain-definition boundaries
# Persons: 120 rows, 30 each of ages 13 (excluded), 14/17 (included), 18 (excluded).
defs_p <- data.frame(country='FIXTURE_DEFS', wave=2000, weight=1,
  stratum=rep('S1', 120), psu=rep(c('P1','P2'), each=60), record_type='person',
  age=rep(c(13, 14, 17, 18), 30), sex=rep(c(1,2), 60), urban=rep(c(1,0), 60),
  wealth=rep(1:5, 24), attendance=1, stringsAsFactors=FALSE)
defs_p$school_years <- NA
# Women cohorts: 60 rows each for the README cohorts, with ONLY boundary ages (20/24, 25/34, 40/49)
mk_cohort <- function(ages, n=60) data.frame(country='FIXTURE_DEFS', wave=2000, weight=1,
  stratum=rep('S1', n), psu=rep(c('P1','P2'), each=n/2), record_type='woman', sex=2,
  age=rep(ages, length.out=n), urban=rep(c(1,0), n/2), wealth=rep(1:5, n/5), stringsAsFactors=FALSE)
c40 <- mk_cohort(c(40, 49)); c40$school_years <- rep(c(5, 6, 11, 12), 15)
c40$children_ever_born <- rep(c(2, 3, 4, 5), 15); c40$household_size <- rep(c(6, 5, 4, 3), 15)
c40$age_first_birth <- 99; c40$age_first_union <- 99; c40$currently_in_school <- NA; c40$attendance <- NA
c25 <- mk_cohort(c(25, 34)); c25$school_years <- rep(c(5, 6, 11, 12), 15)
c25$children_ever_born <- rep(c(1, 2, 2, 2), 15); c25$household_size <- rep(c(5, 4, 4, 4), 15)
c25$age_first_birth <- rep(c(19, 20, 99, 20), 15)   # 19 = early, 20 = not early, 99 = never
c25$age_first_union <- rep(c(19, 20, 99, 20), 15)
c25$currently_in_school <- NA; c25$attendance <- NA
c20 <- mk_cohort(c(20, 24)); c20$school_years <- rep(c(5, 6, 11, 12), 15)
c20$children_ever_born <- NA; c20$household_size <- NA; c20$age_first_birth <- NA; c20$age_first_union <- NA
c20$currently_in_school <- rep(c(1, 0), 30); c20$attendance <- NA
# Exclusion rows: women aged 19/35/39/50 (must be excluded from every woman cohort)
defs_x <- data.frame(country='FIXTURE_DEFS', wave=2000, weight=1,
  stratum=rep('S1', 8), psu=rep(c('P1','P2'), 4), record_type='woman', sex=2,
  age=c(19, 35, 39, 50, 19, 35, 39, 50), urban=rep(c(1,0), 4), wealth=1,
  school_years=8, children_ever_born=2, household_size=4, age_first_birth=18,
  age_first_union=18, currently_in_school=1, attendance=NA, stringsAsFactors=FALSE)
defs_e6 <- data.frame(country='FIXTURE_DEFS', wave=2000, weight=1,
  stratum=rep('S1', 60), psu=rep(c('P1','P2'), each=30), record_type='person', sex=2,
  age=rep(c(20, 24), 30), urban=rep(c(1,0), 30), wealth=rep(1:5, 12), attendance=NA,
  school_years=NA, children_ever_born=NA, age_first_birth=NA, age_first_union=NA, household_size=NA,
  currently_in_school=rep(c(1, 0), 30), stringsAsFactors=FALSE)
write_fix(rbind_fix(defs_p, c40, c25, c20, defs_x, defs_e6), 'domain_defs.csv')

# --------------------------------------------------------------------------------- fixture 9: two countries x two waves
two <- rbind(
  transform(persons[1:40, ], country='FIXTURE_C1', wave=2000),
  transform(persons[1:40, ], country='FIXTURE_C1', wave=2001),
  transform(persons[1:40, ], country='FIXTURE_C2', wave=2000))
write_fix(two, 'two_countries_waves.csv')

# --------------------------------------------------------------------------------- fixture 10: bad-input variants
good <- known[1:120, ]
corrupt <- function(name, expr) { x <- good; x <- expr(x); write_fix(x, name) }
corrupt('bad_inf_weight.csv',   function(x) { x$weight[1] <- Inf; x })
corrupt('bad_zero_weight.csv',  function(x) { x$weight[1] <- 0; x })
corrupt('bad_sex.csv',          function(x) { x$sex[1] <- 3; x })
corrupt('bad_school99.csv',     function(x) { x$school_years[1] <- 99; x })
corrupt('bad_cev99.csv',        function(x) { x$children_ever_born[1] <- 99; x })
corrupt('bad_age120.csv',       function(x) { x$age[1] <- 120; x })
corrupt('bad_union97.csv',      function(x) { x$age_first_union[1] <- 97; x })
corrupt('bad_wealth6.csv',      function(x) { x$wealth[1] <- 6; x })
corrupt('bad_urban2.csv',       function(x) { x$urban[1] <- 2; x })
{ x <- good; x$sex <- NULL; write.csv(x, file.path(outdir, 'bad_missing_col.csv'), row.names=FALSE, na='') }
corrupt('bad_stratum_na.csv',   function(x) { x$stratum[1] <- NA; x })
corrupt('bad_psu_na.csv',       function(x) { x$psu[1] <- NA; x })
corrupt('bad_recordtype.csv',   function(x) { x$record_type[1] <- 'child'; x })
corrupt('bad_psu_cross_stratum.csv', function(x) { x$stratum[2] <- 'S2'; x$psu[2] <- x$psu[1]; x })
corrupt('bad_stratum_empty.csv', function(x) { x$stratum[1] <- ''; x })

# --------------------------------------------------------------------------------- fixture 11: benchmarks
km <- read.csv(file.path(outdir, 'known_means.csv'), stringsAsFactors=FALSE, na.strings=c('', 'NA'))
exp_mean <- function(df, out) weighted.mean(df[[out]], df$weight, na.rm=TRUE)
b_ok <- data.frame(experiment='E1', country='FIXTURE_KM', wave=2000, group='5',
  benchmark=exp_mean(km[km$record_type=='person' & km$age %in% 14:17 & !is.na(km$attendance) & km$wealth==5, ], 'attendance'),
  tolerance=0.01, source='SYNTHETIC FIXTURE', citation='not a real benchmark; fixture only',
  stringsAsFactors=FALSE)
b_bad <- b_ok; b_bad$group <- '4'; b_bad$benchmark <- 0.99
write.csv(b_ok, file.path(outdir, 'benchmarks_ok.csv'), row.names=FALSE)
write.csv(b_bad, file.path(outdir, 'benchmarks_bad.csv'), row.names=FALSE)

# --------------------------------------------------------------------------------- fixture 12: adapter metadata
meta <- data.frame(key=c('country','wave','release','record_type','weight_variable','strata_variable',
                         'psu_variable','missing_codes','approved_access'),
                   value=c('FIXTURE_KM','2000','FIXTURE-RELEASE','person+woman','person_weight/woman_weight',
                           'stratum','psu','NA=unknown; 99=verified never','SYNTHETIC FIXTURE ONLY - not real data'),
                   stringsAsFactors=FALSE)
write.csv(meta, file.path(outdir, 'metadata_ok.csv'), row.names=FALSE)
write.csv(meta[meta$key != 'approved_access', ], file.path(outdir, 'metadata_missing_key.csv'), row.names=FALSE)

writeLines(c(
  '# QA FIXTURES -- SYNTHETIC ONLY',
  '',
  'Every CSV in this directory is synthetic fixture data generated by `make_fixtures.R` for the',
  'methods/QA test harness. **None of these values are real DHS data and none may be reported as a',
  'result.** Each row carries `synthetic_fixture = "TRUE"` and country codes are prefixed `FIXTURE`.',
  '',
  'Purpose: known-answer tests of the analysis engine (survey-weighted means, design SEs, lonely PSU',
  'behaviour, missingness semantics, domain estimation, suppression, multiplicity reporting, schema',
  'enforcement, record-type weights, benchmark machinery).',
  '',
  'Real-data benchmark verification is BLOCKED in this worktree: no DHS microdata or adapter exists',
  '(harmonize/ is empty). See ../QA_REPORT.md for the sign-off status.'), file.path(outdir, 'README.md'))
note <- function(...) cat(..., '\n', sep='')
note('wrote fixtures to ', outdir)
