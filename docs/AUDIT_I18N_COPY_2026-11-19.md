# i18n root-cause + copy polish audit — 19 Nov 2026

**Auditor:** DeepSeek (auditor teammate) · **Repo:** `TreyModels/atlas-of-education` @ `origin/main` `270d705` (after PR #13/#16)
**Branch:** `audit/i18n` · **Scope:** read-only analysis; **no app edits** — this doc only.
**Companion audits:** `docs/AUDIT_MODEL_COVERAGE_2026-11-19.md` (coverage), `docs/AUDIT_LIVE_SITE_2026-11-19.md` (live-site/QA), `docs/AUDIT_RESEARCH_ARCHIVE_2026-11-19.md` (archive).

**Method.** (1) TypeScript AST scan of every shipped `.tsx`/`ts` for user-facing literals not wrapped in `t()` (JSX text, `aria-label`/`title`/`placeholder`/`alt`, JSX attribute strings, template fragments). (2) Programmatic census of all *rendered* strings (components' `t('…')` literals + every string in `about.ts`, `site-status.ts`, `home-explainer.ts`, `family-stories.ts`, all nine journeys, `model-catalogue.ts`, `cards/guide/model-stories/analysis-advice/control-audit.json`, and all 22 worlds' `nav/title/meta/question/version/controls/evidence/view` data) against the merged dictionary (`translations.json` ⊕ `ui-translations.json`). (3) Headless-Chrome render of 17 routes in `en` vs `zh-Hans` on the built app (`vite preview`, current `main`), diffing visible text and attributes. (4) Dictionary quality pass (missing/empty/identical/Latin-prose/fr-vi) and dead-key pass (key is neither an exact nor a substring of any rendered string — matching `translate()`'s substring behaviour). (5) Copy grep for brand/spelling/date/typography/placeholder defects.

**Reproduce:** `node scripts/check-react.cjs` and `node check-translations.cjs` both **PASS** on `270d705` — the gap below is invisible to them, because those checks test *dictionary → zh-Hans completeness*, never *source string → dictionary coverage*. That asymmetry is the root cause of everything in §2.

---

## 1. Executive summary — priorities

| # | Pri | Finding | Where |
| --- | --- | --- | --- |
| P0-1 | **P0** | **Home page chrome is untranslated.** Chinese visitors see English purpose/state badges (`Published foundation`, `Mechanism exploration`, `Implementation checked`…), nine English family status lines, English status intro and English CTA buttons. 8 + 9 + 5 strings; suggestions in §3.1. | `src/data/angkor-journey.ts:24-35`, `src/data/site-status.ts:8-36`, rendered `Library.tsx:145-156, 183-184, 260-268` |
| P0-2 | **P0** | **Every narrated journey page leaks English chrome** — 15 structural strings (`What the evidence says`, `The rule we wrote`, `What the experiment shows`, `Limits`, `How the maths works`, `Deeper experiments`, `Open workbench`, `Notes`, `Propose a version`, `Chapters`, `Download and adapt`…) plus the 5 claim labels (`From the published study`, `Observed data`, `Produced by an Atlas simulation`, `Still unsettled`, `How the model works`). | `src/components/AngkorJourney.tsx:11,29-32,71,96,101,106,113,118,145,156-161`; `src/data/angkor-journey.ts:36-42` |
| P0-3 | **P0** | **PR #15 content edits silently dropped their translations** (dictionary is keyed by the full English sentence). The new `about.ts:28` and `site-status.ts:28` sentences have no zh-Hans; the superseded keys still sit live in `ui-translations.json:3493` and `:3761`. About page now mixes Chinese paragraphs with one English paragraph. | `src/data/about.ts:28`, `src/data/site-status.ts:28`; dead: `src/data/ui-translations.json:3493,3761` |
| P0-4 | **P0** | **The precise English-only disclosure is a dead key.** `translations.json:17` ("Language applies to navigation and core controls. Detailed research notes and some model descriptions remain in English…") is referenced nowhere; the only live disclosure (`ui-translations.json:1472`, rendered `Library.tsx:273`) says "classic workbenches, linked publications and archived research files retain original language" — it does **not** cover narrated model pages, which are 87–99% English in 8 of 9 families (§4). | `src/data/translations.json:17` (dead), `src/data/ui-translations.json:1472`, `Library.tsx:273` |
| P1-5 | P1 | **Old brand + untranslatable version strings**: 8 live worlds still expose `Atlas of Education 0.11.2 · …` in the evidence panel; `Workbench.tsx:142` renders `{world.version}` **without `t()`**, so no dictionary can ever translate it. | `src/models/worlds.js:31,112,158,544,588,640,679,719`; `Workbench.tsx:142` |
| P1-6 | P1 | **`about/workflow` page is entirely English** (19 strings incl. title and 8 headings); nav-linked. Also `how-models-work`'s formula line `share = runs with the outcome ÷ total runs` and `BetaExplorer`'s 9 strings (Angkor "Watch this" moment) are missing. | `src/data/about.ts:63-90`; `about.ts:49` area; `src/components/BetaExplorer.tsx:26-44` |
| P1-7 | P1 | **zh-Hans brand/quality defects**: brand "Atlas Worlds" correctly stays Latin (8/8 entries ✅), but 21 entries translate the collection name "Atlas" into `地图集`/`图谱`, mixing with `Atlas`/`《Atlas》`; untranslated Latin tokens survive in Chinese (`adjusted gender parity` → `调整后性别 parity`; `logistic 工具`; `onset 中位数`; `Harvest 仍然…`; `tipping 悬崖`); the CCP model name flips between `CCP bus` and `中共巴士`/`巴士`. Full table §5. | `translations.json:22,427,…,1922,1927,2962,4787,4817`; `ui-translations.json:2387,2412,2432,2872,2982,3017` |
| P2-8 | P2 | **254 candidate dead dictionary keys**, incl. 4 old-brand keys (`THE ATLAS OF EDUCATION · COMPLETE MODEL LIBRARY` at `ui-translations.json:1357`), 4 stale language-count keys (`… · 3 languages`), 2 superseded about strings, 2 duplicate disclosure strings, and ~240 strings from the pre-PR-13 workbench/catalogue UI. | §6 |
| P2-9 | P2 | **Copy polish**: mixed date formats (`14 November 2026` in prose vs `2026-11-07` / `Atlas of Education 0.11.2` in versions vs `19 Nov 2026`), `2 languages` rail copy (accurate for the React UI = en+zh, but opaque; stale "3 languages" keys linger), legacy product naming decisions needed (`Full Education Atlas`, `Atlas of Models`, `Atlas of Education`), inconsistent zh spacing around Latin/digits (`PDSI映射` vs `PDSI 映射`; `2015年后` vs `2015 年`). British spelling is otherwise consistent; no TODO/lorem/placeholder text found. | §7 |

**The root cause is not missing `t()` wrappers.** The AST scan found essentially **zero** untranslated user-facing literals in shipped components (exceptions: `Navigation.tsx:36-38` deliberately trilingual language label + native `English` endonym; `ESC` key hint; `DOI …`; per-language copyright ternaries in `App.tsx:125`). The gap is **1,212 rendered English strings with no dictionary entry** (§2), overwhelmingly data-driven prose/labels that *are* already passed through `t()`.

---

## 2. Root-cause census

### 2.1 Rendered strings vs dictionary (whole app, current main)

3,099 distinct rendered English strings collected from the sources listed in the method; **1,212 (39%) have no entry in the merged dictionary**, so `translate()` falls through to English in zh-Hans mode.

| Source | Rendered strings | Missing | Notes |
| --- | --- | --- | --- |
| `src/data/education-journey.ts` | 144 | **137 (95%)** | narration + card notes |
| `src/data/systems-journey.ts` | 111 | **101 (91%)** | |
| `src/data/shadow-journey.ts` | 96 | **95 (99%)** | |
| `src/data/angkor-journey.ts` | 137 | **135 (99%)** | includes purpose/state/claim label vocab |
| `src/data/fertility-journey.ts` | 105 | **92 (88%)** | |
| `src/data/planning-journey.ts` | 95 | **83 (87%)** | |
| `src/data/extension-journey.ts` | 58 | **56 (97%)** | |
| `src/data/deephistory-journey.ts` | 41 | **37 (90%)** | |
| `src/data/ccp-journey.ts` | 80 | **6 (8%)** | **the only translated journey** — see §4 |
| `src/data/site-status.ts` | 49 | **47 (96%)** | statusIntro, 9 family lines, CTA + 4 buttons + licence |
| `src/data/family-stories.ts` | 159 | 57 (36%) | component `StoryPage.tsx` is **dead** (not routed); low priority |
| `src/data/about.ts` | 64 | **25 (39%)** | workflow article + 2 PR-15 sentences + 1 formula |
| `src/components/AngkorJourney.tsx` (t() literals) | 15 | **15 (100%)** | journey chrome |
| `src/components/BetaExplorer.tsx` | 9 | **9 (100%)** | Angkor chapter 1 interactive |
| `src/components/*` other (Library/Nav/Workbench/DataChart/Model*/Guide/Catalogue/SchoolFutures/App) | 96 | **1 (`Year`)** | chrome is translated ✅ |
| `src/data/model-catalogue.ts` | 203 | 28 | all 28 are `keywords` (search-only, not displayed — **not a defect**) |
| `src/data/cards.json` / `guide.json` | 158 | 29 | fragments/hrefs/ids (not displayed — not a defect) |
| `src/data/control-audit.json` | 181 | 15 | `M_REL`, `greedy`, option ids (data, not displayed — not a defect) |
| 22 worlds (`nav/title/meta/question/version/controls/evidence/view`) | ~900 | **~25** | 22 × `version` string + 3 citations (`Lieberman & Buckley 2012` etc., intentionally Latin) |

### 2.2 Strings that can never translate (hardcoded)

| File:line | String | Verdict |
| --- | --- | --- |
| `src/components/Navigation.tsx:36` | `Language / 语言 / Ngôn ngữ` (sr-only) | intentional trilingual label — keep |
| `src/components/Navigation.tsx:37` | `aria-label="Language / 语言 / Ngôn ngữ"` | same; acceptable for a language picker (it must be readable before a language is chosen) |
| `src/components/Navigation.tsx:38` | `<option>English</option>` | native endonym convention (pairs with 简体中文) — keep |
| `src/components/Navigation.tsx:172` | `ESC` (kbd hint) | key name — keep |
| `src/App.tsx:125` | `DOI 10.5281/zenodo.24369167` | identifier — keep |
| `src/App.tsx:125` | copyright sentences as `language === 'zh-Hans' ? '…' : language === 'vi' ? '…' : '…'` | hardcoded per-language copy instead of dictionary; works today for en/zh/vi but a third shipping language would need code changes. Low priority; note for consistent i18n. |
| `src/components/Workbench.tsx:142` | `{world.version}` (raw render, no `t()`) | **real defect** (P1-5): 22 version strings bypass translation & carry the old brand |
| `src/components/*`, 7 candidates only | `textAnchor`, `sandbox`, `scrolling` etc. | not user-facing |

**No JSX prose literals remain unwrapped anywhere in shipped chrome.** The one real structural fix is `Workbench.tsx:142` (+ world data brand).

### 2.3 Why translations keep getting lost (process root cause)

The dictionary is keyed by the **full English source string**. Any copy edit creates a new key with no translation and orphans the old one. Live examples on `270d705`:

- `about.ts:28` and `site-status.ts:28` were edited in PR #15; new keys absent, old keys dead at `ui-translations.json:3493` and `:3761` (both still carry correct zh-Hans).
- `ui-translations.json:1472` (live, rendered) vs `translations.json:2212` (dead near-duplicate) — two subtly different disclosure sentences.
- `translations.json:1922`/`:1927`/`:2962` etc. translate "Atlas" inconsistently because different copy edits produced different keys.

**Recommended process rule (no code change needed now):** any PR touching an English string in `about.ts`/`site-status.ts`/`ui-translations.json`-backed data must update the dictionary key in the same commit (add a "translation diff" check to CI: the source→dictionary coverage test in §8). Longer-term, move high-churn prose to stable ids, but that is not needed for launch.

---

## 3. P1 handover: UI chrome that must be Chinese (exact strings + suggested zh-Hans)

### 3.1 Home page (`site-status.ts` + label vocab)

| File:line | Current English | Suggested zh-Hans | Notes |
| --- | --- | --- | --- |
| `angkor-journey.ts:25` | Published foundation | 已发表基础模型 | badge label, rendered `Library.tsx:155,183` |
| `angkor-journey.ts:25` | Implements relationships reported in a peer-reviewed study. | 实现同行评审研究报告中的关系。 | tooltip (`title=`) |
| `angkor-journey.ts:26` | Mechanism exploration | 机制探索 | |
| `angkor-journey.ts:26` | Asks what follows if these rules held. Not a reconstruction of what happened. | 追问若这些规则成立会怎样；这不是对史实的重建。 | |
| `angkor-journey.ts:27` | Teaching | 教学模型 | |
| `angkor-journey.ts:27` | Built to show an idea clearly. Complete for that purpose. | 为清楚地展示某一想法而建；就这一目的而言是完整的。 | |
| `angkor-journey.ts:28` | Description and accounting | 描述与核算 | |
| `angkor-journey.ts:28` | Keeps food, labour and people consistent so other rules can be examined. | 保持食物、劳力与人口一致，以便检验其他规则。 | |
| `angkor-journey.ts:31-34` | Implementation checked / In development / Historical result / Empirically evaluated | 实现已检查 / 开发中 / 历史结果 / 经实证评估 | state badges |
| `angkor-journey.ts:31-34` | (4 help strings) | 代码、账本与存储结果已核验；未经历史验证。／规则或输入仍有已知缺口，已列于卡片。／作为记录保留；其结论已被取代或有限。／已用其构建时未使用的观测数据检验。 | |
| `site-status.ts:9-11` | Read this first / Models you can inspect, with their code and limits / Some models implement findings from peer-reviewed studies… | 请先阅读 / 可检查的模型，附带其代码与限制 / 部分模型实现同行评审研究的发现；部分探索若某机制成立会怎样；部分用于教学；部分仍在建设中。每个模型页面都会说明属于哪一种、检验到何种程度。标签是对模型可主张范围的限制，而非评分。 | statusIntro kicker/title/text (rendered `Library.tsx:144-146`) |
| `site-status.ts:15-23` | 9 family `line` sentences (angkor, shadow, politics, extension, planning, fertility, education, systems, deephistory) | e.g. angkor → 以同行评审研究（Klassen 等，2022）为基础；后续扩展是逐项标注的机制探索。 education → 文凭、学校教育与工作，包括中国青年失业模型（拟合后仍存在未解释的残差）。 systems → 队列、教师、教室与预算随人口变化推进。 | each is one long sentence; translate as a batch |
| `site-status.ts:27` | Think a model is missing something? Change it. | 觉得某个模型缺了什么？修改它。 | CTA title |
| `site-status.ts:28` | Every model’s code can be downloaded and run on your own machine. … | 每个模型的代码都可以下载并在你自己的机器上运行。如果你改变某项假设、加入数据或发现错误，请提交你的版本。所有提案都会在列入本站前由 Dr. Trey Menefee 审核。 | **PR-15 regression** |
| `site-status.ts:30-33` | Download all the code / Propose a version / Challenge a claim / How to cite (CC BY-NC 4.0) | 下载全部代码 / 提交你的版本 / 质疑某项主张 / 如何引用（CC BY-NC 4.0） | CTA buttons |
| `site-status.ts:35` | Licensed CC BY-NC 4.0: … | 已按 CC BY-NC 4.0 许可发布：注明 Dr. Trey Menefee 后可重用和改编，仅限非商业用途。版本化发布用于引用；DOI 详情将在发布后显示。 | footer |

### 3.2 Journey chrome (all nine story pages)

| File:line | Current English | Suggested zh-Hans |
| --- | --- | --- |
| `AngkorJourney.tsx:29` | Open workbench | 打开工作台 |
| `AngkorJourney.tsx:30` | Code | 代码 |
| `AngkorJourney.tsx:31` | Notes | 说明 |
| `AngkorJourney.tsx:32` | Propose a version | 提交你的版本 |
| `AngkorJourney.tsx:71` | Chapters (aria-label) | 章节目录 |
| `AngkorJourney.tsx:96` | What the evidence says | 证据怎么说 |
| `AngkorJourney.tsx:101` | The rule we wrote | 我们写下的规则 |
| `AngkorJourney.tsx:106` | What the experiment shows | 实验显示了什么 |
| `AngkorJourney.tsx:113` | Limits | 局限 |
| `AngkorJourney.tsx:118` | How the maths works | 数学如何运作 |
| `AngkorJourney.tsx:145` | Deeper experiments | 深入实验 |
| `AngkorJourney.tsx:156` | Download and adapt | 下载并改编 |
| `AngkorJourney.tsx:157` | Everything here, the models, their data and these notes, lives in one repository. Download it, run a model, and change a rule to see what carries the result. | 这里的一切——模型、数据与这些说明——都在同一个代码库中。下载它，运行一个模型，改动一条规则，看看结果由什么承载。 |
| `AngkorJourney.tsx:159` | The repository on GitHub | GitHub 上的代码库 |
| `AngkorJourney.tsx:161` | Download the code (zip) | 下载代码（zip） |
| `angkor-journey.ts:37-41` | From the published study / Observed data / Produced by an Atlas simulation / Still unsettled / How the model works | 来自已发表研究 / 观测数据 / 由 Atlas 模拟生成 / 仍未有定论 / 模型运作方式 |

`AngkorJourney.tsx:24` renders `t(purposeLabel[m.purpose].help)` as a tooltip, so §3.1 label/help entries also fix the story cards.

### 3.3 Angkor beta explorer (`BetaExplorer.tsx`)

| File:line | Current English | Suggested zh-Hans |
| --- | --- | --- |
| :26 | Watch this | 看这里 |
| :26 | Move community size. With β above 1, each person’s share of the production index rises as communities grow. | 移动社区规模。当 β 大于 1 时，社区越大，每个人分到的生产指数越高。 |
| :27 | People in a temple community | 神庙社区人数 |
| :29 | Per-person production index against community size for three scaling exponents | 三种规模指数下人均生产指数与社区规模的关系 |
| :34 | people | 人 |
| :38 | Assumption | 假设 |
| :38 | Index per person at | …人时的人均指数 |
| :41 | 95% range of the published fit | 已发表拟合的 95% 区间 |
| :44 | Index = 100 at 100 people. It is a product of archaeological proxies for labour, land and water, not tonnes of rice. | 100 人时指数为 100。它是考古代理量（劳力 × 土地 × 水）的乘积，不是稻米吨数。 |

### 3.4 Smaller chrome gaps

| File:line | Current English | Suggested zh-Hans | Note |
| --- | --- | --- | --- |
| `DataChart.tsx:68` (t of `view.xTitle`) + world data `xTitle: 'Year'` | Year | 年 | only missing axis title; other three axis titles are translated |
| `about.ts` how-models-work maths (`plain`/`formula`) | `share = runs with the outcome ÷ total runs` | 占比 = 出现该结果的运行次数 ÷ 总运行次数 | displayed in `how-models-work` maths block |
| `about.ts:63-90` | workflow article (19 strings incl. title + 8 headings) | title 一位研究者与一组 AI 代理如何构建这些模型；kicker 我的数字工作流程，2026；headings: 团队与分工 / 代理之间的共享留言板 / 廉价工作者的集群 / 底层的科学过程 / 错误如何被发现 / 默认开放 | nav-linked page currently 100% English |
| `about.ts:28` | Every model’s code can be downloaded and run on your own machine. … | 每个模型的代码都可以下载并在你自己的机器上运行。…… | PR-15 regression |
| `about.ts:81` | …Models that fail a test stay on the site, labelled as a historical or limited result. | ……未通过检验的模型仍保留在站内，并标注为"历史结果"或"有限结论"。 | part of workflow article |
| `models/worlds.js:31,112,158,544,588,640,679,719` | `Atlas of Education 0.11.2 · …` | `Atlas Worlds 0.11.2 · …` (English version identifier OK) | brand defect + raw render `Workbench.tsx:142`; either wrap in `t()` + add zh, or document version ids as English |

---

## 4. Narrated research prose — classify separately from broken chrome

The live disclosure (`Library.tsx:273`) is home-page only and does not name narrated model pages. The dead disclosure (`translations.json:17`) did. Actual state per journey (rendered strings, zh-Hans diff on built app):

| Journey | Rendered strings | Untranslated | Coverage | Verdict |
| --- | --- | --- | --- | --- |
| politics (`ccp-journey.ts`) | 80 | 6 (4 are ids) | **~92% Chinese** | *translated* — proves the pipeline works |
| fertility | 105 | 92 (88%) | mostly English | disclosed-prose category |
| planning | 95 | 83 (87%) | mostly English | disclosed-prose |
| systems | 111 | 101 (91%) | mostly English | disclosed-prose |
| deephistory | 41 | 37 (90%) | mostly English | disclosed-prose |
| education | 144 | 137 (95%) | mostly English | disclosed-prose |
| extension | 58 | 56 (97%) | mostly English | disclosed-prose |
| shadow | 96 | 95 (99%) | mostly English | disclosed-prose |
| angkor | 137 | 135 (99%) | almost all English | disclosed-prose |

**Classification for the fix task:**
- **(i) UI chrome — must be Chinese now:** §3.1–3.4. ~55 strings.
- **(ii) Narrated prose — disclosed, but disclosure needs repair:** ~1,000 strings across 8 journeys. The politics journey is already Chinese, so "narrated pages are English-only" is *not* consistently true — it is a per-family state. Recommended minimal action: update the live disclosure to name the exception explicitly, e.g. `The model library and interactive controls are translated. Narrated model pages are being translated family by family (politics is translated); linked publications and archived research files stay in their original language.` and render it on journey pages too, not only the home footer. Do **not** attempt to translate ~1,000 prose strings in the final-bundle window.
- **(iii) Names/citations to keep Latin:** person names, journal titles, `Klassen et al.`, `Lieberman & Buckley 2012`, `Buckley et al. 2010`, `CCDI`, `PDSI`, `RMSE`, file paths. Currently correctly kept Latin (2 citations are allowlisted in `check-react.cjs`).

---

## 5. zh-Hans quality: brand rule and machine-translation leftovers

**Brand rule check:** `Atlas Worlds` is kept Latin in all 8 entries that mention it (`translations.json`/`ui-translations.json`) ✅. No Chinese translation of the full brand found. **However** the collection name "Atlas" (shorthand for the product) is translated into `地图集`/`图谱` in 21 entries, and the style flips between `Atlas`, `《Atlas》` and `地图集` within the same page family:

| File:line | English key (short) | Current zh-Hans | Suggested patch |
| --- | --- | --- | --- |
| `translations.json:1922` | Atlas contribution · Executable comparison | 地图集贡献 · 可执行比较 | Atlas 贡献 · 可执行比较 |
| `translations.json:1927` | …existing Atlas long-run engine… | …既有地图集长期引擎… | …既有 Atlas 长期引擎… |
| `translations.json:2962` | Atlas extension · Dynamic accounts | 地图集扩展 · 动态核算 | Atlas 扩展 · 动态核算 |
| `translations.json:2887` | Gross collection is an Atlas assumption… | 按总收成征收是地图集假设… | …是 Atlas 的假设… |
| `translations.json:427,457,567,572,582,602,1887,3697` | "the full Atlas"/"the Atlas documents"… | 完整地图集/地图集… | keep `Atlas` (or, if a Chinese common noun is preferred, use one term consistently and define it once — but the brand rule points to keeping `Atlas`) |
| `translations.json:4817` | The Atlas documents that… | 《Atlas》记录显示… | 《Atlas》→ Atlas（书名号 imply a cited work; this is the product） |
| `ui-translations.json:122,842,847,927` | Full Education Atlas / Atlas of Education / … | 完整教育地图集 / 教育地图集 / … | **decision needed**: "Atlas of Education" is the legacy classic app's own title. Either keep it Latin as a legacy product name (`Atlas of Education（经典教育图谱）`) or translate consistently; today it is translated and sits beside Latin "Atlas Worlds". |
| `ui-translations.json:1037` | Atlas of Models (catalogue page title) | 模型图谱 | `图谱` vs `地图集` inconsistency; decide brand-architecture wording (`Atlas of Models` kept Latin? or 模型图谱) |
| `ui-translations.json:1557` | Original Angkor Atlas | 原始吴哥图谱 | 原始吴哥 Atlas / 原始 Angkor Atlas |

**Untranslated Latin tokens inside Chinese sentences** (machine-translation leftovers):

| File:line | Current zh-Hans fragment | Suggested |
| --- | --- | --- |
| `ui-translations.json:2387` | …调整后性别 parity 与师生比。 | …调整后性别均等指数与师生比。 |
| `ui-translations.json:2412` | logistic 工具把覆盖率目标所需的 S 曲线速度… | 逻辑斯蒂（logistic）工具将覆盖率目标所需的 S 曲线速度… |
| `ui-translations.json:2432` | …1,260 次走向衰落， onset 中位数为 1362 年。 | …1,260 次走向衰落，起势年份中位数为 1362 年。 |
| `translations.json:4787` | 计时已修复。Harvest 仍然忽略剩余的农场劳动力… | 计时已修复。收成（Harvest）仍然忽略剩余的农场劳动力… |
| `ui-translations.json:2182` | …不过数据并未证实存在清晰的 tipping 悬崖。 | …不过数据并未证实存在清晰的临界悬崖。 |
| `ui-translations.json:2872,2982,2992,2997,3017` | 中共巴士 / 巴士 | English keys use `CCP bus`; some zh strings keep `bus`, others say 巴士 (vehicle). Pick one: recommend keeping the model name Latin — `CCP bus · 对立机制` — and glossing the mechanism once (`bus 机制`). "中共" as a rendering of `CCP` is also inconsistent with `CCDI`, `CCP` kept Latin elsewhere. |

**zh typography:** spacing around Latin/digits is inconsistent — `PDSI映射` (`translations.json:1928`) vs `PDSI 映射` elsewhere; `2015年后` (`translations.json:4901,4931…`) vs `2015 年`. Adopt one rule (space between CJK and Latin/digits) and batch-fix. Also `S 曲线`, `β = 1.227` spacing is fine.

---

## 6. Dead dictionary keys (low priority, but they hide regressions)

Candidate dead keys: **254** of 1,774 entries (key is neither an exact rendered string nor a substring of one; matching `translate()`'s substring-replacement path). High-confidence, explicitly confirmed:

| File:line | Dead key | Why it matters |
| --- | --- | --- |
| `ui-translations.json:1357` | THE ATLAS OF EDUCATION · COMPLETE MODEL LIBRARY | old brand; no consumer left (task called this out) |
| `ui-translations.json:3493` | Every model can be downloaded, run on your own machine and changed. … Each release has a DOI… | superseded by PR #15 copy; keeps correct zh |
| `ui-translations.json:3761` | same family, DOI sentence variant | second superseded duplicate |
| `translations.json:17` | Language applies to navigation and core controls. Detailed research notes and some model descriptions remain in English… | **the precise English-only disclosure, orphaned** |
| `translations.json:2212` | The model library and interactive model interface are translated… | near-duplicate of the live `ui-translations.json:1472` |
| `ui-translations.json` (4 keys) | `24 models · 3 languages`, `37 models & worlds · 3 languages`, `{n} models & worlds · 3 languages`, `{n} catalogue entries · 3 languages` | stale language-count claims (React UI ships en + zh-Hans = 2) |
| `ui-translations.json`/`translations.json` ~240 | pre-PR-13 workbench strings, e.g. `Live model`, `Save run JSON ↓`, `Use this run in Obligations →`, `1 · Ecology and mobilisation`, `Angkor · Competing accounts` | old UI; verify with grep before deleting (dynamic/substring use is possible) |

**Caveat:** the dead-key test is conservative — a key used only via runtime string construction could appear dead. Treat the table above as delete-after-grep candidates, not a blind delete list.

---

## 7. Copy polish (all files on current main)

| Pri | File:line | Current | Suggested |
| --- | --- | --- | --- |
| P1 | `src/models/worlds.js:31,112,158,544,588,640,679,719` | `Atlas of Education 0.11.2 · …` (8 worlds) | `Atlas Worlds 0.11.2 · …`; also wrap `world.version` in `t()` at `Workbench.tsx:142` if zh version labels are wanted |
| P1 | `src/models/worlds.js` (credentials) | `Atlas 0.11.2 · relfloor_countries.py v2.1, graded liquidity · 14 November 2026` | `Atlas Worlds 0.11.2 · relfloor_countries.py v2.1 · …` (drop bare `Atlas`, avoid mixed date) |
| P2 | `Navigation.tsx:126`, `App.tsx:125`, `model-catalogue.ts:174,181,188` etc. | `Full Education Atlas` links/labels | decide legacy naming: keep "Education Atlas" as the classic app's name (add "classic") or rename link text to `Classic Education Atlas` |
| P2 | `Catalogue.tsx:46`, `App.tsx:61` | `Atlas of Models` (legacy markdown catalogue pagename) | either keep (it is a section title, not the product) or align with brand hierarchy; document decision |
| P2 | `about.ts` prose vs `shadow/ccp` prose vs version strings | dates: `14 November 2026`, `16 November 2026`, `19 November 2026` vs `2026-11-07` (version strings) vs `19 Nov 2026` (comment) | one user-facing format: `14 Nov 2026` (or ISO `2026-11-14`); leave machine version tags ISO |
| P2 | `Navigation.tsx:136` | `{n} catalogue entries · 2 languages` | copy is accurate (React UI ships en + zh-Hans; `supportedLanguages` at `i18n.ts:23`) but opaque — `{n} 个模型条目 · 英文/中文` or `{n} catalogue entries · bilingual` |
| P2 | `translations.json:17` vs `ui-translations.json:1472` vs `translations.json:2212` | three disclosure variants | consolidate to one canonical sentence, rendered on home + journey pages |
| P2 | zh punctuation | mixed `——` vs `—`, `：` vs `:`, `·` spacing inconsistent (`地图集贡献 · 可执行比较` vs `PDSI映射`) | adopt one zh typography rule (space around Latin; one dash/spacing style) and batch-fix (§5) |
| P3 | `src/components/ui/*` (43 files) | full shadcn UI kit: **not imported by any shipped component**; contains hardcoded English (`Close`, `Toggle Sidebar`, `Loading`, `Previous slide`, `breadcrumb`, `Go to pages`) | dead code + unused deps; either delete or exclude from i18n scope. Not user-visible today. |
| P3 | `src/components/StoryPage.tsx` + `src/data/family-stories.ts` | `StoryPage` is exported but imported by nothing (App renders `AngkorJourney` for `story-*`); `familyStories` used only for `document.title` | dead narrative layer (also flagged in the coverage audit, D14); deleting it removes 159 untranslated strings from the census |
| P3 | `src/data/about.ts:1` comment | straight apostrophe in `Trey's` | not user-facing; ignore |

**Verified clean (do not "fix"):** British spelling is consistent in user-facing prose (`organised`, `normalised`, `modelled`, `behaviour` in prose, `labelled`, `licence`); `behavior`/`center`/`color` appear only as JS/CSS identifiers. `CC BY-NC 4.0` formatting is consistent. No TODO/FIXME/lorem/"coming soon"/placeholder prose anywhere in `src/`. No doubled spaces in prose (the one `Y = Y₀ · N^β     per-person index…` double space is intentional formula alignment). Straight-vs-curly apostrophes are consistent in user-facing strings (curly), except code comments.

---

## 8. Recommended fix batches (for the follow-up task)

1. **Chrome batch (P0, ~60 strings, no code changes):** add zh-Hans entries for §3.1–3.3 and `Year`; fix the PR-15 regression strings (`about.ts:28`, `site-status.ts:28`); update/merge the disclosure (§4) and render it on `AngkorJourney` pages. Run `check-react.cjs` + `check-translations.cjs`.
2. **Brand/copy batch (P1, small code edits):** `worlds.js` version strings → `Atlas Worlds …`; wrap `Workbench.tsx:142` in `t()`; decide legacy "Education Atlas"/"Atlas of Models" naming; fix `{n} catalogue entries · 2 languages` copy.
3. **zh quality batch (P1, dictionary-only):** 21 brand-translation entries; 5 untranslated-token fixes; unify `CCP bus`; date format pass.
4. **Coverage test (P0-process):** add `scripts/check-i18n-coverage.mjs` that asserts every rendered source string is in the dictionary, with an explicit allowlist for (ii) narrated prose and (iii) citations. Without this test, PR-15-style regressions and 1,212-string gaps remain invisible.
5. **Dead-key/cleanup batch (P2):** delete confirmed dead keys after grep; delete unused `src/components/ui/*` + `StoryPage.tsx`/`family-stories.ts` (or wire the story route).
6. **Prose batch (post-launch, separately funded):** translate journeys family by family; politics is the template (`ccp-journey.ts` at 92%). ~1,000 strings; do not attempt in the final-bundle window.

---

## 9. Limitations / not verified

- The live-site zh render was taken from `vite preview` of current `main` at 270d705 in headless Chromium; a deployed-Pages spot check is in `docs/AUDIT_LIVE_SITE_2026-11-19.md`.
- The dead-key census is substring-based and conservative; some "dead" keys may be used by runtime string construction. Verify by grep before deleting.
- `fr`/`vi` completeness: 71 entries are zh-only (no fr/vi) — noted only; shipping pair is en + zh-Hans (`supportedLanguages`, `i18n.ts:23`), and the language selector exposes only those two (`Navigation.tsx:38`).
- Legacy `public/reference/*` and `public/research/*` pages use their own `public/languages.js` dictionary and were out of scope; they plausibly contain further English-only content and old brand strings (`ATLAS OF EDUCATION`).
- `src/components/ui/*` is unused by shipped components; its English literals were catalogued but are not user-visible today.

---

## 10. Disclosure fix — exact wording and placement (held for the post-night pass)

The disclosure that the site is (partly) English is **inaccurate and misplaced** today. The live sentence (`ui-translations.json:1472`, rendered only in the home footer at `Library.tsx:273`) says the *classic workbenches, linked publications and archived research files* stay in their original language, but the larger English-only surface is the **narrated model pages** — 87–99% English in 8 of 9 families — and the **politics journey is already translated (~92%)**, so any blanket claim would be wrong. The precise sentence that used to cover this is a dead key (`translations.json:17`: "Language applies to navigation and core controls. Detailed research notes and some model descriptions remain in English…").

**Recommended implementation (needs JSX, so not in `fix/i18n-2`):**

1. **Per-family notice on every narrated journey page.** Render a small note directly under the lede in `AngkorJourney.tsx` (after line 65, before `journey-why`), only when the interface language is not English. `AngkorJourney` needs the `language` prop threaded from `App.tsx` (it currently receives only `t`); add `.journey-translation-note` styling in `journey.css`.
   - For the 8 English-only families (angkor, education, systems, planning, fertility, shadow, deephistory, extension):
     - EN: `This narrated page is being translated family by family. The research prose below is currently in English; the politics journey is already translated. Model labels, buttons and the rest of the site are in Chinese.`
     - zh-Hans: `本叙述页正在按家族逐步翻译。下方研究文字目前为英文；政治经济学页面已翻译。模型标签、按钮及站内其他界面均为中文。`
   - For politics (`ccpJourney`), a short positive note instead:
     - EN: `This narrated page is translated. Linked publications and data files keep their original language.`
     - zh-Hans: `本叙述页已翻译；链接的出版物与数据文件保留原文。`
   - Key these as two dictionary entries (e.g. `Narrated page: transcription in progress` / `Narrated page: translated`), so fr/vi can follow later.
2. **Replace the home-footer disclosure** (`ui-translations.json:1472`, `Library.tsx:273`) with one canonical sentence that names the exception:
   - EN: `The model library and interactive controls are translated into Chinese. Narrated model pages are being translated family by family (politics is translated); linked publications and archived research files keep their original language.`
   - zh-Hans: `模型库与交互控件已译为中文。叙述式模型页面正按家族逐步翻译（政治经济学已翻译）；链接的出版物与存档研究文件保留原文。`
3. **Delete/retire the orphaned variants** while doing this: `translations.json:17` and `translations.json:2212` (dead duplicates of the above), so there is exactly one disclosure string in the codebase.
4. **Why it matters beyond accuracy:** `translate()` silently falls back to English for every missing key, so without an explicit notice a Chinese reader cannot tell translated chrome from untranslated researched prose. The notice converts a seeming translation failure into a declared limitation — consistent with the site's own "label as a limit" style.
5. **Do not** claim "the narrated pages are in English" anywhere else (e.g. home hero, meta description) — politics makes that false; refer to "family by family" instead.

### Addendum — `fix/i18n-2` (PR #20, commit `d2b3d19`)

60 zh-Hans entries added for the rewired About/CTA strings + home/journey/beta/chart chrome; 64 existing zh strings normalised (bare `Atlas`, `parity`/`logistic`/`onset`/`Harvest`/`tipping`, `CCP bus`). Four keys deliberately skipped because `translate()`'s substring replacement would corrupt English prose in zh mode: `people` (46 rendered hits), `Limits` (2), `Teaching` (1), `Chapters` (1) — these need key namespacing. Workflow strings left to PR #18. Journeys prose untouched.
