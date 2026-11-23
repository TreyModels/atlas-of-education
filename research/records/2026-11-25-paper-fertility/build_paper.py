#!/usr/bin/env python3
"""Assemble the Paper F draft from section files, renumber headings, append references."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(HERE, p)).read().rstrip() + "\n\n"
parts = []
parts.append(read("draft/frame_intro_new.md"))
parts.append(read("draft/section2_literature.md"))
parts.append(read("sections/section3_methods.md"))
s = read("sections/section1_levels_changes.md")
s = s.replace("# Section 1. The wrong level of analysis: a large between-country schooling–fertility gradient that the within-country design erases",
              "# 4. The finding: a global between-country gradient that the standard change design erases")
s = re.sub(r"^## 1\.(\d)", r"## 4.\1", s, flags=re.M)
parts.append(s)
parts.append(read("sections/section5_implications.md"))
parts.append(read("sections/section6_future.md"))
parts.append("# 7. Supporting evidence: the survey gradient, the nulls, the transition, and the threshold\n\n"
             "The four subsections that follow are the project's supporting workstreams. They are subordinate to the "
             "centrepiece audit: each tests a mechanism or a data source, and each reports its verdict with the same "
             "claim-to-source discipline.\n\n")
d = read("sections/section4_dhs.md")
d = d.replace("# Section 4. The survey-level gradient: what DHS says about schooling and completed fertility, and what it cannot say",
              "## 7.1 The survey-level gradient: what DHS says about schooling and completed fertility, and what it cannot say")
d = re.sub(r"^## 4\.(\d)", r"### 7.1.\1", d, flags=re.M)
parts.append(d)
c = read("sections/section3_care_nulls.md")
c = re.sub(r"^## (\d)\.", r"### 7.2.\1", c, flags=re.M)
c = c.replace("# Paper F section (for un-data): care work, policy bounds, and tipping points",
              "## 7.2 Care work, policy bounds, and tipping points: three falsifiable mechanisms")
parts.append(c)
t = read("sections/section4_transition.md")
t = re.sub(r"^## (\d)\.", r"### 7.3.\1", t, flags=re.M)
t = t.replace("# Paper F (Fertility) — Section: the transition engine, the individuation (dose) model, and the tolerance ladder",
              "## 7.3 The transition engine, the individuation model, and the tolerance ladder")
parts.append(t)
h = read("sections/section5_threshold.md")
h = h.replace("# Section 5. Where in the schooling distribution the gradient lives: the threshold shape and the massification margin",
              "## 7.4 Where in the schooling distribution the gradient lives: the threshold shape and the massification margin")
h = re.sub(r"^## 5\.(\d)", r"### 7.4.\1", h, flags=re.M)
parts.append(h)
parts.append(read("sections/section8_discussion.md"))
refs = [l.rstrip() for l in open(os.path.join(HERE, "lit/refs.md")) if l.startswith("- ")]
parts.append("# References\n\n" + "\n".join(refs) + "\n")
draft = "\n".join(parts)
out = os.path.join(HERE, "draft/paperF_draft.md")
open(out, "w").write(draft)
words = len(re.findall(r"\b\w+\b", draft))
body_words = len(re.findall(r"\b\w+\b", draft.split("# References")[0]))
print(f"wrote {out}: {words} words total ({body_words} before references); {len(refs)} references")
