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
summary=json.loads((D/'summary.json').read_text())
mechanism=json.loads((D/'mechanism_summary.json').read_text())
med=lambda key: summary[key]['median']
mm=lambda scenario,key: mechanism[scenario][key]['median']
def col(k):return np.array([float(r[k]) for r in rows])
q=lambda x:np.quantile(x,[.05,.5,.95])
C=canvas.Canvas(str(D.parent/'Same Score Same Chance.pdf'),pagesize=(612,792),pageCompression=1)
C.setTitle('Same score, same chance? | Guangzhou working paper')
C.setAuthor('James W. Menefee III')
ink='#182F37'; teal='#006F68'; red='#A64B26'; soft='#DBE9E6'; muted='#486369'; light='#D1DDDC'; paper='#F7F7F2'
tag='https://github.com/TreyModels/atlas-of-education/releases/tag/v2026.11.27-guangzhou-r2'
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
page=0
def head(n,section,title):
    global page
    page+=1
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
y=para(y,'We follow synthetic pupils through the zhongkao (senior-high entrance exam), school and class placement, tutoring and a ranked university-admission proxy. We ask how the answer changes when we compare families at comparable entrance-score bands, comparable modeled starting-ability bands, or both.')
rect(48,y+1,516,93,soft)
para(y+14,'Across 1,024 simulated cohorts, the richer-to-poorer admission ratio was 0.91 at comparable entrance scores, 1.19 at comparable scores and starting ability, and 1.41 at comparable starting ability. All three statements describe the same model.',x=64,w=483,size=12)
y+=117
y=para(y,'The simulated spending decline aligns directionally with national household evidence. The equity change also depends on an unverified assumption about changes in class reassignment after 2021. Neither comparison identifies a Guangzhou policy effect.')
para(y,link(tag,'Paper, code, data and contribution details')+'  ·  '+link(doi,'Atlas collection DOI'),font='Sans',size=10)
end()
head(2,'Field evidence and scholarship','Where tutoring fits in the school day')
y=para(149,'At the author’s Guangzhou boarding school, evening study and weekend homework leave little time for paid lessons during term. A tutor interviewed for the study saw a different clientele: pupils seeking help with difficult material, ambitious pupils targeting a subject, and families buying holiday or full-time instruction. A single school and a single provider offer two windows on the market. Neither gives its citywide size.')
y=para(y,'Mark Bray (2007) defines shadow education by its relationship to mainstream schooling. As the curriculum or examination changes, the private lesson changes with it. Bray and Lykins (2012) distinguish the reach, intensity and forms of tutoring. Here, counting participants alone would give equal weight to a holiday lesson and a semester away from school. The model therefore distinguishes term, holiday and full-time provision.')
y=para(y,'Zhang and Bray (2021) trace how tutoring in urban China changes location and organizational form as the regulatory environment changes. Their account motivates asking where instruction moves when time or supply is constrained. Wang (2020) documented pupils in Taiyuan attending full-time providers while remaining enrolled elsewhere. The Guangzhou interview suggests a local instance. Its prevalence remains unknown.')
sub(y+16,'National survey evidence');y+=35
y=para(y,'The 2021 Double Reduction directive restricted academic tutoring during compulsory education (General Office of the CCP Central Committee &amp; General Office of the State Council, 2021). Wei (2024, Figure 1) reports weighted participation in off-campus academic tutoring. The decline was already underway before the directive.')
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
head(0,'Evidence and calibration','What informs the assumptions?')
y=para(150,'Liu et al. (2024) surveyed 486 parents and interviewed 23 in a Guangzhou school setting. Their retrospective accounts connect socioeconomic resources with tutoring choices and spending. Liu and Bray (2025) document continuing demand through hidden channels. These studies motivate a wealth gradient in effective restrictions, but do not estimate the coefficient used here.')
y=para(y,'Effective restriction is clipped to [0,1] and equals BAN_RED × [1 + BAN_GRAD × (1 − 2 × wealth rank)]. BAN_GRAD ranges from 0 to 1. Zero gives a uniform reduction. At one, the poorest pupils face up to twice the central reduction, while the wealthiest face nearly none. This is a sensitivity specification.')
y=para(y,'Wu et al. (2019) estimate a 0.435 SD final-exam effect of magnet-class enrollment near a cutoff in one rural county. Their suggestive decomposition puts the teacher component at about 40% of the peer component, roughly 29/71 of the total. Our default cumulative premiums are 0.15 and 0.29. Each is halved at each of two stages. Both are independently varied from 0.10 to 0.35; these ranges and the stage allocation are assumptions.')
y=para(y,'School effects vary across settings (Park et al., 2015; Dee &amp; Lan, 2015). Tutoring findings also depend on design and measurement (Zhang, Y., 2013; Zhang, L., 2024; Zhang, Z., et al., 2025). None directly calibrates our entire synthetic Guangzhou cohort. Literature estimates motivate mechanisms and sensitivity ranges rather than a fitted population prediction.')
para(y,'Bray’s (2024) timescapes perspective motivates distinguishing term and holiday provision. Zhang (2023) examines regulatory responses internationally. Zhang and Bray (2018) connect tutoring access with tracking; Reardon et al. (2016) model college sorting. Zhou (2019) explains selection concerns when conditioning on credentials, a related problem in a different setting.',size=11)
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
y=para(y,'S* takes the highest fifth by entrance score and groups by both score and ability. Each retained cell needs at least five rich and five poor pupils. Both groups receive the same cell weights, proportional to their combined counts. The 5 × 5 grid retained a median 98.6% of eligible rich and poor pupils. In the 150-setting grid experiment, the corresponding support at 10 × 10 and 20 × 20 was 91% and 45%.')
para(y,'The unconditional ratio in the 150-setting mechanism experiment, with no score or ability restriction, was 2.56. Differences among these ratios cannot be added: each comparison asks about a different set or mix of pupils.',size=11)
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
y=para(y,'Lean 4.36.0 checked these rates by exact rational arithmetic. For any finite list of before/after Boolean admission indicators, gains equal losses when the two admission totals are equal. For integer scores, increasing a rival’s score can only worsen or preserve a focal pupil’s rank. With one place and scores of 8 and 7, a two-point bonus to the second pupil displaces the first.')
y=para(y,'Banding uses a ranked list of distinct pupil IDs. Taking its first k IDs yields exactly the smaller of k and school size for every ranking, including a ranking containing score ties. University admission uses a different rule in Python: everyone at or above the cutoff qualifies. Two scores of 8 at a one-seat cutoff form a checked counterexample to universal exact capacity.')
para(y,'Scope: proofs apply to the stated mathematical rules. The finite tests below connect those rules to sampled Python outputs. Clinical, psychological or biological interpretations of “talent” are outside the model.',size=10,font='Sans')
end()
head(5,'Paired model scenarios','A small and uncertain equity change')
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
y=caption(base+25,'Figure 4. Each bar counts configurations in a 0.025-wide interval. Bars to the left of zero show a narrower rich-to-poor gap. The median paired change was −0.013. The middle 90% ranged from −0.123 to +0.093.')
y=para(y,'T fell in 598 of 1,024 draws (58.4%). A Wilson 95% interval for repeated sampling from this design is 55.4%–61.4%. Median T was 1.42 in the no-restriction/no-reband scenario and 1.41 in the baseline. Median paired tutoring spending fell ¥4,159 over five school years (middle 90%: ¥336–¥10,642 saved). The paired comparison provides weak evidence of a consistent equity direction within the design.')
y=para(y,'At 128 independently sampled settings, each repeated with eight cohorts, 119 settings produced both positive and negative paired changes. The pooled within-setting standard deviation was 0.057, compared with a between-setting standard deviation of 0.031 after subtracting cohort variation. The direction of a small change is therefore sensitive to the generated cohort.')
para(y,'A two-factor decomposition at 150 settings gave median contributions to T of −0.006 from the restriction and −0.005 from re-banding. These are hypothetical contributions averaged over both introduction orders. No longitudinal Guangzhou series establishes that re-banding intensified after 2021.',size=10.5)
end()
head(0,'Restriction-only sensitivity','Who can evade the restriction?')
y=para(150,'The isolated restriction comparison sets BAN_RED to zero while keeping senior-2 re-banding on. Across all 1,024 settings, the median effect on T is −0.0047 (middle 90%: −0.073 to +0.056). T falls in 585 runs (57.1%; Wilson 95%: 54.1%–60.1%). This small effect differs from the combined scenario comparison.')
y=para(y,'To examine the enforcement gradient directly, we hold each of 256 parameter settings fixed and compare BAN_GRAD = 0, 0.5 and 1. The no-restriction comparison uses the same initial seed and setting. Other simulated events can diverge as pupils follow different paths.')
sub(y+12,'Median restriction-only change in T');y+=38
for i,row in enumerate(mechanism['enforcement']):
    yy=y+i*53
    txt(50,yy+4,'Gradient '+str(row['gradient']),11,'Bold')
    lo,mid,hi=row['p05'],row['median'],row['p95']
    xx=lambda v: 370+v*1100
    line(xx(lo),yy,xx(hi),yy,teal,2);dot(xx(mid),yy,5,teal)
    txt(500,yy+4,f"{mid:+.4f}",11,'Bold')
