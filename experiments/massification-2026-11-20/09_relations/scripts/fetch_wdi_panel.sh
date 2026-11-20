#!/usr/bin/env bash
# Fetch a wide WDI panel for relation estimation. Observed cells only; no imputation.
set -u
OUT="$(cd "$(dirname "$0")/.." && pwd)/raw/wdi"
mkdir -p "$OUT"
CTYS="CHN;HKG;KHM;PHL;KOR;JPN;VNM;THA;IDN;MYS;SGP;MMR;LAO;MNG;IND;BGD;PAK;LKA;NPL;TUR;MEX;BRA;EGY;NGA;KEN;ZAF;PER;COL;MAR;UKR"
IND="SE.XPD.TOTL.GD.ZS,SE.XPD.TOTL.GB.ZS,SE.PRM.ENRR,SE.PRM.NENR,SE.PRM.CMPT.ZS,SE.SEC.ENRR,SE.SEC.CMPT.LO.ZS,SE.TER.ENRR,SE.PRM.ENRL.TC.ZS,SE.SEC.ENRL.TC.ZS,SE.PRM.PRIV.ZS,SE.SEC.PRIV.ZS,SE.TER.PRIV.ZS,SE.SEC.ENRL.VO.ZS,SE.PRM.DURS,SE.SEC.DURS,SE.SEC.ENRR.UP,SE.PRM.UNER.ZS,SE.ADT.1524.LT.ZS"
IND2="NY.GDP.PCAP.KD,NY.GDP.PCAP.PP.CD,NY.GDP.MKTP.KD.ZG,SP.URB.TOTL.IN.ZS,SP.POP.TOTL,SP.POP.0014.TO.ZS,SP.DYN.TFRT.IN,BX.TRF.PWKR.DT.GD.ZS,SL.AGR.EMPL.ZS,SL.UEM.1524.ZS,SL.UEM.NEET.ZS,GC.TAX.TOTL.GD.ZS,GC.XPN.TOTL.GD.ZS,IT.NET.USER.ZS,SL.TLF.ACTI.1524.ZS,SE.PRM.CUAT.ZS,SE.SEC.CUAT.UP.ZS,SE.TER.CUAT.BA.ZS"
for i in $(echo "$IND,$IND2" | tr ',' ' '); do
  f="$OUT/$i.json"
  [ -s "$f" ] && continue
  curl -s --max-time 90 "https://api.worldbank.org/v2/country/$CTYS/indicator/$i?format=json&per_page=20000&date=1970:2024" -o "$f"
  n=$(wc -c < "$f")
  echo "$i -> $n bytes"
  sleep 0.15
done
