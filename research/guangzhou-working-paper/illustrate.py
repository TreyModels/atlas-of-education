"""Build the illustrated paper. Run with ReportLab, NumPy and Georgia/Arial or Liberation fonts."""
import csv, json
from pathlib import Path
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

D=Path(__file__).resolve().parent
for key,mac,linux in [('Body','Georgia.ttf','LiberationSerif-Regular.ttf'),('Title','Georgia Bold.ttf','LiberationSerif-Bold.ttf'),('Sans','Arial.ttf','LiberationSans-Regular.ttf'),('Bold','Arial Bold.ttf','LiberationSans-Bold.ttf')]:
    candidates=[Path('/System/Library/Fonts/Supplemental')/mac,Path('/usr/share/fonts/truetype/liberation2')/linux]
    pdfmetrics.registerFont(TTFont(key,next(str(x) for x in candidates if x.exists())))
rows=list(csv.DictReader((D/'draws.csv').open()))
rep=list(csv.DictReader((D/'repeats.csv').open()))
old=[json.loads(x) for x in (D/'archived_v8.jsonl').read_text().splitlines()]
def col(k):return np.array([float(r[k]) for r in rows])
def oldcol(k,field):return np.array([r[k][field] for r in old])
q=lambda x:np.quantile(x,[.05,.5,.95])
C=canvas.Canvas(str(D.parent/'Same Score Same Chance.pdf'),pagesize=(612,792),pageCompression=1)
C.setTitle('Same score, same chance? | Guangzhou working paper')
C.setAuthor('James W. Menefee III')
ink='#182F37'; teal='#006F68'; red='#A64B26'; soft='#DBE9E6'; muted='#486369'; light='#D1DDDC'; paper='#F7F7F2'
tag='https://github.com/TreyModels/atlas-of-education/releases/tag/v2026.11.27-guangzhou'
doi='https://doi.org/10.5281/zenodo.24369167'
def color(x):return HexColor(x)
def txt(x,y,s,size=11,font='Sans',c=ink):
    C.setFillColor(color(c));C.setFont(font,size);C.drawString(x,792-y,s)
def line(x,y,X,Y,c=light,w=1):
    C.setStrokeColor(color(c));C.setLineWidth(w);C.line(x,792-y,X,792-Y)
def rect(x,y,w,h,c):
    C.setFillColor(color(c));C.rect(x,792-y-h,w,h,fill=1,stroke=0)
def dot(x,y,r,c):
    C.setFillColor(color(c));C.circle(x,792-y,r,fill=1,stroke=0)
def para(y,s,x=48,w=516,size=12,font='Body',leading=None):
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.44,textColor=color(ink))
    p=Paragraph(s,st);_,h=p.wrap(w,900);p.drawOn(C,x,792-y-h)
    assert y+h < 745,(page,s[:65],y+h)
    return y+h+12
def head(n,section,title):
    global page
    page=n
    txt(48,38,'GUANGZHOU   /   SHADOW EDUCATION',8,'Bold',teal)
    txt(455,38,'WORKING PAPER   ·   2026',8,'Sans',muted)
    line(48,50,564,50);txt(48,82,section.upper(),9,'Bold',teal)
    txt(48,122,title,24,'Title')
def end():
    line(48,748,564,748);txt(48,765,'Menefee   /   Same score, same chance?',8,'Sans',muted);txt(544,765,str(page),9,'Bold',muted);C.showPage()
