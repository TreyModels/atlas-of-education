import sys; sys.argv=['x']
import full_matrix_trends as F
for x,y in (("electricity","lsc"),("electricity","sec"),("wage_emp","ter"),("ter","sec"),("gdppc_log","lsc"),("lsc","gdppc_log")):
    for t in (False,True):
        r=F.edge((x,y,t)); print(x,"->",y,"trend" if t else "FE", None if r is None else "b=%+.4f se=%.4f n=%d nc=%d"%(r[3],r[4],r[5],r[6]))
