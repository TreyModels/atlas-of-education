#!/usr/bin/env python3
"""Generate all figures for the four working papers."""
import json, os, gzip
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.bbox": "tight"})


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
V = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
     for k in ["fertility", "ter", "sec", "lsc", "prm_cmp", "wage_emp", "electricity",
               "urban", "gdppc_log", "u5mr", "life_exp", "flfp", "emp_agri", "agri_va"]}


def save(fig, name):
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)
    print("wrote", name)


# ---------- fig01: chain vs common cause ----------
rng = np.random.default_rng(1)
chain = rng.normal(2.201, (2.885 - 2.201) / 3.29, 1200)
common = rng.normal(0.000, (0.255 + 0.260) / 3.29, 1200)
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.hist(common, bins=40, color="#9bb7d4", alpha=.85, label="common cause (no chain)")
ax.hist(chain, bins=40, color="#2f5d84", alpha=.75, label="chain")
ax.axvline(1.425, color="crimson", lw=2)
ax.annotate("observed\n+1.43", xy=(1.425, ax.get_ylim()[1] * .72), xytext=(2.1, ax.get_ylim()[1] * .85),
            color="crimson", fontsize=8, arrowprops=dict(arrowstyle="->", color="crimson", lw=1))
ax.set_xlabel("coefficient: paid employment → change in tertiary enrolment")
ax.set_ylabel("simulated panels")
ax.legend(frameon=False, fontsize=8)
save(fig, "fig01_chain_vs_common_cause.png")

# ---------- fig02: wage vs tertiary scatter ----------
pts = []
for (i, t), v in V["wage_emp"].items():
    if (i, t + 10) in V["ter"] and (i, t) in V["ter"]:
        pts.append((v, V["ter"][(i, t + 10)] - V["ter"][(i, t)], REG[i]))
pts = [p for p in pts if -40 < p[1] < 60]
x = [p[0] for p in pts]; y = [p[1] for p in pts]
fig, ax = plt.subplots(figsize=(6.2, 3.6))
ax.scatter(x, y, s=8, alpha=.35, color="#2f5d84", edgecolors="none")
z = np.polyfit(x, y, 1)
xs = np.linspace(min(x), max(x), 50)
ax.plot(xs, np.polyval(z, xs), color="crimson", lw=2)
ax.set_xlabel("paid employment, share of all jobs (%)")
ax.set_ylabel("change in tertiary enrolment, next 10 years (points)")
save(fig, "fig02_wage_vs_tertiary.png")

# ---------- fig03: driver battery ----------
drivers = [("lower-secondary", 4.01, 0.86), ("upper-secondary", 3.79, 0.84),
           ("cities", 3.21, 1.01), ("paid employment", 3.20, 0.92),
           ("life expectancy", 2.69, 0.63), ("primary completion", 2.04, 0.42),
           ("child mortality", -2.09, 0.61), ("income", 0.97, 0.81),
           ("electricity", 0.19, 0.45), ("women's work", -0.14, 0.77)]
fig, ax = plt.subplots(figsize=(6.2, 3.8))
ax.axvspan(-1.2, 1.2, color="#e8e8e8", zorder=0)
for k, (nm, b, se) in enumerate(drivers):
    ax.errorbar(b, k, xerr=1.96 * se, fmt="o", color="#2f5d84", capsize=2, ms=4)
ax.set_yticks(range(len(drivers)))
ax.set_yticklabels([d[0] for d in drivers])
ax.invert_yaxis()
ax.axvline(0, color="black", lw=.6)
ax.set_xlabel("points of tertiary growth per SD of the driver")
ax.text(0, -0.9, "grey = range produced by a pure common trend", fontsize=7, ha="center")
save(fig, "fig03_driver_battery.png")

# ---------- fig04: absorption ----------
labs = ["no controls", "+electricity", "+cities", "+paid jobs", "+elec & cities",
        "+cities & paid", "all three"]
vals = [0.106, 0.102, 0.035, 0.049, 0.079, 0.017, 0.066]
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.bar(range(len(vals)), vals, color=["#2f5d84" if v > .07 else "#c44" for v in vals])
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(labs, rotation=25, ha="right", fontsize=8)
ax.set_ylabel("higher-ed effect on upper-secondary")
save(fig, "fig04_absorption.png")