def sub(y,s):txt(48,y,s,14,'Bold',teal)
def caption(y,s):return para(y,s,size=9.5,font='Sans')
def link(url,s):return '<a href="'+url+'" color="#006F68"><u>'+s+'</u></a>'
head(1,'Research question','Same score, same chance?')
para(151,'Shadow education and the route to university in Guangzhou',size=17)
para(195,'James W. Menefee III   ·   27 November 2026',size=10,font='Sans')
y=para(246,'Imagine two pupils entering senior high school with the same exam score. One had strong teachers and private lessons. The other reached that score with fewer resources. If both later win university places at similar rates, what can we conclude about the fairness of the competition?',size=16,leading=23)
y=para(y,'We follow synthetic pupils through the zhongkao (senior-high entrance exam), school and class placement, tutoring and a ranked university-admission proxy. We ask how the answer changes when we compare families at the same entrance score, the same starting ability, or both.')
rect(48,y+1,516,93,soft)
para(y+14,'Across 1,024 simulated cohorts, the richer-to-poorer admission ratio was 0.91 at comparable entrance scores, 1.19 at comparable scores and starting ability, and 1.36 at comparable starting ability. All three statements describe the same model.',x=64,w=483,size=12)
y+=117
y=para(y,'The simulated spending decline aligns directionally with national household evidence. The equity change also depends on an unverified assumption about changes in class reassignment after 2021. Neither comparison identifies a Guangzhou policy effect.')
para(y,link(tag,'Paper, code, data and contribution details')+'  ·  '+link(doi,'Atlas collection DOI'),font='Sans',size=10)
end()
head(2,'Field evidence and scholarship','Where tutoring fits in the school day')
y=para(149,'At the author’s Guangzhou boarding school, evening study and weekend homework leave little time for paid lessons during term. A tutor interviewed for the study saw a different clientele: pupils seeking help with difficult material, ambitious pupils targeting a subject, and families buying holiday or full-time instruction. A single school and a single provider offer two windows on the market. Neither gives its citywide size.')
y=para(y,'Mark Bray (2007) defines shadow education by its relationship to mainstream schooling. As the curriculum or examination changes, the private lesson changes with it. Bray and Lykins (2012) distinguish the reach, intensity and forms of tutoring. Here, counting participants alone would give equal weight to a holiday lesson and a semester away from school. The model therefore distinguishes term, holiday and full-time provision.')
y=para(y,'Zhang and Bray (2021) trace how tutoring in urban China changes location and organizational form as the regulatory environment changes. Their account motivates asking where instruction moves when time or supply is constrained. Wang (2020) documented pupils in Taiyuan attending full-time providers while remaining enrolled elsewhere. The Guangzhou interview suggests a local instance. Its prevalence remains unknown.')
sub(y+16,'National survey evidence');y+=35
y=para(y,'The 2021 Double Reduction directive restricted academic tutoring during compulsory education (General Offices, 2021). Wei (2024, Figure 1) reports weighted participation in off-campus academic tutoring. The decline was already underway before the directive.')
xs=[77,192,307,422,537];vals=[36.1,21.9,23,16.5,13.5];years=['2017','2019','2021','2022','2023']
# Plot calendar time on a linear scale.
xs=[72+(int(v)-2017)*77 for v in years]
base=y+115
for i,(x,v) in enumerate(zip(xs,vals)):
    yy=base-v*2.3
    if i: line(xs[i-1],base-vals[i-1]*2.3,x,yy,teal,2.5)
    dot(x,yy,4,teal);txt(x-13,yy-10,f'{v:g}%',10,'Bold');txt(x-12,base+10,years[i],9,'Sans',muted)
caption(base+24,'Figure 1. National household survey estimates, 2017–2023. The source measures participation in academic tutoring. City-level changes and hours purchased are separate questions.')
end()
head(3,'Measurement','What does “the same” mean?')
y=para(149,'Richer and poorer mean the top and bottom 40% of simulated local-hukou families by wealth. For each group we calculate the share winning a seat. A ratio of 1.20 means 12 richer pupils would win for every 10 poorer pupils winning in equally sized groups. It does not mean a 20-percentage-point gap.')
sub(y+13,'Three comparisons of the same simulated system');y+=43
x0,x1=205,551
toX=lambda v:x0+(v-.55)/1.45*(x1-x0)
for t in [.6,1,1.4,1.8]:
    x=toX(t);line(x,y+4,x,y+131,teal if t==1 else light,1);txt(x-8,y+147,f'{t:.1f}',9,'Sans',muted)
for j,(k,label) in enumerate([('S','Entrance score'),('Sstar','Score and ability'),('T','Starting ability')]):
    l,m,h=q(col(k));yy=y+26+j*46;txt(48,yy+3,label,12,'Bold');line(toX(l),yy,toX(h),yy,teal,3);dot(toX(m),yy,5,teal);txt(toX(m)-12,yy-10,f'{m:.2f}',11,'Bold')
