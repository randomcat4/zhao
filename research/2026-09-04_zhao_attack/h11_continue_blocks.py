"""Exact compressed block obstruction for B; no outside-point search."""
import collections
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'evidence/atom_h11_core_profiles.json').read_text(encoding='utf-8'))
poly=json.loads((ROOT/'h11_continue_polynomial.json').read_text(encoding='utf-8'))
pl={c['id']:c for c in poly['records']}
digits=[tuple(g//5**i%5 for i in range(3)) for g in range(125)]
def enc(t): return sum(t[i]*5**i for i in range(3))
def add(x,y): return enc(tuple((a+b)%5 for a,b in zip(digits[x],digits[y])))
def neg(x): return enc(tuple(-a%5 for a in digits[x]))
rows=[]
for c in data['cores']:
    p=pl[c['id']]; a=p['a']; sig=enc(p['sigma']); d=c['distance_table']
    lin=[sum(v*w for v,w in zip(a,t))%5 for t in digits]
    witnesses=[]
    for g in (1,5,25):
        if d[add(sig,neg(g))]>=10:
            target=add(add(sig,sig),neg(g))
            witnesses.append((g,target,d[target]))
    rows.append({'id':c['id'],'double_sigma_minus_triples':witnesses,
                 'E10_zero':[g for g in range(125) if d[g]>=10 and lin[g]==0],
                 'E10_one':[g for g in range(125) if d[g]>=10 and lin[g]==1]})
out={'status':'FINITE_BLOCK_PROBE','records':rows}
(ROOT/'h11_continue_blocks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('d2sigma_v',dict(collections.Counter(w[2] for r in rows for w in r['double_sigma_minus_triples'])))
print('faild>5',[(r['id'],w) for r in rows for w in r['double_sigma_minus_triples'] if w[2]>5])
print('E10_one',[(r['id'],r['E10_one']) for r in rows if r['E10_one']])
print('E10_zero_distribution',dict(collections.Counter(len(r['E10_zero']) for r in rows)))
