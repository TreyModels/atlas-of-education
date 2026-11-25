#!/usr/bin/env Rscript
# Exploratory survey-weighted descriptive contrasts; input must be independently harmonized.
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=2) stop('Usage: Rscript experiments.R normalized.csv output_dir')
if (!requireNamespace('survey', quietly=TRUE)) stop('Install R package survey')
dir.create(args[2], recursive=TRUE, showWarnings=FALSE)
d <- read.csv(args[1], stringsAsFactors=FALSE, na.strings=c('', 'NA'))
required <- c('country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth','attendance','school_years','children_ever_born','age_first_birth','currently_in_school','age_first_union','household_size')
missing <- setdiff(required,names(d)); if(length(missing)) stop(paste('Missing schema columns:',paste(missing,collapse=', ')))
if(any(is.na(d$country)|is.na(d$wave)|is.na(d$record_type)|is.na(d$weight)|d$weight<=0|is.na(d$stratum)|is.na(d$psu))) stop('Missing survey keys or invalid weights')
if(any(!d$record_type %in% c('person','woman'))) stop('Invalid record_type')
if(any(!is.na(d$wealth)&!d$wealth %in% 1:5)) stop('Wealth must be 1:5')
for(n in c('attendance','currently_in_school','urban')) if(any(!is.na(d[[n]]) & !d[[n]] %in% 0:1)) stop(paste(n,'must be 0/1'))
options(survey.lonely.psu='fail')
specs <- list(
 E1=list(type='person',ages=c(14,17),out='attendance',group='wealth',desc='Adolescent attendance by wealth'),
 E2=list(type='person',ages=c(14,17),out='attendance',group='urban',desc='Adolescent attendance by residence'),
 E3=list(type='person',ages=c(14,17),out='attendance',group='sex',desc='Adolescent attendance by sex'),
 E4=list(type='woman',ages=c(40,49),out='children_ever_born',group='education',desc='Completed-cohort children ever born by schooling'),
 E5=list(type='woman',ages=c(25,34),out='early_birth',group='education',desc='Birth before age 20 by schooling'),
 E6=list(type='woman',ages=c(20,24),out='currently_in_school',group='urban',desc='School participation among young women by residence'),
 E7=list(type='woman',ages=c(25,34),out='early_union',group='education',desc='Union before age 20 by schooling'),
 E8=list(type='woman',ages=c(40,49),out='household_size',group='education',desc='Current household size among older women by schooling'))
d$education <- ifelse(is.na(d$school_years),NA,ifelse(d$school_years<6,'0-5',ifelse(d$school_years<12,'6-11','12+')))
# age_first_birth and age_first_union: NA = unknown; use 99 for verified never.
d$early_birth <- ifelse(is.na(d$age_first_birth),NA,as.numeric(d$age_first_birth<20))
d$early_union <- ifelse(is.na(d$age_first_union),NA,as.numeric(d$age_first_union<20))
results <- list(); status <- list(); k<-0; s<-0
for(key in names(specs)) for(cn in unique(d$country)) for(w in unique(d$wave[d$country==cn])) {
 sp<-specs[[key]]; z<-d[d$country==cn & d$wave==w & d$record_type==sp$type,,drop=FALSE]
 idx<-!is.na(z$age)&z$age>=sp$ages[1]&z$age<=sp$ages[2]&!is.na(z[[sp$out]])&!is.na(z[[sp$group]])
 s<-s+1; msg<-'ok'
 if(sum(idx)<50 || length(unique(z[[sp$group]][idx]))<2) msg<-'insufficient complete cases or groups'
 if(msg=='ok') {
   # Keep full design before subsetting so domain variance uses all PSUs.
   z$domain<-idx; z$stratum<-as.factor(z$stratum); z$psu<-as.factor(z$psu)
   tryCatch({
    design<-survey::svydesign(ids=~psu,strata=~stratum,weights=~weight,data=z,nest=TRUE)
    sub<-subset(design,domain)
    form<-as.formula(paste0('~',sp$out)); grp<-as.formula(paste0('~',sp$group))
    ans<-survey::svyby(form,grp,sub,survey::svymean,na.rm=TRUE,vartype='se')
    for(j in seq_len(nrow(ans))) { k<-k+1; est<-as.numeric(ans[j,2]); se<-as.numeric(ans[j,3]); results[[k]]<-data.frame(experiment=key,country=cn,wave=w,group=as.character(ans[j,1]),estimate=est,se=se,lo=est-1.96*se,hi=est+1.96*se,complete_n=sum(idx & z[[sp$group]]==ans[j,1],na.rm=TRUE),description=sp$desc) }
   },error=function(e) {msg<<-paste('design error:',conditionMessage(e))})
 }
 status[[s]]<-data.frame(experiment=key,country=cn,wave=w,complete_n=sum(idx),status=msg)
}
write.csv(if(length(results)) do.call(rbind,results) else data.frame(),file.path(args[2],'estimates.csv'),row.names=FALSE)
write.csv(do.call(rbind,status),file.path(args[2],'status.csv'),row.names=FALSE)
writeLines(capture.output(sessionInfo()),file.path(args[2],'session_info.txt'))
