## Appendix A. ODD protocol

The description follows the ODD protocol (Grimm et al. 2020).

### A.1 Purpose and patterns

The model asks which of three mechanisms can account for the scale and sourcing of teacher-supplied tutoring in a small Cambodian school system, and whether the mechanisms that fit equally well imply different consequences for policy. The mechanisms are: regular instruction that is too short for the curriculum (thin schooling); teachers withholding regular content to raise demand for their paid lessons (diversion); and a benefit attached to buying from one's own teacher regardless of content (favour). The model is judged by its ability to reproduce seven patterns reported for six secondary schools in Siem Reap province (Section 2): overall participation, participation in Grades 9 and 12, the urban–rural difference, the shares of tutoring supplied by own teachers and by other teachers in the same school, the share of teachers who tutor, and the small commercial share.

### A.2 Entities, state variables and scales

*Schools.* Six schools: three lower secondary schools with Grade 9 and three high schools with Grades 9 and 12, giving nine school-grade units. Two schools (one of each type) are urban. Each unit has a feasible amount of regular instruction m0, a share of the curriculum that the timetable allows, drawn once per run around the calibrated mean (normal, sd 0.08, clipped to [0.2, 1]).

*Classes.* Each unit has two parallel classes of 70 pupils, giving 18 classes and 1,260 pupils, close to the 1,274 surveyed pupils. Each class has a partner class in the same unit.

*Teachers.* One teacher per class and subject, four subjects, 72 teachers (the original study surveyed about 70). State variables: whether the teacher sells tutoring to own pupils; whether the teacher sells to the partner class; the share of regular content withheld d (only when selling to own pupils); a side-job return drawn uniformly from [0, side_job_max]; a per-unit cost of withholding content (a norm, conscience or monitoring cost) drawn lognormally around the calibrated median with log-sd 0.5.

*Pupils.* Grade, class, school, urban location, and household resources r (standard normal, shifted upward in urban schools by a calibrated amount). For each subject a pupil has a probability of buying from the own teacher, the partner-class teacher, a commercial provider, or no one.

*Scale.* One school year is represented as a static equilibrium. Quantities are normalized: instruction as a share of the curriculum, fees with Grade 9 = 1 and Grade 12 = 1.5.

### A.3 Process overview and scheduling

Initialization sets every teacher to sell to own pupils and to the partner class with no withholding (or no own sales under a ban). Teachers then revise their choices one at a time in a random order. Each teacher chooses the option with the highest payoff given the current choices of all other teachers and the purchase probabilities of pupils. A sweep visits every teacher once. Sweeps repeat until no teacher changes (a pure-strategy equilibrium) or 30 sweeps have passed. Outcomes are computed from the final state.

### A.4 Design concepts

*Basic principles.* Pupils choose among providers by multinomial logit (Train 2009). The teacher's payoff adapts Jayachandran's (2014) model of teachers who can lower the value of regular class to raise demand for their tutoring, and adds a side-job option, a partner-class market and rival mechanisms.

*Emergence.* The share of teachers who tutor, the sourcing of tutoring, participation by grade and location, and the amount of withheld content emerge from the interaction of teachers' choices and pupils' demand. In particular, whether a pupil can buy from another teacher depends on that teacher's own choice.

*Adaptation and objectives.* Teachers maximize a payoff per pupil on their roll:
(fee − 0.2) × (own purchases + partner-class purchases) / 70 − fixed cost − norm cost × d − 0.25 × d², compared with the side-job return. Under conditional pay, a bonus is added to every option that excludes sales to own pupils. Withholding is chosen on a grid from 0 to 0.4 in steps of 0.05, not exceeding m0.

*Sensing.* Teachers know the demand of their own and partner-class pupils at each withholding level. Pupils know which teachers sell and how much content their own teacher withholds.

*Interaction.* Teachers in parallel classes compete for each other's pupils. A teacher's withholding raises demand for every provider in proportion to how much of the withheld content that provider can cover: fully for the own teacher, a share ρ (recovery) for others.

*Stochasticity.* Pupil resources, school-grade instruction, side-job returns, norm costs and the order of teacher updates are random. Purchase decisions are not sampled: each pupil's choice probabilities are used directly, so a run is deterministic given its seed.

*Observation.* Participation is the probability that a pupil buys tutoring in at least one subject, averaged over pupils. Provider shares are shares of all expected purchases (pupil-subjects). Teacher tutoring share counts teachers who sell to anyone. Delivered regular instruction is m0 − d. Coverage adds the content supplied by purchased tutoring (the withheld content recovered plus 0.25 of further content), capped at 1.

### A.5 Initialization

Parameter values come from the calibration (Appendix B). Every run uses its own random seed for the world and the update order. Policy experiments reuse the seed of the calibrated run so that baseline and policy differ only in the policy.

### A.6 Input data

None during runs. The seven patterns are used only for calibration.

### A.7 Submodels

*Pupil demand.* For pupil i, subject k and own teacher j, with γ_i = fee_sens × exp(−r_i) and grade fee p:

V_own = A + s_k + Δ·1[Grade 12] + ξ(1 − m0) + β d_j + φ − γ_i p (if j sells to own pupils)
V_other = A + s_k + Δ·1[Grade 12] + ξ(1 − m0) + ρ β d_j − τ_o − γ_i p (if the partner-class teacher sells to this class)
V_com = A + s_k + Δ·1[Grade 12] + ξ(1 − m0) + ρ β d_j − τ_c − γ_i p, with τ_c = com_cost_urban plus com_cost_rural_extra outside town
V_none = 0

Subject offsets s_k are 0, −0.4, −0.8 and −1.2. Purchase probabilities are exp(V)/(1 + Σ exp(V)) over available options. Subjects are independent given the teachers' choices.

*Teacher best response.* For teacher j, demand from the partner class is computed with j selling to it. Demand from own pupils is computed at each feasible withholding level. The payoffs of three options are compared: side job; partner-class sales only; sales to own and partner pupils at the best withholding level. Ties go to the first option listed.

*Mechanism variants.* Thin: β = φ = 0, so withholding never raises revenue and teachers choose d = 0. Diversion: β free, φ = 0. Favour: φ free, β = 0. Full: both free. Thin schooling (ξ) is free in every variant.

*Policies.* Ban: teachers may not sell to own pupils. Conditional pay: a bonus of 0.3 (about a third of a Grade 9 fee per pupil on the roll) for teachers who do not sell to own pupils. Extra time: m0 rises by 0.10. Commercial entry: commercial inconvenience falls by 1.5 utility units.
