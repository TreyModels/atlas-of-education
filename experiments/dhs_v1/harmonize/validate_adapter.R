#!/usr/bin/env Rscript
# Adapter / aggregate cross-validation with the binding engine's survey stack.
#   Rscript harmonize/validate_adapter.R <normalized.csv> [experiment] [country] [wave]
# Checks the experiments.R schema on a LOCAL normalized.csv (no raw microdata) and recomputes ONE domain mean
# with survey::svydesign/svyby so the Python aggregate_layer can be compared against R survey.  No restricted
# microdata is written; the script only prints non-disclosive design summaries/estimates.
suppressPackageStartupMessages(library(survey))
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 1) stop('Usage: Rscript validate_adapter.R <normalized.csv> [experiment] [country] [wave]')
d <- read.csv(args[1], stringsAsFactors=FALSE, na.strings=c('', 'NA', 'NaN'))
required <- c('country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth',
              'attendance','school_years','children_ever_born','age_first_birth','currently_in_school',
              'age_first_union','household_size')
miss <- setdiff(required, names(d))
cat(sprintf('INTERPRETER %s | survey %s | rows %d\n', R.version.string,
            as.character(packageVersion('survey')), nrow(d)))
if (length(miss)) { cat('SCHEMA_MISSING:', paste(miss, collapse=','), '\n'); quit(status=1) }
cat('SCHEMA_OK\n')
stopifnot(all(is.na(d$weight) | d$weight > 0))
stopifnot(all(is.na(d$wealth) | d$wealth %in% 1:5))
for (n in c('attendance','currently_in_school','urban')) stopifnot(all(is.na(d[[n]]) | d[[n]] %in% 0:1))
cat(sprintf('DESIGN_KEYS weight_nonpos=%d stratum_na=%d psu_na=%d psu_stratum_dups=%d\n',
            sum(!is.na(d$weight) & d$weight <= 0), sum(is.na(d$stratum)), sum(is.na(d$psu)),
            sum(duplicated(d[c('stratum','psu')]))))
d$education <- ifelse(is.na(d$school_years), NA,
                ifelse(d$school_years < 6, '0-5', ifelse(d$school_years < 12, '6-11', '12+')))
d$early_birth <- ifelse(is.na(d$age_first_birth), NA, as.numeric(d$age_first_birth < 20))
d$early_union <- ifelse(is.na(d$age_first_union), NA, as.numeric(d$age_first_union < 20))
exp <- if (length(args) >= 2) args[2] else 'E1'
cn  <- if (length(args) >= 3) args[3] else d$country[1]
wv  <- if (length(args) >= 4) args[4] else d$wave[1]
specs <- list(
 E1=list(type='person', lo=14, hi=17, out='attendance', group='wealth'),
 E2=list(type='person', lo=14, hi=17, out='attendance', group='urban'),
 E3=list(type='person', lo=14, hi=17, out='attendance', group='sex'),
 E4=list(type='woman',  lo=40, hi=49, out='children_ever_born', group='education'),
 E5=list(type='woman',  lo=25, hi=34, out='early_birth', group='education'),
 E6=list(type='person', lo=20, hi=24, out='currently_in_school', group='urban'),
 E7=list(type='woman',  lo=25, hi=34, out='early_union', group='education'),
 E8=list(type='woman',  lo=40, hi=49, out='household_size', group='education'))
sp <- specs[[exp]]
z <- d[d$country == cn & d$wave == wv & d$record_type == sp$type, ]
if (exp == 'E6') z <- z[!is.na(z$sex) & z$sex == 2, ]
idx <- !is.na(z$age) & z$age >= sp$lo & z$age <= sp$hi & !is.na(z[[sp$out]]) & !is.na(z[[sp$group]])
cat(sprintf('DOMAIN %s %s/%s n=%d complete=%d\n', exp, cn, wv, nrow(z), sum(idx)))
z$domain <- idx
z$stratum <- as.factor(z$stratum); z$psu <- as.factor(z$psu)
design <- svydesign(ids=~psu, strata=~stratum, weights=~weight, data=z, nest=TRUE)
sub <- subset(design, domain)
ans <- svyby(as.formula(paste0('~', sp$out)), as.formula(paste0('~', sp$group)), sub, svymean, na.rm=TRUE, vartype='se')
print(ans)