y=caption(y+162,'Figure 2. Dots mark medians. Lines span the 5th to 95th percentiles across model settings and synthetic cohorts. The reference at 1 means equal admission rates.')
y=para(y,'S and T use the highest fifth of entrance scores or simulated starting ability, respectively, split into ten equal-count bands. Within each band we calculate rich and poor rates, then divide their equally weighted averages. Cutoffs use the whole cohort. Wealth comparisons include local pupils who did not enter academic high school. Such pupils cannot win a seat in this model.')
y=para(y,'S* takes the highest fifth by entrance score and groups by both score and ability. Each retained cell needs at least five rich and five poor pupils. Both groups receive the same cell weights, proportional to their combined counts. The 5 × 5 grid retained a median 98.6% of eligible rich and poor pupils. In the archived study, 10 × 10 retained 92% and 20 × 20 retained 47%.')
para(y,'The archived unconditional ratio, with no score or ability restriction, was 2.34. Differences among these ratios cannot be added: each comparison asks about a different set or mix of pupils.',size=11)
end()
head(4,'Formal verification','Eight pupils explain the problem')
y=para(149,'Give all eight pupils identical starting ability. Four come from richer homes and four from poorer homes. Everyone scoring high wins a place. Three richer pupils and one poorer pupil score high. The example assumes a score distribution to establish what is logically possible.')
for j,(label,n) in enumerate([('Richer',3),('Poorer',1)]):
    yy=y+32+j*45;txt(65,yy+5,label,14,'Bold')
    for i in range(4):
        x=210+i*52;dot(x,yy,12,teal if i<n else '#DFE6E4');txt(x-4,yy+4,'H' if i<n else 'L',10,'Bold','#FFFFFF' if i<n else muted)
    txt(453,yy+5,f'{n} of 4 win',13,'Bold')
y=caption(y+108,'Figure 3. H = high score and admitted. L = low score and unadmitted. Both wealth groups contain pupils at both scores.')
y=para(y,'At either score, pupils receive exactly the same decision. Give the high and low score groups equal weight, and each wealth group’s standardized admission rate is one-half. Their ratio is 1. Across all pupils of this identical ability, however, the rates are three-quarters and one-quarter. Their ratio is 3. A score-based rule can therefore deliver exact score parity while family advantage enters upstream.')
sub(y+13,'What Lean checked');y+=31
y=para(y,'Lean 4.36.0 checked these rates by exact rational arithmetic. For any finite before-and-after roster, it also proved that gains in admissions equal losses whenever the total admitted stays fixed. For integer scores, increasing a rival’s score can only worsen or preserve a focal pupil’s rank. With one place and scores of 8 and 7, a two-point bonus to the second pupil displaces the first.')
y=para(y,'Banding uses a ranked list of distinct pupil IDs. Taking its first k IDs yields exactly the smaller of k and school size for every ranking, including a ranking containing score ties. University admission uses a different rule in Python: everyone at or above the cutoff qualifies. Two scores of 8 at a one-seat cutoff form a checked counterexample to universal exact capacity.')
para(y,'Scope: proofs apply to the stated mathematical rules. The finite tests below connect those rules to sampled Python outputs. Clinical, psychological or biological interpretations of “talent” are outside the model.',size=10,font='Sans')
end()
head(5,'Historical scenario','A smaller gap in most cohorts')
y=para(150,'We run the same parameter setting twice, starting with the same random seed. Both scenarios include boarding, holiday tutoring and alternative routes. The “before” scenario switches off the pre-gate tutoring restriction and senior-2 re-banding. This design pairs comparable settings and initial pupils. Later random events can differ when the scenarios follow different paths.')
delta=col('T')-col('T_before')
sub(y+13,'Change in the rich-to-poor ratio at comparable ability');y+=35
step=.025;edges=np.arange(np.floor(delta.min()/step)*step,np.ceil(delta.max()/step)*step+step*1.5,step)
counts,edges=np.histogram(delta,edges);base=y+115
hx=lambda v:65+(v-edges[0])/(edges[-1]-edges[0])*480
for a,b,n in zip(edges,edges[1:],counts):
    h=100*n/max(counts);rect(hx(a),base-h,hx(b)-hx(a)-1,h,teal if b<.000001 else red)
