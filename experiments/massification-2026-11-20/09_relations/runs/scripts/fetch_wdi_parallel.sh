#!/usr/bin/env bash
# Parallel WDI fetch in chunks of 10 countries (observed cells only). Idempotent: skips non-empty files.
set -u
OUT="$(cd "$(dirname "$0")/.." && pwd)/raw/wdi"; mkdir -p "$OUT"
G1="CHN;HKG;KHM;PHL;KOR;JPN;VNM;THA;IDN;MYS"
G2="SGP;MMR;LAO;MNG;IND;BGD;PAK;LKA;NPL;TUR"
G3="MEX;BRA;EGY;NGA;KEN;ZAF;PER;COL;MAR;UKR"
G4="CHN;HKG;KHM;PHL;KOR;JPN;VNM;THA;IDN;MYS;SGP;MMR;LAO;MNG;IND"
G5="BGD;PAK;LKA;NPL;TUR;MEX;BRA;EGY;NGA;KEN;ZAF;PER;COL;MAR;UKR"
IND="SE.XPD.TOTL.GD.ZS SE.XPD.TOTL.GB.ZS SE.PRM.ENRR SE.PRM.NENR SE.PRM.CMPT.ZS SE.SEC.ENRR SE.SEC.CMPT.LO.ZS SE.TER.ENRR SE.PRM.ENRL.TC.ZS SE.SEC.ENRL.TC.ZS SE.PRM.PRIV.ZS SE.SEC.PRIV.ZS SE.TER.PRIV.ZS SE.SEC.ENRL.VO.ZS SE.PRM.DURS SE.SEC.DURS SE.SEC.ENRR.UP SE.PRM.UNER.ZS SE.ADT.1524.LT.ZS NY.GDP.PCAP.KD NY.GDP.PCAP.PP.CD NY.GDP.MKTP.KD.ZG SP.URB.TOTL.IN.ZS SP.POP.TOTL SP.POP.0014.TO.ZS SP.DYN.TFRT.IN BX.TRF.PWKR.DT.GD.ZS SL.AGR.EMPL.ZS SL.UEM.1524.ZS SL.UEM.NEET.ZS GC.TAX.TOTL.GD.ZS GC.XPN.TOTL.GD.ZS IT.NET.USER.ZS SL.TLF.ACTI.1524.ZS SE.PRM.CUAT.ZS SE.SEC.CUAT.UP.ZS SE.TER.CUAT.BA.ZS SE.PRM.TCHR SE.SEC.TCHR SE.PRM.ENRL SE.SEC.ENRL SE.TER.ENRL SE.XPD.PRIM.PC.ZS SE.XPD.SECO.PC.ZS SL.ISV.IFRM.ZS SL.EMP.SELF.ZS SP.POP.1564.TO.ZS NV.IND.MANF.ZS SL.TLF.CACT.FE.ZS SE.XPD.TERT.PC.ZS"
export OUT
job() { # group indicator
  local g="$1" i="$2"
  local f="$OUT/${g##*;}.json"
  f="$OUT/$g.$i.json"
  [ -s "$f" ] && return 0
  curl -s --max-time 100 "https://api.worldbank.org/v2/country/$g/indicator/$i?format=json&per_page=20000&date=1970:2024" -o "$f"
}
export -f job
: > /tmp/joblist.txt 2>/dev/null || true
for i in $IND; do for k in 0 1 2; do echo "$i $k" ; done; done > "$OUT/.joblist"
cat "$OUT/.joblist" | while read -r i k; do
  case $k in 0) g=$G1;; 1) g=$G2;; 2) g=$G3;; esac
  echo "$g|$i"
done | xargs -P 8 -I{} bash -c 'g="${1%%|*}"; i="${1##*|}"; f="$OUT/$i.${g%%;*}.json"; [ -s "$f" ] || curl -s --max-time 100 "https://api.worldbank.org/v2/country/$g/indicator/$i?format=json&per_page=20000&date=1970:2024" -o "$f"' _ {}
echo DONE; ls "$OUT"/*.json | wc -l
