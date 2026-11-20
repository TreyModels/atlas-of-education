#!/usr/bin/env bash
set -u
OUT="$(cd "$(dirname "$0")/.." && pwd)/raw/wdi"; mkdir -p "$OUT"
CTYS="CHN;HKG;KHM;PHL;KOR;JPN;VNM;THA;IDN;MYS;SGP;MMR;LAO;MNG;IND;BGD;PAK;LKA;NPL;TUR;MEX;BRA;EGY;NGA;KEN;ZAF;PER;COL;MAR;UKR"
for i in SE.PRM.TCHR SE.SEC.TCHR SE.PRM.ENRL SE.SEC.ENRL SE.TER.ENRL SE.XPD.PRIM.PC.ZS SE.XPD.SECO.PC.ZS SL.ISV.IFRM.ZS SL.EMP.SELF.ZS SP.POP.1564.TO.ZS NV.IND.MANF.ZS SE.PRM.CMPT.ZS SL.TLF.CACT.FE.ZS SE.XPD.TERT.PC.ZS; do
  f="$OUT/$i.json"; [ -s "$f" ] && continue
  curl -s --max-time 90 "https://api.worldbank.org/v2/country/$CTYS/indicator/$i?format=json&per_page=20000&date=1970:2024" -o "$f"
  echo "$i -> $(wc -c < "$f") bytes"; sleep 0.15
done