line(370,y-14,370,y+122,muted,1)
y=caption(y+145,'Lines show the middle 90% across settings. Zero is unchanged equity. Positive values mean a higher rich-to-poor ratio under the restriction.')
y=para(y,'At gradient 1, the median is +0.0009 and T falls in 123 of 256 settings (48.0%). This does not demonstrate a robust increase. It shows that the direction of a small modeled restriction effect can reverse when informal access is strongly wealth-graded.')
para(y,'Yang (2026) likewise models how imperfect enforcement and unequal informal access can change distributional outcomes. Its overlapping-generations analysis and our scenario exercise have different structures. Neither comparison identifies the observed causal effect of Double Reduction.',size=11)
end()
head(6,'Mechanisms','Who gets a seat after a bonus?')
y=para(148,'Hold pupils, academic eligibility and exam scores fixed. Rank academic pupils once by their ordinary exam scores, then again after applying the modeled art and joint-exam bonuses. Count pupils admitted under the first ranking who lose their place in the second. This isolates the effect of ranking rules in the simulation.')
sub(y+14,'4,000 seats in each ranking');y+=34
rect(49,y+15,510,32,soft);rect(49,y+15,510*189/4000,32,red)
line(61,y+47,61,y+62,red);txt(49,y+79,'189 seats change hands',12,'Bold',red);txt(288,y+79,'3,811 keep the same pupil',12,'Bold',teal)
y=caption(y+94,'Figure 5. Median displacement, a 4.7% turnover of seats. The middle 90% ranged from about 52 to 422 seats. Counting everyone who uses a route would also count candidates who would have won anyway.')
y=para(y,'Every one of the 1,024 current-scenario cohorts allocated exactly 4,000 places under each ranking. Every gain matched a loss, and every new winner received a bonus. Both class placements met the intended headcount at every represented school. Continuous synthetic scores made cutoff ties uncommon. Real exam systems need an explicit tie rule.')
sub(y+14,'Where does the remaining advantage come from?');y+=35
y=para(y,'In the 150-setting intervention experiment, disabling term and holiday tutoring, full-time instruction and the mutually exclusive route bonuses reduced median S* from 1.19 to 1.10. The median within-draw share of excess above parity removed was 50%. The residual is consistent with earlier advantages persisting and with pupils differing within score-and-ability cells. Its precise source remains unresolved.')
y=para(y,'The ordinary-exam ranking gave a lower rich-family advantage under T (1.33 against 1.42) and S* (1.11 against 1.19) in the same 150-setting sample. Under S, its ratio of 0.87 lay farther from equal admission rates than 0.91. A claim that one ranking is “fairer” therefore requires a choice of criterion.')
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
y=para(y,'In the paired intervention experiment, removing the wealth-linked home input removed a median 47% of excess T above 1. Removing the zone gradient in teacher inputs removed 26%, and setting pre-gate tutoring effectiveness to zero removed 10%. Removing all three together removed 78%. The corresponding median changes in mean academic-track skill were 0.00, 0.00, −0.02 and −0.02 model units.')
y=para(y,'The small mean changes partly reflect additive learning: a gain for one pupil can offset a loss for another. These interventions say where the simulated gap comes from. Their costs and practical feasibility were never estimated. Diminishing returns, interactions and distinct persistence rates could alter the result.')
para(y,'The most informative new evidence would link zhongkao subject results to later term scores, class and teacher assignments, senior-2 reassignments, family resources, tutoring histories and gaokao outcomes. Even one school could test the timing of re-banding and the persistence of early score differences.',size=10.5)
end()
head(8,'Research design','What the equations assume')
items=[
('Class provision','In N1, a pupil’s later score combines early skill, school value added, teaching, peers and tutoring. In the implementation, each stage adds half the cumulative teacher and peer premiums. A pupil in the top band at both stages receives their sum. Wu et al. (2019) motivate the cumulative scale; its equal allocation across stages is assumed. Entry classes use zhongkao rank. Senior-2 classes use a weighted mix of entry and later performance ranks. Each nonempty school takes at least one top-band pupil, otherwise the nearest integer to one-eighth of enrollment.'),
('The school-choice margin','N2 subtracts the expected loss of top-class access from a stronger school’s value added. Suppose the school adds 0.20 skill units, the top class adds 0.44, and the chance of that class falls from 65% to 15%. The net is 0.20 − 0.44 × 0.50 = −0.02. This example holds other channels fixed.'),
('Why families buy tutoring','N3 proposes that families weigh price against the risk of missing a consequential threshold. A marginal benefit calculation describes an interior candidate. The optimum can also be zero or all affordable hours. Python uses a simpler demand rule: both tails have four times the middle group’s base weight, wealth increases demand, and one round of class-average demand influences take-up. A monotonicity proof for the insurance term alone cannot characterize total demand.'),
('How a seat is won','N4 describes separate gates with their own eligibility and capacities. The frozen simulation implements one ranking. Its 4,000-seat target equals 10% of the whole synthetic age cohort, with only academic-track students eligible. Wealth-related selection into proxy routes is an assumption. No full matching market or response of all families to one another’s investments is estimated.'),
('What a regression recovers','Bray (2014) explains why research on tutoring effects is difficult to compare. Families select tutoring for different reasons and buy different amounts. The regression diagnostics require further validation: a coefficient comparing any tutoring with none combines term and holiday doses. Manski (1993) identifies a related difficulty for peer effects. The estimated peer coefficient and simulated band premium use different units, leaving quantitative recovery unresolved.')]
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
y=para(y,'Guangzhou reports 31,858 quota places across 491 receiving junior schools in 2026. Eligible high schools allocate at least 50% of planned places. Public-school migrant caps span 8%–18%. The model sweeps 30%–60% for allocation and 8%–20% for caps, applied at an aggregated tier. Of 1,024 draws, 284 satisfy both numerical limits. T fell in 58.1% of that subset, with median change −0.014. This post-hoc check still abstracts from school-specific rules (Guangzhou Admissions Office, 2026a, 2026b, 2026c).')
sub(y+11,'An invitation to contribute');y+=32
para(y,'The '+link(tag,'research repository')+' includes every parameter range, fixed assumption, public benchmark, proof and synthetic result. Contributions can take the form of an issue or a pull request. Please identify the parameter, population, years, units, exact source or table, and the proposed range. Estimates of separate home, school and tutoring persistence would be especially valuable. Aggregate evidence and shareable code are welcome.',size=11)
end()
head(10,'Methods and research record','How to reproduce the comparisons')
y=para(150,'The analysis uses synthetic cohorts of 40,000 pupils. The principal experiment samples 1,024 parameter settings independently. Mechanism ablations and the factorial decomposition reuse the first 150 settings, while a separate experiment repeats 128 settings across eight cohorts each. A further check fixes the enforcement gradient at three values on 256 settings. All experiments are exploratory. Reported quantiles give each setting equal weight within its experiment.')
y=para(y,'For the principal experiment, 32 inputs were sampled independently and uniformly over the ranges in the parameter register. One fresh cohort was generated for each of 1,024 parameter vectors. Each paired comparison reused the same vector and initial seed. The collection is an experiment over a chosen distribution of possible worlds. Its frequencies depend on the endpoints, independence assumption and uniform weights (Morris et al., 2019).')
y=para(y,'The second experiment crossed 128 fresh parameter settings with eight seeds each. For change in T, the within-setting variance is the mean of the 128 sample variances. The variance of setting means includes cohort variance divided by eight, which we subtracted to estimate between-setting variance. The unit for uncertainty about settings is the setting. Treating eight replicates as eight new parameter settings would understate uncertainty.')
y=para(y,'The packaged outputs were regenerated locally after the cumulative-premium, enforcement-gradient and route-exclusivity corrections. Deterministic seeds, regression checks and file checksums support reproduction. These corrected outputs have not been independently reproduced on another machine. Independent reimplementation, calibration on Guangzhou pupils, and independent statistical peer review remain open.')
y=para(y,'The model was informed by the author’s observations and one confidential conversation with a tutoring provider in November 2026. Prices, schedules and client descriptions are contextual field evidence. The accompanying data contain synthetic draw-level results and source-linked aggregate benchmarks. Interview transcripts, recordings and pupil records are excluded. The conversation is informal context. The study does not establish documented consent for public dissemination or institutional ethics approval.')
para(y,'Detailed equations, scenario comparisons, Lean proofs and the parameter register accompany the paper. The research materials are available through the '+link(doi,'data and code archive')+'. '+link(tag,'Download the reproducibility package')+'. AI tools assisted drafting, programming and figure preparation; the author is responsible for the interpretation.',size=11)
end()
head(11,'Verification and sensitivity','Which assumptions matter most?')
y=para(150,'We ranked all 32 sampled inputs and each outcome, then removed the linear rank association with the other 31 inputs. The remaining correlation is a partial rank correlation (PRCC). This is a diagnostic for approximately monotone relationships over our chosen ranges, not a causal effect or a share of variance. The full table also reports ordinary Spearman correlations.')
sub(y+12,'Largest associations with the equal-ability ratio T');y+=40
sens=list(csv.DictReader((D/'sensitivity.csv').open()))
top=sorted([r for r in sens if r['outcome']=='T'],key=lambda r:abs(float(r['prcc'])),reverse=True)[:5]
for r in top:
    value=float(r['prcc']);txt(48,y+12,r['parameter'],10,'Bold');line(330,y+6,330,y+19,muted)
    rect(min(330,330+value*150),y+5,abs(value)*150,12,teal if value>0 else red)
    txt(500,y+15,f'{value:+.2f}',11,'Bold');y+=32
