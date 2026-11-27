# Rank sensitivity diagnostics

All 32 independently sampled inputs; 1,024 settings, one synthetic cohort per setting. PRCC controls the ranks of the other 31 inputs. Coefficients describe this assumed input distribution; they are neither causal effects nor variance shares. Nonmonotonicity, interactions and cohort noise can weaken or distort rankings. No inferential p-values are reported. TEACH_SD also controls HS_TEACH_SD.

## T

| Input | Spearman | PRCC |
|---|---:|---:|
| DECAY | -0.638 | -0.886 |
| HOME | +0.511 | +0.846 |
| TEACH_ZONE | +0.228 | +0.596 |
| SCHOOL_VA | +0.160 | +0.394 |
| PRE_EFF | +0.176 | +0.352 |
| ART_SHARE | +0.107 | +0.302 |
| POST_EFF | +0.096 | +0.291 |
| TEACH_SD | -0.073 | -0.290 |
| HK_SHARE | +0.050 | +0.243 |
| NONHUKOU | -0.066 | -0.229 |
| ART_BONUS | +0.095 | +0.214 |
| PRE_SHARE | +0.091 | +0.188 |
| ACAD | -0.033 | -0.125 |
| PEER | -0.058 | -0.115 |
| NOISE | -0.046 | -0.110 |
| BAN_GRAD | +0.061 | +0.098 |
| HOL_SHARE | -0.064 | -0.077 |
| QUOTA | +0.021 | +0.073 |
| TERM_SHARE | +0.006 | +0.071 |
| MINBAN_PEN | +0.071 | +0.059 |
| HK_BONUS | +0.035 | +0.056 |
| FT_SHARE | -0.042 | -0.051 |
| REBAND_PERF | -0.014 | -0.045 |
| ZHIBIAO | +0.033 | -0.024 |
| INSURE | -0.062 | +0.021 |
| TOP_TEACH | -0.054 | -0.015 |
| FT_EFF | +0.031 | +0.012 |
| BAN_RED | -0.004 | -0.012 |
| TAL_WEALTH | -0.010 | -0.010 |
| ZB_FLOOR | -0.025 | +0.007 |
| RHO_DEMAND | +0.042 | -0.005 |
| NH_WEALTH | -0.026 | +0.000 |

## Sstar

| Input | Spearman | PRCC |
|---|---:|---:|
| DECAY | -0.661 | -0.807 |
| HOME | +0.220 | +0.491 |
| ART_SHARE | +0.239 | +0.424 |
| TEACH_SD | -0.185 | -0.423 |
| NOISE | +0.217 | +0.395 |
| HK_SHARE | +0.160 | +0.340 |
| SCHOOL_VA | -0.153 | -0.284 |
| ART_BONUS | +0.171 | +0.270 |
| POST_EFF | +0.116 | +0.256 |
| TEACH_ZONE | +0.052 | +0.189 |
| NONHUKOU | -0.069 | -0.166 |
| HK_BONUS | +0.062 | +0.131 |
| PRE_EFF | +0.099 | +0.128 |
| ACAD | -0.046 | -0.115 |
| HOL_SHARE | -0.067 | -0.108 |
| MINBAN_PEN | +0.097 | +0.092 |
| PRE_SHARE | +0.043 | +0.076 |
| TOP_TEACH | -0.036 | +0.066 |
| TERM_SHARE | +0.022 | +0.064 |
| FT_SHARE | -0.056 | -0.051 |
| NH_WEALTH | -0.058 | -0.050 |
| RHO_DEMAND | +0.002 | -0.045 |
| TAL_WEALTH | -0.020 | -0.044 |
| QUOTA | +0.010 | +0.043 |
| ZHIBIAO | +0.037 | +0.039 |
| BAN_GRAD | +0.041 | +0.037 |
| PEER | -0.035 | -0.035 |
| INSURE | -0.052 | +0.033 |
| REBAND_PERF | -0.007 | +0.032 |
| FT_EFF | +0.042 | +0.031 |
| ZB_FLOOR | -0.001 | +0.006 |
| BAN_RED | -0.021 | +0.006 |

