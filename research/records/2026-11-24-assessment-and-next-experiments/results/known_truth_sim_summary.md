Counts out of 100 replicates per regime (v2 rules).

| regime | truth | R | paper-rule ROBUST | ROBUST+H | ROBUST-HET | ROBUST-but-GROUP | GROUP | NONE | planted tag flagged |
|---|---|---|---|---|---|---|---|---|---|
| A | uniform b=0.15 (robust) | 25 | 100 | 93 | 7 | 0 | 0 | 0 |  |
| A | uniform b=0.15 (robust) | 100 | 100 | 97 | 3 | 0 | 0 | 0 |  |
| A | uniform b=0.15 (robust) | 400 | 100 | 98 | 1 | 1 | 0 | 0 |  |
| W | weak uniform b=0.06 (robust, low power) | 25 | 13 | 10 | 3 | 0 | 0 | 87 |  |
| W | weak uniform b=0.06 (robust, low power) | 100 | 13 | 11 | 2 | 0 | 0 | 87 |  |
| W | weak uniform b=0.06 (robust, low power) | 400 | 13 | 11 | 2 | 0 | 1 | 86 |  |
| B | b=0.40 only in top tercile of family 0 (group-specific) | 25 | 85 | 22 | 63 | 0 | 0 | 15 | 0 |
| B | b=0.40 only in top tercile of family 0 (group-specific) | 100 | 85 | 47 | 35 | 3 | 3 | 12 | 6 |
| B | b=0.40 only in top tercile of family 0 (group-specific) | 400 | 85 | 51 | 0 | 34 | 15 | 0 | 49 |
| C | null, independent series | 25 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| C | null, independent series | 100 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| C | null, independent series | 400 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| D | null, shared country trends (spurious levels link) | 25 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| D | null, shared country trends (spurious levels link) | 100 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| D | null, shared country trends (spurious levels link) | 400 | 0 | 0 | 0 | 0 | 2 | 98 |  |
| S | sign split: +0.25 / -0.25 by family-1 median (group-specific) | 25 | 0 | 0 | 0 | 0 | 0 | 100 |  |
| S | sign split: +0.25 / -0.25 by family-1 median (group-specific) | 100 | 0 | 0 | 0 | 0 | 99 | 1 |  |
| S | sign split: +0.25 / -0.25 by family-1 median (group-specific) | 400 | 0 | 0 | 0 | 0 | 100 | 0 |  |

Run 1 (paper rule only, no heterogeneity condition, 200 replicates):
A {'ROBUST': 199, 'NONE': 1}
W {'NONE': 173, 'ROBUST': 25, 'GROUP': 2}
B {'ROBUST': 174, 'GROUP': 26, 'planted_tag_flagged': 26}
C {'NONE': 199, 'GROUP': 1}
D {'NONE': 197, 'GROUP': 3}
S {'GROUP': 200}