y=para(y+10,'Negative values mean larger input values tend to accompany smaller T after controlling the other input ranks. DECAY is the fraction of early advantage that disappears. HOME is the wealth-related home input. TEACH_SD also sets senior-high teacher variability, so its coefficient combines both roles.',size=11)
y=para(y,'For S*, persistence is again the strongest rank association (DECAY PRCC −0.81). Associations with the paired policy changes are much weaker: the largest absolute PRCC is 0.21 for the combined contrast and 0.13 for the isolated restriction. Interactions, nonmonotonic responses and cohort noise limit what these rankings can show.',size=11)
y=para(y,'Verification includes exact cumulative-premium scaling, mutually exclusive routes, a no-restriction equivalence check and a neutral-world experiment. With wealth-related channels disabled, 20 independent cohorts gave geometric-mean ratios T=1.000, S=1.004 and S*=1.002. Finite random samples need not equal 1 exactly.',size=11)
para(y,'The model does not match survey moments or validate an out-of-sample empirical target. Families do not solve a new spending optimization after a policy switch, and prices are fixed. Some downstream choices respond mechanically to changed scores and classes; this is not an equilibrium model of substitution.',size=11)
end()
head(11,'Sources','References')
refs=[(r['entry'],r['url']) for r in json.loads((D/'references.json').read_text())]
y=150
for i,(ref,url) in enumerate(refs):
    if i and i % 7 == 0:
        end();head(12,'Sources','References and research materials');y=150
    y=para(y,ref+' '+link(url,url if 'doi.org' in url else 'Source'),size=10.5)