line(hx(0),y+6,hx(0),base+6,ink);txt(hx(0)-18,y,'No change',9,'Bold')
for t in [-.3,-.2,-.1,0,.1,.2]:
    if edges[0]<=t<=edges[-1]:txt(hx(t)-9,base+14,f'{t:.1f}',9,'Sans',muted)
y=caption(base+25,'Figure 4. Each bar counts configurations in a 0.025-wide interval. Bars to the left of zero show a narrower rich-to-poor gap. The median paired change was −0.051. The middle 90% ranged from −0.188 to +0.052.')
y=para(y,'T fell in 807 of 1,024 draws (78.8%). A 95% Wilson interval for repeated sampling from this specified design is 76.2%–81.2%. The archived Latin-hypercube experiment gave 126 of 150 (84%). For the larger experiment, median T was 1.41 before and 1.36 under the current scenario. Median paired tutoring expenditure fell ¥5,069 over five school years (middle 90%: ¥405–¥12,424 saved).')
y=para(y,'A separate test held each of 128 new parameter settings fixed and generated eight cohorts per setting. At 75 settings the direction of change differed between cohorts. The pooled within-setting standard deviation of the paired change was 0.056. The estimated between-setting standard deviation of the mean change was 0.042 after subtracting sampling variation. This explains why a single cohort per setting can give an unstable sign.')
para(y,'The archived design attributed a median −0.017 in T to the restriction and −0.036 to re-banding by averaging each change over both orders of introduction. Spending levels were ¥35,838 before (¥23,474–¥46,359) and ¥28,771 after (¥19,886–¥41,678). No longitudinal Guangzhou series establishes that re-banding intensified after 2021.',size=10.5)
end()
head(6,'Mechanisms','Who gets a seat after a bonus?')
y=para(148,'Hold pupils, academic eligibility and exam scores fixed. Rank academic pupils once by their ordinary exam scores, then again after applying the modeled art and joint-exam bonuses. Count pupils admitted under the first ranking who lose their place in the second. This isolates the effect of ranking rules in the simulation.')
sub(y+14,'4,000 seats in each ranking');y+=34
rect(49,y+15,510,32,soft);rect(49,y+15,510*187/4000,32,red)
line(61,y+47,61,y+62,red);txt(49,y+79,'187 seats change hands',12,'Bold',red);txt(288,y+79,'3,813 keep the same pupil',12,'Bold',teal)
y=caption(y+94,'Figure 5. Median displacement, a 4.7% turnover of seats. The middle 90% ranged from about 53 to 418 seats. Counting everyone who uses a route would also count candidates who would have won anyway.')
y=para(y,'Every one of the 1,024 current-scenario cohorts allocated exactly 4,000 places under each ranking. Every gain matched a loss, and every new winner received a bonus. Both class placements met the intended headcount at every represented school. Continuous synthetic scores made cutoff ties uncommon. Real exam systems need an explicit tie rule.')
sub(y+14,'Where does the remaining advantage come from?');y+=35
y=para(y,'In the archived 150-draw intervention, disabling term and holiday tutoring, full-time instruction and both route bonuses reduced median S* from 1.19 to 1.09. The median within-draw share of excess above parity removed was 49%. The residual is consistent with earlier advantages persisting and with pupils differing within score-and-ability cells. Its precise source remains unresolved.')
y=para(y,'The ordinary-exam ranking gave a lower rich-family advantage under T (1.25 against 1.35) and S* (1.11 against 1.19). Under S, its ratio of 0.85 lay farther from equal admission rates than 0.91. A claim that one ranking is “fairer” therefore requires a choice of criterion.')
para(y,'A real art or joint-exam applicant faces distinct eligibility rules, academic and specialist requirements, and capacities. The single-ranking bonus is an approximation. The model cannot estimate how many actual Guangzhou places changed hands.',size=11)
end()
head(7,'Sensitivity','How long does an early advantage last?')
y=para(149,'Earlier research models accumulated skills and measures teacher-effect persistence (Cunha &amp; Heckman, 2007; Jacob et al., 2010). Here, home inputs, junior-school teaching and tutoring enter one stock. At senior 2, a fraction of this stock fades. We varied that fraction between 0% and 90%. If earlier advantages persist, families’ circumstances at age 15 matter longer. This is a structural assumption with little direct local evidence.')
sub(y+12,'Admission ratio at comparable starting ability');y+=36
x0,x1=172,501
def fx(v):return x0+(v-.9)/1.3*(x1-x0)
for t in [1,1.4,1.8,2.2]:
    line(fx(t),y,fx(t),y+152,teal if t==1 else light);txt(fx(t)-8,y+167,f'{t:.1f}',9,'Sans',muted)
