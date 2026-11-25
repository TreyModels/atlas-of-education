#!/usr/bin/env Rscript
# validate_benchmarks.R -- real-data validation of adapter + engine against the
# prior Cambodia attendance series (research/cambodia-dhs, itself anchored to the
# DHS 2021-22 final report Table 2.12). Two prior variants exist and are compared
# separately: "current" (HV121==1 OR (HV121==2 AND HV122>0)) and
# "any_current_year" (HV121 in {1,2}).
suppressPackageStartupMessages(library(survey))
dir <- Sys.getenv("DHS_NORM_DIR", path.expand("~/neon-boot/dhs8_local/normalized"))
P <- data.frame(
 wave=c(rep("2000",3),rep("2005",3),rep("2010",3),rep("2014",3),rep("2021-22",3)),
 age =rep(c("6-11","12-14","15-17"),5),
 cur =c(66.622,77.771,41.985,74.484,89.071,60.42,87.972,86.105,53.804,86.583,83.485,46.844,69.243,72.011,51.124),
 any =c(66.622,77.771,41.985,76.723,89.148,60.441,90.43,86.11,53.804,90.361,83.485,46.844,74.654,72.013,51.124))
rows <- list()
for (w in unique(P$wave)) {
  d <- read.csv(file.path(dir, sprintf("KH-%s_person.csv", w)), stringsAsFactors = FALSE)
  d <- d[!is.na(d$attendance) & !is.na(d$age) & d$age>=6 & d$age<=17, ]
  d$stratum<-as.factor(d$stratum); d$psu<-as.factor(d$psu)
  d$ag <- ifelse(d$age<=11,"6-11",ifelse(d$age<=14,"12-14","15-17"))
  des <- svydesign(ids=~psu,strata=~stratum,weights=~weight,data=d,nest=TRUE)
  m <- svyby(~attendance,~ag,des,svymean,vartype="se")
  for(i in seq_len(nrow(m))) rows[[length(rows)+1]] <-
    data.frame(wave=w, age=as.character(m$ag[i]), ours=100*as.numeric(m$attendance[i]),
               ours_se=100*as.numeric(m$se[i]))
}
C <- merge(P, do.call(rbind,rows), by=c("wave","age"))
C$d_cur <- C$ours-C$cur; C$d_any <- C$ours-C$any
C <- C[order(C$wave,C$age),]
print(C[,c("wave","age","cur","any","ours","d_cur","d_any")], row.names=FALSE, digits=2)
cat(sprintf("\nvs 'any_current_year': max|delta|=%.3f pp, max|delta|/se=%.3f  (n=%d)\n",
            max(abs(C$d_any)), max(abs(C$d_any)/C$ours_se), nrow(C)))
cat(sprintf("vs 'current'         : max|delta|=%.3f pp  (confined to ages 6-11: %s)\n",
            max(abs(C$d_cur)), all(abs(C$d_cur[C$age!="6-11"])<0.2)))
cat(sprintf("ages 12-17 vs 'any'  : max|delta|=%.3f pp\n", max(abs(C$d_any[C$age!="6-11"]))))