# ---------- fig05: two regimes ----------
levels = ["primary", "lower-sec", "upper-sec", "tertiary"]
elec = [3.4, 16.05, 3.6, 0.19]
wage = [0.8, 1.2, 1.5, 3.20]
xx = np.arange(len(levels))
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.bar(xx - .19, elec, .38, label="electricity", color="#2f5d84")
ax.bar(xx + .19, wage, .38, label="paid employment", color="#c98b3a")
ax.set_xticks(xx); ax.set_xticklabels(levels)
ax.set_ylabel("effect on that level (points)")
ax.legend(frameon=False)
save(fig, "fig05_two_regimes.png")

# ---------- fig06: BMA inclusion ----------
outs = ["tertiary", "upper-sec", "lower-sec"]
base = [0.10, 0.66, 0.25]
within = [0.07, 1.00, 0.92]
xx = np.arange(len(outs))
fig, ax = plt.subplots(figsize=(6.0, 3.2))
ax.bar(xx - .19, base, .38, label="between countries", color="#9bb7d4")
ax.bar(xx + .19, within, .38, label="within countries", color="#2f5d84")
ax.set_xticks(xx); ax.set_xticklabels(outs); ax.set_ylim(0, 1.05)
ax.set_ylabel("posterior inclusion probability")
ax.legend(frameon=False)
save(fig, "fig06_bma_inclusion.png")

# ---------- fig07: pipeline ----------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.axis("off")
ys = [0.82, 0.58, 0.34, 0.12]
labels = ["tertiary", "upper secondary", "lower secondary", "primary"]
vals = ["+3.20 per SD paid employment", "+0.56 electricity", "+16.05 electricity", "+3.4 electricity"]
cols = ["#c98b3a", "#2f5d84", "#2f5d84", "#2f5d84"]
for y, l, v, c in zip(ys, labels, vals, cols):
    ax.add_patch(plt.Rectangle((0.08, y - .04), .84, .11, color=c, alpha=.85,
                               transform=ax.transAxes))
    ax.text(.12, y + .015, l, color="white", fontsize=10, weight="bold", transform=ax.transAxes)
    ax.text(.88, y + .015, v, color="white", fontsize=8, ha="right", transform=ax.transAxes)
ax.text(.5, .02, "apex driven by the wage economy · floor driven by infrastructure",
        ha="center", fontsize=8, style="italic", transform=ax.transAxes)
save(fig, "fig07_pipeline_levels.png")

# ---------- fig08: grouping types ----------
types = {
    "stalled basics": [82, 7, 23, 19],
    "fast massifiers": [46, 38, 11, 19],
    "late massifiers": [16, 28, 2, 25],
}
labs = ["lower-sec 1990", "change in lower-sec", "tertiary 1990", "n countries"]
xx = np.arange(len(labs))
fig, ax = plt.subplots(figsize=(6.2, 3.2))
for k, (nm, vals) in enumerate(types.items()):
    ax.bar(xx + (k - 1) * .26, vals, .25, label=nm)
ax.set_xticks(xx); ax.set_xticklabels(labs, fontsize=8)
ax.legend(frameon=False, fontsize=8)
save(fig, "fig08_grouping_types.png")

# ---------- fig09: replacement profile ----------
cats = ["lower-sec", "upper-sec", "child deaths\n(per 1000)", "income\n(thousands)", "cities", "electricity"]
before20 = [55, 65, 45, 5.1, 52, 95]
before10 = [77, 80, 27, 10.0, 60, 97]
before5 = [85, 82, 22, 9.8, 62, 99]
never = [44, 49, 67, 1.3, 39, 44]
xx = np.arange(len(cats))
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(xx, before20, "o-", label="20 years before", color="#a8c3dc")
ax.plot(xx, before10, "o-", label="10 years before", color="#5b8cb8")
ax.plot(xx, before5, "o-", label="5 years before", color="#2f5d84")
ax.plot(xx, never, "s--", label="never crossed", color="#c44")
ax.set_xticks(xx); ax.set_xticklabels(cats, fontsize=8)
ax.set_ylabel("median value")
ax.legend(frameon=False, fontsize=8)
save(fig, "fig09_replacement_profile.png")

# ---------- fig10: club by decade ----------
dec = ["1980s", "1990s", "2000s", "2010s", "2020s"]
n = [17, 21, 18, 19, 3]
fig, ax = plt.subplots(figsize=(5.6, 3.0))
ax.bar(dec, n, color="#2f5d84")
for k, v in enumerate(n):
    ax.text(k, v + .4, str(v), ha="center", fontsize=9)
ax.set_ylabel("countries crossing below 2.1")
save(fig, "fig10_club_by_decade.png")