## delta_T

| Input | Spearman | PRCC |
|---|---:|---:|
| TEACH_SD | +0.201 | +0.210 |
| DECAY | -0.205 | -0.188 |
| PEER | -0.107 | -0.114 |
| TOP_TEACH | -0.114 | -0.097 |
| HOME | -0.090 | -0.094 |
| BAN_GRAD | +0.082 | +0.090 |
| TEACH_ZONE | -0.081 | -0.080 |
| TAL_WEALTH | -0.053 | -0.060 |
| REBAND_PERF | -0.063 | -0.058 |
| ZHIBIAO | +0.019 | +0.050 |
| MINBAN_PEN | +0.045 | +0.044 |
| PRE_SHARE | -0.039 | -0.043 |
| HK_BONUS | -0.024 | -0.042 |
| QUOTA | +0.026 | +0.042 |
| NOISE | +0.044 | +0.041 |
| BAN_RED | -0.057 | -0.039 |
| ZB_FLOOR | +0.039 | +0.034 |
| POST_EFF | +0.045 | +0.033 |
| NONHUKOU | +0.014 | +0.032 |
| ART_BONUS | +0.020 | +0.025 |
| ART_SHARE | +0.032 | +0.025 |
| HOL_SHARE | +0.017 | +0.024 |
| FT_EFF | +0.041 | +0.023 |
| SCHOOL_VA | -0.007 | +0.022 |
| NH_WEALTH | -0.037 | -0.022 |
| FT_SHARE | -0.029 | -0.021 |
| TERM_SHARE | +0.020 | +0.019 |
| PRE_EFF | -0.016 | -0.017 |
| HK_SHARE | +0.035 | +0.015 |
| INSURE | -0.009 | +0.009 |
| ACAD | -0.014 | +0.006 |
| RHO_DEMAND | -0.033 | -0.006 |

## delta_T_ban

| Input | Spearman | PRCC |
|---|---:|---:|
| BAN_GRAD | +0.128 | +0.128 |
| DECAY | +0.095 | +0.104 |
| BAN_RED | -0.103 | -0.101 |
| PRE_EFF | -0.104 | -0.096 |
| HK_BONUS | -0.053 | -0.046 |
| INSURE | -0.037 | -0.045 |
| ZB_FLOOR | +0.048 | +0.042 |
| TEACH_SD | -0.050 | -0.040 |
| TOP_TEACH | -0.040 | -0.039 |
| NH_WEALTH | -0.031 | -0.037 |
| FT_SHARE | -0.015 | -0.035 |
| HOME | -0.020 | -0.029 |
| NOISE | -0.026 | -0.027 |
| MINBAN_PEN | +0.022 | +0.027 |
| PRE_SHARE | -0.030 | -0.025 |
| ART_SHARE | -0.017 | -0.022 |
| ART_BONUS | +0.029 | +0.015 |
| ACAD | +0.019 | +0.015 |
| POST_EFF | +0.006 | +0.014 |
| REBAND_PERF | -0.009 | -0.014 |
| TEACH_ZONE | -0.019 | -0.012 |
| HOL_SHARE | -0.003 | +0.011 |
| RHO_DEMAND | +0.004 | +0.011 |
| HK_SHARE | -0.001 | -0.008 |
| QUOTA | +0.023 | +0.008 |
| TAL_WEALTH | +0.002 | +0.007 |
| SCHOOL_VA | -0.011 | -0.007 |
| ZHIBIAO | +0.002 | +0.007 |
| PEER | -0.003 | +0.005 |
| TERM_SHARE | -0.009 | -0.002 |
| NONHUKOU | -0.005 | +0.002 |
| FT_EFF | +0.009 | -0.001 |
