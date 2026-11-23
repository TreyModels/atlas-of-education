# Paper M section 2: Credential inflation as a positional mechanism — a pre-registered test

*Draft section for the consolidated Massification paper (lead: panel-matrix). Source: care-credential @ e626cb8; the +0.81 correlation below was re-verified for this draft against the committed file `results/panel_cross_section.csv` (r = 0.807, n = 46). Traceability in `SOURCE_MAP.md`.*

## The prediction

The framework's credential-inflation story is positional. It is not that more schooling lowers
fertility because schooling is productive or because it raises income; it is that credentials are a
queue, and what matters is your *position* in the queue relative to the jobs that require
credentials. The sharp testable version is a gap measure: female tertiary attainment minus the
share of female jobs that are actually credentialed (managerial and professional occupations). If
the positional story is right, the gap should predict fertility *better* than attainment itself,
and it should do so especially in countries where attainment is already high and the queue is
saturated.

## The test and the data

The pre-registered test had two parts. B1: does the credential-occupation gap beat attainment in a
horse race for fertility? B2: does the gap predict better in high-attainment (saturated) countries
than in low-attainment ones? Data: ILO occupational employment (ISCO major groups 1–2,
managerial/professional) for 2019 and 2023, giving 49 countries with the credentialed-jobs share
and **46 usable countries** with female tertiary attainment, fertility and the gap; World Bank
female tertiary attainment and total fertility. This is a cross-section, one observation per
country, so no country fixed effects; the pre-registration fixed the specification and falsifiers
in advance.

## B1: the gap does not beat attainment — it carries almost no information

The correlation of fertility with the credential-occupation gap is **−0.15** (explaining about 2%
of variance, n = 46), against **−0.62** for female tertiary attainment and **−0.65** for the
credentialed-jobs share itself. In the horse race, attainment keeps a large negative coefficient
(**−0.81, t = −4.6**) while the gap turns **positive (+0.33, t = +1.9)** once attainment is in the
model — the pre-registered "sign is the opposite of predicted" falsifier. With income and
urbanisation added, attainment is **−0.80 (t = −2.85)**, the gap **+0.32 (t = +1.61)**, log income
−0.035 (t = −0.30) and urban +0.036 (t = 0.19).

The reason is visible in the data. Attainment and the credentialed-jobs share are almost the same
variable: their correlation is **+0.81** (re-verified at r = 0.807, n = 46, from the committed
panel). The gap is their difference, so it is a small, noisy residual rather than a queue position.
A positional theory needs the two components to move separately; in these data they do not.

## B2: the saturation prediction also fails

If credential inflation bites hardest where attainment is saturated, the gap should perform better
in high-attainment countries. It performs worse. In the 23 countries above median tertiary
attainment the model fits R² = 0.17; in the 23 below it, R² = 0.50, and the gap's coefficient is
larger and more precise in the *low*-attainment group. The saturation prediction is the reverse of
what the data show.

## The care-work context (reported here for the massification story; full test in the fertility paper)

The same record tested the care-work loop. The care share of female employment rises steeply with
female attainment — 8.1% in the bottom tercile, 19.0% in the middle, 28.4% at the top (n = 148) —
but the association is fully absorbed by income and urbanisation (attainment coefficient +0.009,
t = 0.17, once log GDP +0.242, t = 2.47 and urban +0.42, t = 3.38 are in), and the sector placebos
are decisive (male care +0.179, t = 2.10; manufacturing −0.189, t = −3.47). The massification
engine is not visible as a care-employment mechanism either.

## What the section claims, and what it does not

**Claim.** The credential-occupation gap, as measured here, is not a positional mechanism: it is
nearly collinear with attainment, carries about 2% of fertility variance on its own, flips to the
wrong sign once attainment is controlled, and fails the pre-registered saturation test. Credentials
may still be positional in ways this measure cannot capture — the measure uses occupation rather
than required education, and overeducation could not be constructed for this sample.

**What it does not claim.** Not that credential inflation is unreal, and not that signaling is
irrelevant to fertility. The claim is narrower and pre-registered: the specific gap measure the
framework proposes does not do the work the framework says it does, and the plain attainment
channel (correlation −0.62, surviving every control in the horse race) is what the data support.
The honest limits are the 46-country sample, the single cross-section, the occupational proxy for
"credentialed jobs", and the absence of an overeducation measure; each is declared in the record
rather than approximated.