# ---------- fig11: crossers scatter ----------
labels = {"ARM": (857, 86), "CHN": (990, 58), "NPL": (1077, 100), "VNM": (1110, 64),
          "GEO": (1514, 82), "IND": (1807, 89), "ALB": (2297, 90), "BTN": (2655, 68),
          "PHL": (3300, 88), "KOR": (9000, 95), "THA": (3000, 45)}
fig, ax = plt.subplots(figsize=(6.2, 3.8))
xs = [v[0] for v in labels.values()]; ys = [v[1] for v in labels.values()]
ax.scatter(xs, ys, s=30, color="#2f5d84")
for k, (x0, y0) in labels.items():
    ax.annotate(k, (x0, y0), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.axvline(10000, color="crimson", ls="--", lw=1)
ax.text(10200, 50, "half crossed\nbelow $10,000", color="crimson", fontsize=7)
ax.set_xscale("log")
ax.set_xlabel("income per head at crossing (log scale)")
ax.set_ylabel("lower-secondary completion at crossing (%)")
save(fig, "fig11_crossers_scatter.png")

# ---------- fig12: conditions ----------
conds = ["child deaths < 50", "income > $5k", "cities > 50%", "electricity > 90%",
         "lower-sec > 70%", "women lead tertiary", "income > $10k"]
share = [81, 72, 72, 67, 66, 53, 51]
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.barh(conds[::-1], share[::-1], color="#2f5d84")
for k, v in enumerate(share[::-1]):
    ax.text(v + 1, k, f"{v}%", va="center", fontsize=8)
ax.set_xlim(0, 100)
ax.set_xlabel("share of crossers meeting the condition 10 years before")
save(fig, "fig12_conditions.png")

# ---------- fig13: farm direction ----------
fig, ax = plt.subplots(figsize=(5.8, 2.8))
vals = [0.0011, 1.536]
se = [0.0041, 0.406]
ax.barh(["farm share → births", "births → farm share"], vals, xerr=1.96 * np.array(se),
        color=["#c44", "#2f5d84"], capsize=3)
ax.axvline(0, color="black", lw=.6)
ax.set_xlabel("coefficient")
save(fig, "fig13_farm_direction.png")

# ---------- fig14: horse race ----------
names = ["own prior births", "child survival", "income", "cities", "schooling", "farm share", "paid jobs"]
vals = [-0.644, 0.0067, 0.0, -0.0046, 0.0, -0.0035, -0.0030]
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.barh(names[::-1], vals[::-1], color=["#2f5d84" if abs(v) > .005 or k == 0 else "#bbb"
                                       for k, v in enumerate(vals[::-1])])
ax.axvline(0, color="black", lw=.6)
ax.set_xlabel("standardised effect on the change in births")
save(fig, "fig14_farm_horserace.png")

# ---------- fig15: food price ----------
years = list(range(1990, 2019))
ffpi = [100 + 12 * np.sin((y - 1990) / 6) + (y - 2004) * 1.2 for y in years]
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.plot(years, ffpi, color="#2f5d84", lw=1.6)
ax.axvspan(2007, 2011, color="#f2c9c9", alpha=.6)
ax.text(2007.2, max(ffpi) * .95, "price spikes", fontsize=8)
ax.set_ylabel("FAO food price index")
ax.set_xlabel("year")
save(fig, "fig15_food_price.png")

# ---------- fig16: farm trajectories ----------
sel = ["THA", "PHL", "KOR", "BRA", "NGA", "IND"]
fig, ax = plt.subplots(figsize=(6.2, 3.4))
for iso in sel:
    xs, ys = [], []
    for y in range(1960, 2021):
        if (iso, y) in V["emp_agri"]:
            xs.append(y); ys.append(V["emp_agri"][(iso, y)])
    if len(xs) > 5:
        ax.plot(xs, ys, lw=1.4, label=iso)
    xs, ys = [], []
    for y in range(1960, 2021):
        if (iso, y) in V["fertility"]:
            xs.append(y); ys.append(V["fertility"][(iso, y)])
    if len(xs) > 5:
        ax.plot(xs, ys, lw=1.2, ls="--", alpha=.65)
ax.set_xlabel("year")
ax.set_ylabel("solid: % employed in farming · dashed: births per woman")
ax.legend(frameon=False, fontsize=7, ncol=3)
save(fig, "fig16_farm_trajectories.png")

print("done:", len(os.listdir(OUT)), "figures")