for j in range(6):
    ii=(col('DECAY')>=j*.15)&(col('DECAY')<(j+1)*.15);lo,m,hi=q(col('T')[ii]);yy=y+12+25*j
    txt(53,yy+4,f'{15*j}–{15*(j+1)}% fades',10,'Sans');line(fx(lo),yy,fx(hi),yy,teal,2);dot(fx(m),yy,4,teal);txt(518,yy+4,f'{m:.2f}',10,'Bold')
y=caption(y+179,'Figure 6. Medians and middle 90% of current-scenario ratios within six parameter bands, from the new 1,024 draws. Other parameters and pupils also vary within each band. This is a sensitivity comparison.')
y=para(y,'In the archived paired interventions, removing the wealth-linked home input removed a median 44% of excess T above 1. Removing the zone gradient in teacher inputs removed 22%, and setting pre-gate tutoring effectiveness to zero removed 8%. Removing all three together removed 74%. The corresponding median changes in mean academic-track skill were 0.00, 0.00, −0.02 and −0.02 model units.')
y=para(y,'The small mean changes partly reflect additive learning: a gain for one pupil can offset a loss for another. These interventions say where the simulated gap comes from. Their costs and practical feasibility were never estimated. Diminishing returns, interactions and distinct persistence rates could alter the result.')
para(y,'The most informative new evidence would link zhongkao subject results to later term scores, class and teacher assignments, senior-2 reassignments, family resources, tutoring histories and gaokao outcomes. Even one school could test the timing of re-banding and the persistence of early score differences.',size=10.5)
end()
head(8,'Research design','What the equations assume')
items=[
('Class provision','In N1, a pupil’s later score combines early skill, school value added, teaching, peers and tutoring. In the implementation, only top-band pupils receive a fixed teacher and peer premium. Entry classes use zhongkao rank. Senior-2 classes use a weighted mix of entry and later performance ranks. Each nonempty school takes at least one top-band pupil, otherwise the nearest integer to one-eighth of enrollment.'),
('The school-choice margin','N2 subtracts the expected loss of top-class access from a stronger school’s value added. Suppose the school adds 0.20 skill units, the top class adds 0.44, and the chance of that class falls from 65% to 15%. The net is 0.20 − 0.44 × 0.50 = −0.02. This example holds other channels fixed.'),
('Why families buy tutoring','N3 proposes that families weigh price against the risk of missing a consequential threshold. A marginal benefit calculation describes an interior candidate. The optimum can also be zero or all affordable hours. Python uses a simpler demand rule: both tails have four times the middle group’s base weight, wealth increases demand, and one round of class-average demand influences take-up. A monotonicity proof for the insurance term alone cannot characterize total demand.'),
('How a seat is won','N4 describes separate gates with their own eligibility and capacities. The frozen simulation implements one ranking. Its 4,000-seat target equals 10% of the whole synthetic age cohort, with only academic-track students eligible. Wealth-related selection into proxy routes is an assumption. No full matching market or response of all families to one another’s investments is estimated.'),
('What a regression recovers','Bray (2014) explains why research on tutoring effects is difficult to compare. Families select tutoring for different reasons and buy different amounts. A coefficient comparing any tutoring with none also combines term and holiday doses. Manski (1993) identifies a related difficulty for peer effects. The archived peer coefficient and simulated band premium use different units, leaving quantitative recovery unresolved.')]
y=150
for h,body in items:
    sub(y+11,h);y=para(y+22,body,size=10.8)
