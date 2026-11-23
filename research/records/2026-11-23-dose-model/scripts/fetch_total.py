"""Fetch both-sex Barro-Lee shares and populations (male = total minus female)."""
import json, sys
sys.argv = [sys.argv[0], sys.argv[1]]
exec(open("fetch_data.py").read().split("res = {}")[0])
res = {}
for a in ["1519", "2024", "2529"]:
    for k in ["NOED.%s.ZS", "PRM.ICMP.%s.ZS", "PRM.CMPT.%s.ZS", "SEC.ICMP.%s.ZS", "SEC.CMPT.%s.ZS", "TER.ICMP.%s.ZS", "TER.CMPT.%s.ZS", "POP.%s", "UCMP"]:
        if k == "UCMP":
            for l in ["PRM", "SEC", "TER"]:
                ind = f"BAR.{l}.UCMP.{a}.ZS"; res[ind] = get(ind)
            continue
        kk = k % a; ind = "BAR." + kk
        res[ind] = get(ind)
json.dump(res, open(f"{OUT}/wb_total.json", "w")); print("done")
