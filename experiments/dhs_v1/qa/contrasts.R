#!/usr/bin/env Rscript
# contrasts.R -- design-based differences between domain means.
# A difference of two domain means from the SAME survey design is not
# independent: its variance needs the covariance, which svycontrast() on the
# svyby object provides. Reporting only per-group SEs would overstate the
# precision of every gap we quote.
#
# Usage: Rscript contrasts.R normalized.csv outdir

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Usage: Rscript contrasts.R normalized.csv outdir")
infile <- args[1]; outdir <- args[2]
suppressPackageStartupMessages(library(survey))
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
options(survey.lonely.psu = "fail")

d <- read.csv(infile, stringsAsFactors = FALSE, na.strings = c("", "NA"))
d$school_years[d$school_years %in% c(95,96,97,98,99)] <- NA
d$children_ever_born[d$children_ever_born %in% c(95,98,99)] <- NA
d$age_first_birth[!is.na(d$age_first_birth) & d$age_first_birth > 49 & d$age_first_birth != 99] <- NA
d$age_first_union[!is.na(d$age_first_union) & d$age_first_union > 49 & d$age_first_union != 99] <- NA
d$education <- ifelse(is.na(d$school_years), NA,
               ifelse(d$school_years < 6, "0-5",
               ifelse(d$school_years < 12, "6-11", "12+")))
d$early_birth <- ifelse(is.na(d$age_first_birth), NA, as.numeric(d$age_first_birth < 20))
d$early_union <- ifelse(is.na(d$age_first_union), NA, as.numeric(d$age_first_union < 20))

# experiment -> (record type, ages, outcome, grouping, contrast pair low->high)
S <- list(
  E1 = list(t="person", a=c(14,17), o="attendance",          g="wealth",   pair=c("1","5")),
  E2 = list(t="person", a=c(14,17), o="attendance",          g="urban",    pair=c("0","1")),
  E3 = list(t="person", a=c(14,17), o="attendance",          g="sex",      pair=c("1","2")),
  E4 = list(t="woman",  a=c(40,49), o="children_ever_born",  g="education",pair=c("0-5","12+")),
  E5 = list(t="woman",  a=c(25,34), o="early_birth",         g="education",pair=c("0-5","12+")),
  E6 = list(t="person", a=c(20,24), o="currently_in_school", g="urban",    pair=c("0","1"), female=TRUE),
  E7 = list(t="woman",  a=c(25,34), o="early_union",         g="education",pair=c("0-5","12+")),
  E8 = list(t="woman",  a=c(40,49), o="household_size",      g="education",pair=c("0-5","12+")))

out <- list()
for (key in names(S)) {
  sp <- S[[key]]
  for (cn in sort(unique(d$country))) for (w in sort(unique(d$wave[d$country==cn]))) {
    fr <- d[d$country==cn & d$wave==w & d$record_type==sp$t, , drop=FALSE]
    if (!nrow(fr)) next
    elig <- !is.na(fr$age) & fr$age>=sp$a[1] & fr$age<=sp$a[2]
    if (isTRUE(sp$female)) elig <- elig & fr$sex==2
    ok <- elig & !is.na(fr[[sp$o]]) & !is.na(fr[[sp$g]]) & fr$weight>0
    if (sum(ok) < 50) next
    fr$stratum <- as.factor(fr$stratum); fr$psu <- as.factor(fr$psu); fr$.dom <- ok
    r <- tryCatch({
      des <- svydesign(ids=~psu, strata=~stratum, weights=~weight, data=fr, nest=TRUE)
      sub <- subset(des, .dom)
      ans <- svyby(as.formula(paste0("~", sp$o)), as.formula(paste0("~", sp$g)),
                   sub, svymean, na.rm=TRUE, vartype="se")
      lev <- as.character(ans[[sp$g]])
      i <- match(sp$pair[1], lev); j <- match(sp$pair[2], lev)
      if (is.na(i) || is.na(j)) { list(ok=FALSE, why="contrast group level absent") } else {
        co <- svycontrast(ans, structure(c(1,-1), names=c(rownames(ans)[i], rownames(ans)[j])))
        list(ok=TRUE, est=as.numeric(co), se=as.numeric(SE(co)),
             m1=as.numeric(ans[[sp$o]][i]), m2=as.numeric(ans[[sp$o]][j]),
             n1=sum(ok & fr[[sp$g]]==sp$pair[1]), n2=sum(ok & fr[[sp$g]]==sp$pair[2]))
      }
    }, error=function(e) list(ok=FALSE, why=conditionMessage(e)))
    if (isTRUE(r$ok)) {
      out[[length(out)+1]] <- data.frame(experiment=key, country=cn, wave=w,
        contrast=sprintf("%s vs %s", sp$pair[2], sp$pair[1]),
        mean_ref=round(r$m1,4), mean_alt=round(r$m2,4),
        difference=round(r$est,4), se=round(r$se,4),
        lo95=round(r$est-1.96*r$se,4), hi95=round(r$est+1.96*r$se,4),
        z=round(r$est/r$se,3), p=round(2*pnorm(-abs(r$est/r$se)),6),
        n_ref=r$n1, n_alt=r$n2, stringsAsFactors=FALSE)
    } else {
      out[[length(out)+1]] <- data.frame(experiment=key, country=cn, wave=w,
        contrast=NA, mean_ref=NA, mean_alt=NA, difference=NA, se=NA, lo95=NA, hi95=NA,
        z=NA, p=NA, n_ref=NA, n_alt=NA, status=r$why, stringsAsFactors=FALSE)
    }
  }
}
C <- do.call(rbind, out)
if (!"status" %in% names(C)) C$status <- "ok"
C$p_holm <- NA_real_
for (f in unique(paste(C$experiment, C$country))) {
  i <- which(paste(C$experiment, C$country)==f & !is.na(C$p))
  if (length(i) > 1) C$p_holm[i] <- p.adjust(C$p[i], method="holm")
}
C$sig_holm_05 <- !is.na(C$p_holm) & C$p_holm < 0.05
C <- C[order(C$experiment, C$country, C$wave), ]
write.csv(C, file.path(outdir, "contrasts.csv"), row.names=FALSE)
cat("wrote", nrow(C), "contrasts\n")
print(C[!is.na(C$difference), c("experiment","country","wave","difference","se","z","p","p_holm")],
      row.names=FALSE, digits=3)