end()
head(9,'Calibration and participation','What public data can improve')
y=para(149,'China has household and classroom microdata suited to this question. Three public sources already constrain parts of the model. Their populations and questions differ, so each has a specific use.')
sub(y+14,'School and family surveys');y+=35
y=para(y,'In the China Education Panel Survey, baseline parent questions A2–A3 ask whether a child attended cram school or an extracurricular course that semester and what the family paid. The 2013–14 baseline covers grades 7 and 9 across 438 classes and 112 schools. Estimate weighted participation and semester spending, including zero spenders. The broad item mixes academic and other courses, and the cohort predates Double Reduction (National Survey Research Center, 2014).')
y=para(y,'China Family Panel Studies provides household resources and longitudinal family information through an application for public-use files. Match child and household identifiers, check definitions by wave and use survey weights and sampling units. For expenditure comparisons, harmonize recall periods and prices. Public files mask locations below province level, so claiming a Guangzhou city estimate from them would be unjustified (Institute of Social Science Survey, n.d.).')
sub(y+12,'Local administrative anchors');y+=33
y=para(y,'Guangzhou reports 31,858 quota places across 491 receiving junior schools in 2026. Eligible high schools allocate at least 50% of planned places. Public-school migrant caps span 8%–18%. The model sweeps 30%–60% for allocation and 8%–20% for caps, applied at an aggregated tier. Of 1,024 draws, 284 satisfy both numerical limits. T fell in 78.5% of that subset, with median change −0.051. This post-hoc check still abstracts from school-specific rules (Guangzhou Admissions Office, 2026a, 2026b, 2026c).')
sub(y+11,'An invitation to contribute');y+=32
para(y,'The '+link(tag,'GitHub release')+' includes every parameter range, fixed assumption, public benchmark, proof and synthetic result. Contributions can take the form of an issue or a pull request. Please identify the parameter, population, years, units, exact source or table, and the proposed range. Estimates of separate home, school and tutoring persistence would be especially valuable. Aggregate evidence and shareable code are welcome.',size=11)
end()
head(10,'Methods and research record','How to reproduce the comparisons')
y=para(150,'The frozen generator is gz_v5.py (v5.1, archive commit 2082f47). The archived v8 experiment used 150 Latin-hypercube settings and cohorts of 40,000. Recalculating every line of its summary from the archived draw table reproduced its published values. The new experiments are exploratory extensions. All reported quantiles give each independent design draw equal weight.')
y=para(y,'For the primary extension, 31 inputs were sampled independently and uniformly across the archived ranges. One fresh cohort was generated for each of 1,024 parameter vectors. Each paired comparison reused the same vector and initial seed. The collection is an experiment over a chosen distribution of possible worlds. Its frequencies depend on the endpoints, independence assumption and uniform weights (Morris et al., 2019).')
y=para(y,'The second experiment crossed 128 fresh parameter settings with eight seeds each. For change in T, the within-setting variance is the mean of the 128 sample variances. The variance of setting means includes cohort variance divided by eight, which we subtracted to estimate between-setting variance. The unit for uncertainty about settings is the setting. Treating eight replicates as eight new parameter settings would understate uncertainty.')
y=para(y,'A local run and a Linux server run using different NumPy patch versions generated identical primary CSV bytes (SHA-256 in the package). This checks implementation reproducibility across two environments. Both executed the same code. Independent reimplementation, calibration on Guangzhou pupils, and independent statistical peer review remain open.')
y=para(y,'The model was informed by the author’s observations and one confidential conversation with a tutoring provider in November 2026. Prices, schedules and client descriptions are contextual field evidence. The release contains synthetic draw-level results and source-linked aggregate benchmarks. Interview transcripts, recordings and pupil records are excluded. The author’s archived account reports consent; this analysis does not independently authenticate the consent record or establish institutional ethics approval.')
para(y,'The full manuscript, archived scenario comparisons, checked Lean source, axiom output and input dictionary accompany this edition. The collected Atlas models have a '+link(doi,'collection DOI')+'. The '+link(tag,'versioned release')+' identifies this paper and its exact package. The simulation can be rerun independently of this document.',size=11)
end()
head(11,'Sources','References')
refs=[
('Bray, M. (2007). <i>The shadow education system: Private tutoring and its implications for planners</i> (2nd ed.). UNESCO International Institute for Educational Planning.','https://etico.iiep.unesco.org/sites/default/files/2017-09/118486e.pdf'),
('Bray, M. (2014). The impact of shadow education on student academic achievement: Why the research is inconclusive and what can be done about it. <i>Asia Pacific Education Review, 15</i>(3), 381–389.','https://doi.org/10.1007/s12564-014-9326-9'),
('Cunha, F., &amp; Heckman, J. (2007). The technology of skill formation. <i>American Economic Review, 97</i>(2), 31–47.', 'https://doi.org/10.1257/aer.97.2.31'),
('Bray, M., &amp; Lykins, C. (2012). <i>Shadow education: Private supplementary tutoring and its implications for policy makers in Asia.</i> Asian Development Bank &amp; Comparative Education Research Centre, University of Hong Kong.','https://www.adb.org/sites/default/files/publication/29777/shadow-education.pdf'),
('General Office of the Central Committee of the Communist Party of China, &amp; General Office of the State Council. (2021, July 24). <i>Opinions on further reducing homework and off-campus training burdens for students in compulsory education</i> [Policy directive, in Chinese].','https://www.moe.gov.cn/jyb_xxgk/moe_1777/moe_1778/202107/t20210724_546576.html'),
('Guangzhou Admissions Office. (2026a). <i>Notice on quota allocation for ordinary senior high schools in 2026</i> [In Chinese].','https://jyj.gz.gov.cn/gk/zfxxgkml/ywgz/zsks/content/post_10788402.html'),
('Guangzhou Admissions Office. (2026b, May 12). <i>Results of the 2026 quota allocation lottery</i> [In Chinese].','https://gzzk.gz.gov.cn/zkzz/zkxx/zkzx/content/post_10809606.html'),
('Guangzhou Admissions Office. (2026c). <i>Third- and fourth-batch ordinary high school admissions completed</i> [In Chinese].','https://gzzk.gz.gov.cn/gkmlpt/content/10/10910/post_10910997.html'),
('Institute of Social Science Survey, Peking University. (n.d.). <i>China Family Panel Studies: Public-use and restricted data access guidelines.</i>','https://www.isss.pku.edu.cn/cfps/en/data/restricted/index.htm'),
('Jacob, B. A., Lefgren, L., &amp; Sims, D. P. (2010). The persistence of teacher-induced learning. <i>Journal of Human Resources, 45</i>(4), 915–943.', 'https://doi.org/10.3368/jhr.45.4.915'),
('Manski, C. F. (1993). Identification of endogenous social effects: The reflection problem. <i>The Review of Economic Studies, 60</i>(3), 531–542.','https://doi.org/10.2307/2298123'),
('Morris, T. P., White, I. R., &amp; Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. <i>Statistics in Medicine, 38</i>(11), 2074–2102.','https://doi.org/10.1002/sim.8086'),
('National Survey Research Center, Renmin University of China. (2014). <i>China Education Panel Survey: Baseline parent questionnaire, 2013–2014.</i>','https://ceps.ruc.edu.cn/Enlish/dfiles/11184/14391214047032.pdf'),
('Wang, F. (2020, November 26). Students retain school enrollment while training providers offer full-time schooling [In Chinese]. <i>Xinhua.</i>','https://www.xinhuanet.com/politics/2020-11/26/c_1126790587.htm'),
('Wei, Y. (2024). Short-term effects of burden-reduction policy: Evidence from the China household survey of education finance [In Chinese]. <i>China Education Finance</i> (No. 11, cumulative No. 255). Peking University.','https://ciefr.pku.edu.cn/docs/2024-12/bcd3767a1681440c99e79c5c9e94fcd0.pdf'),
('Zhang, W., &amp; Bray, M. (2021). A changing environment of urban education: Historical and spatial analysis of private supplementary tutoring in China. <i>Environment and Urbanization, 33</i>(1), 43–62.','https://doi.org/10.1177/0956247820981820')]
y=150
for i,(ref,url) in enumerate(refs):
    if i==9:
        end();head(12,'Sources','References and research materials');y=150
    y=para(y,ref+' '+link(url,url if 'doi.org' in url else 'Source'),size=10.5)
end();C.save()
