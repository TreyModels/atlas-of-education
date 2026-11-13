"""Figures for the paper, from results/summary.json and the posterior files."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

R = Path("results"); F = Path("paper/figures"); F.mkdir(parents=True, exist_ok=True)
S = json.loads((R / "summary.json").read_text())
VARIANTS = [v for v in ["thin", "diversion", "favour", "full"] if v in S["variants"]]
LABEL = {"thin": "Thin schooling", "diversion": "Diversion", "favour": "Favour", "full": "Full model"}
COLOR = {"thin": "#2a78d6", "diversion": "#eb6834", "favour": "#1baf7a", "full": "#eda100"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 9,
                     "axes.titleweight": "bold", "axes.titlecolor": INK})


def dot_panel(ax, rows, title, ref=None, pct=True, xlabel=None):
    """rows: list of (label, variant, [q05, q50, q95])."""
    ys = np.arange(len(rows))[::-1]
    scale = 100 if pct else 1
    for y, (lab, v, q) in zip(ys, rows):
        ax.plot([q[0] * scale, q[2] * scale], [y, y], color=COLOR[v], lw=2, solid_capstyle="round")
        ax.plot(q[1] * scale, y, "o", ms=6, color=COLOR[v], mec="white", mew=1.2, zorder=3)
    ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows])
    ax.tick_params(axis="y", length=0)
    if ref is not None:
        for r in np.atleast_1d(ref):
            ax.axvline(r * scale, color=MUTED, lw=1, ls=(0, (3, 2)), zorder=0)
    ax.grid(axis="x", color=GRID, lw=.6); ax.set_axisbelow(True)
    ax.set_title(title, loc="left")
    if xlabel:
        ax.set_xlabel(xlabel)


# Figure 1: fit to the seven patterns
patterns = [("participation", "Participation, all"), ("participation_g9", "Participation, Grade 9"),
            ("participation_g12", "Participation, Grade 12"), ("own_purchase_share", "Own teacher share"),
            ("other_purchase_share", "Other teacher share"), ("teacher_tutor_share", "Teachers who tutor")]
fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.9), sharey=True)
for ax, (key, title) in zip(axes.flat, patterns):
    target, tol = S["targets"][key]
    ax.axvspan((target - tol) * 100, (target + tol) * 100, color="#f1f0ec", zorder=0)
    rows = [(LABEL[v], v, S["variants"][v]["fit"][key]) for v in VARIANTS]
    dot_panel(ax, rows, title, ref=target)
for ax in axes[1]:
    ax.set_xlabel("Percent")
fig.text(0.01, 0.005, "Dashed line: published value. Shaded band: tolerance. Dots: weighted posterior median; bars: 90% interval.",
         color=MUTED, fontsize=7.5)
fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(F / "fig1_fit.png", dpi=220); plt.close(fig)

# Figure 2: policy effects on non-buyers' regular instruction and on participation
pols = [("ban_own", "Ban own-pupil sales"), ("cond_pay", "Conditional pay"),
        ("extra_time", "Ten more points of class time"), ("com_entry", "Commercial entry")]
fig, axes = plt.subplots(2, 4, figsize=(7.4, 3.9), sharey=True)
for j, (pol, title) in enumerate(pols):
    for i, (key, lab) in enumerate([("nonbuyer_class_instruction", "Regular instruction where pupils do not buy"),
                                    ("participation", "Participation")]):
        rows = [(LABEL[v], v, S["policy_effects"][v][pol][key]) for v in VARIANTS]
        dot_panel(axes[i, j], rows, title if i == 0 else "", ref=0)
        axes[i, j].set_xlabel("Change, points" if i == 1 else "")
    axes[0, 0].set_ylabel("Regular instruction\nwhere pupils do not buy", labelpad=6)
    axes[1, 0].set_ylabel("Participation", labelpad=6)
fig.tight_layout(); fig.savefig(F / "fig2_policies.png", dpi=220); plt.close(fig)

# Figure 3: signatures
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.0), sharey=True)
rows = [(LABEL[v], v, S["variants"][v]["signatures"]["instr_gap_tutoring_vs_not"]) for v in VARIANTS]
dot_panel(axes[0], rows, "Delivered instruction: tutoring minus non-tutoring teachers' classes", ref=0, xlabel="Points")
rows = [(LABEL[v], v, S["variants"][v]["signatures"]["buy_gap_tutoring_vs_not"]) for v in VARIANTS]
dot_panel(axes[1], rows, "Purchase rate in the subject: same comparison", ref=0, xlabel="Points")
fig.tight_layout(); fig.savefig(F / "fig3_signatures.png", dpi=220); plt.close(fig)

# Figure 4: what the patterns say about the mechanism parameters (full model)
richest = "full" if "full" in VARIANTS else VARIANTS[-1]
post = pd.DataFrame(json.loads((R / f"posterior_{richest}.json").read_text())["particles"])
for col in ("diversion", "favour"):
    post[col] = post.get(col, 0.0)
w = post["weight"] / post["weight"].sum()
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.1))
for ax, (key, lab, hi) in zip(axes, [("diversion", "Diversion response β", 4), ("favour", "Own-teacher benefit φ", 2),
                                     ("thin", "Thin-schooling response ξ", 3)]):
    ax.hist(post[key], bins=np.linspace(0, hi, 17), weights=w, color=COLOR["full"], edgecolor="white", lw=1.5)
    ax.axhline(1 / 16, color=MUTED, lw=1, ls=(0, (3, 2)))
    ax.set_title(lab, loc="left"); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlim(0, hi)
axes[0].text(0.02, 1 / 16, " uniform prior", color=MUTED, fontsize=7, va="bottom", transform=axes[0].get_yaxis_transform())
fig.tight_layout(); fig.savefig(F / "fig4_posterior.png", dpi=220); plt.close(fig)
print("figures written")
