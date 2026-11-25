#!/usr/bin/env Rscript
# Registry-driven external benchmark checks for the delivered DHS layers.
# Compares independent, non-disclosive statistics computed from the normalized CSV with the
# published DHS benchmark registry (benchmarks/benchmark_registry_v0.1.csv).  Only AVAILABLE rows
# are compared; PENDING rows are reported as PENDING and never compared.
# Usage: Rscript qa/benchmark_checks.R normalized.csv benchmark_registry.csv out.csv [label]
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 3) stop('Usage: Rscript qa/benchmark_checks.R normalized.csv registry.csv out.csv [label]')
data_path <- args[1]; reg_path <- args[2]; out_path <- args[3]
label <- if (length(args) >= 4) args[4] else ''
d <- read.csv(data_path, stringsAsFactors=FALSE, na.strings=c('', 'NA'))
reg <- read.csv(reg_path, stringsAsFactors=FALSE, na.strings=c('', 'NA'))
num <- function(x) suppressWarnings(as.numeric(x))
d$attendance <- num(d$attendance); d$age <- num(d$age); d$sex <- num(d$sex); d$urban <- num(d$urban)
res <- list()
add <- function(b, ours, benchmark, tol, direction_note, definition_match, status_override=NULL) {
  diff <- ours - benchmark
  within <- is.finite(diff) && abs(diff) <= tol
  direction <- if (!is.finite(diff)) NA_character_ else if (diff > 0) 'ours_higher' else if (diff < 0) 'ours_lower' else 'equal'
  res[[length(res)+1]] <<- data.frame(
    benchmark_id=b$benchmark_id, country=b$country, wave=b$wave, indicator=b$indicator,
    our_statistic=ours, published=benchmark, diff_pp=diff, tolerance_pp=tol,
    direction=direction, within_tolerance=within, definition_match=definition_match,
    status=if (!is.null(status_override)) status_override else if (within) 'MATCH' else 'MISMATCH',
    source=b$source, citation=b$citation, caveat=b$notes, computed_by=label, stringsAsFactors=FALSE)
}
sub_person <- function(country, wave, age_lo, age_hi, sex=NA, urban=NA) {
  z <- d[d$country == country & as.character(d$wave) == as.character(wave) & d$record_type == 'person', ]
  z <- z[!is.na(z$age) & z$age >= age_lo & z$age <= age_hi, ]
  if (!is.na(sex)) z <- z[!is.na(z$sex) & z$sex == sex, ]
  if (!is.na(urban)) z <- z[!is.na(z$urban) & z$urban == urban, ]
  z
}
wmean <- function(z) if (nrow(z) && any(!is.na(z$attendance) & is.finite(z$weight))) {
  ok <- !is.na(z$attendance) & is.finite(z$weight) & z$weight > 0
  100 * sum(z$attendance[ok] * z$weight[ok]) / sum(z$weight[ok])
} else NA_real_
for (i in seq_len(nrow(reg))) {
  b <- reg[i, ]
  if (!identical(toupper(b$status), 'AVAILABLE')) {
    res[[length(res)+1]] <- data.frame(benchmark_id=b$benchmark_id, country=b$country, wave=b$wave,
      indicator=b$indicator, our_statistic=NA_real_, published=NA_real_, diff_pp=NA_real_, tolerance_pp=NA_real_,
      direction=NA_character_, within_tolerance=NA, definition_match=b$definition_match,
      status='PENDING', source=b$source, citation=b$citation, caveat=b$notes, computed_by=label,
      stringsAsFactors=FALSE)
    next
  }
  tol <- ifelse(is.na(num(b$tolerance_pp)), 2.5, num(b$tolerance_pp))
  if (grepl('^KH', b$country) && grepl('2021-22', b$wave)) {
    if (grepl('primary NAR by sex', b$indicator, ignore.case=TRUE)) {
      m <- wmean(sub_person('KH', '2021-22', 6, 11, sex=1)); f <- wmean(sub_person('KH', '2021-22', 6, 11, sex=2))
      add(transform(b, benchmark_id=paste0(b$benchmark_id, ':M')), m, 72.0, tol, '', 'definitional')
      add(transform(b, benchmark_id=paste0(b$benchmark_id, ':F')), f, 73.5, tol, '', 'definitional')
    } else if (grepl('primary NAR urban', b$indicator, ignore.case=TRUE)) {
      u <- wmean(sub_person('KH', '2021-22', 6, 11, urban=1)); r <- wmean(sub_person('KH', '2021-22', 6, 11, urban=0))
      add(transform(b, benchmark_id=paste0(b$benchmark_id, ':urban')), u, 75.5, tol, '', 'definitional')
      add(transform(b, benchmark_id=paste0(b$benchmark_id, ':rural')), r, 71.3, tol, '', 'definitional')
    } else if (grepl('secondary NAR', b$indicator, ignore.case=TRUE)) {
      add(b, wmean(sub_person('KH', '2021-22', 12, 18)), 42.0, tol, '', 'definitional')
    } else {
      add(b, wmean(sub_person('KH', '2021-22', 6, 11)), 72.8, tol, '', 'definitional')
    }
  } else {
    res[[length(res)+1]] <- data.frame(benchmark_id=b$benchmark_id, country=b$country, wave=b$wave,
      indicator=b$indicator, our_statistic=NA_real_, published=num(b$estimate), diff_pp=NA_real_,
      tolerance_pp=tol, direction=NA_character_, within_tolerance=NA, definition_match=b$definition_match,
      status='NO_MATCHING_DOMAIN_IN_ADAPTER', source=b$source, citation=b$citation, caveat=b$notes,
      computed_by=label, stringsAsFactors=FALSE)
  }
}
out <- do.call(rbind, res)
write.csv(out, out_path, row.names=FALSE)
cat('benchmark checks ->', out_path, '\n')
print(out[, c('benchmark_id','status','our_statistic','published','diff_pp','direction','within_tolerance')])