end()
head(13,'School pathways','How students move through school')
y=para(150,'This diagram outlines possible routes in Guangzhou. Actual admission depends on the year, eligibility, preferences, school plans and admissions batches. Students can take different paths after secondary school.')
def box(x, y, w, h, title, subtitle=''):
    rect(x,y,w,h,soft)
    txt(x+13,y+22,title,11,'Bold',ink)
    if subtitle:
        para(y+30,subtitle,x=x+13,w=w-26,size=9,font='Sans',leading=12)
def arrow(x,y):
    line(x,y,x,y+12,teal,1.3)
    C.setFillColor(color(teal));C.circle(x,792-y-12,2,fill=1,stroke=0)
box(48,235,516,52,'Primary school → junior secondary school','Nine years of compulsory education')
arrow(306,287)
box(48,300,516,55,'Zhongkao, eligibility and school preferences','Scores, registration, school plans and admissions batches interact.')
line(306,355,306,361,teal);line(172,361,440,361,teal);line(172,361,172,368,teal);line(440,361,440,368,teal)
box(48,368,249,80,'General senior high school','Public or private; admission through several categories.')
box(315,368,249,80,'Vocational secondary education','Different schools and programmes, with routes to further study or work.')
arrow(172,448);arrow(440,448)
box(48,461,249,70,'Gaokao and other admissions routes','General-high-school pupils commonly take the university entrance exam.')
box(315,461,249,70,'Further study or work','Vocational pupils can also pursue further education.')
para(557,'Some eligible students can apply for quota places allocated to junior schools by participating public high schools. Minimum scores and eligibility rules apply. Unused quota places can return to later general admission batches (Guangzhou Admissions Office, 2026a).',size=11)
para(663,'This outline is a guide to the system, not a complete admissions rulebook. School options and admission categories vary by year.',size=10,font='Sans')
end()
head(14,'Simulation pathways','What the program actually follows')
para(150,'The code simplifies the real pathway. It generates pupils and ranks them using simulated scores. The boxes show model rules, not observed flows or actual Guangzhou admission rates.',size=11.5)
box(48,226,516,55,'Synthetic pupils and junior-school inputs','Family wealth, modeled starting ability, teacher effects and pre-gate tutoring.')
arrow(306,281)
box(48,294,516,67,'Simulated entrance score and public academic-seat ranking','A single modeled cap limits non-local pupils in public academic places.')
line(306,361,306,367,teal);line(128,367,484,367,teal);line(128,367,128,374,teal);line(306,367,306,374,teal);line(484,367,484,374,teal)
box(48,374,160,116,'Public academic','Elite or regular school; some elite seats follow junior-school quota rules.')
box(226,374,160,116,'Private academic','Only certain non-local pupils shut out of public seats, above the public cutoff and able to afford fees.')
box(404,374,160,116,'Outside academic','Others are not followed through later education or work in this model.')
arrow(128,490);arrow(306,490)
box(48,503,338,88,'Academic track → simulated university competition','Class banding; optional senior-2 reassignment; tutoring and route bonuses; top-decile place proxy.')
para(614,'The university outcome targets 10% of the entire synthetic cohort. Art and joint-exam routes are represented as bonuses in one ranking, rather than separate admission systems. The cutoff includes ties, so exact capacity is verified for these runs, not guaranteed for every possible input.',size=10.5)
end();C.save()
