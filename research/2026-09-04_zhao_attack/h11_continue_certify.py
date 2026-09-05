"""Small exact certificate for the two finite inputs of the B-H11 proof.

This does not search outside extensions.  Core admissibility and distances are
computed directly from the four choices of the two extra positions.
"""
import collections
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=[tuple(g//5**i%5 for i in range(3)) for g in range(125)]
def enc(v): return sum(v[i]*5**i for i in range(3))
def plus(x,y): return tuple((a+b)%5 for a,b in zip(x,y))
def mul(k,x): return tuple(k*a%5 for a in x)
def dot(x,y): return sum(a*b for a,b in zip(x,y))%5
directions=[v for v in D if any(v) and next(x for x in v if x)==1]
perms=list(itertools.permutations(range(3)))
def canonical(x,y):
    return min(tuple(sorted((enc(tuple(x[i] for i in p)),enc(tuple(y[i] for i in p))))) for p in perms)
def distance_table(x,y):
    result=[]
    for t in D:
        options=[]
        for e,f in itertools.product(range(2),repeat=2):
            z=tuple((t[i]-e*x[i]-f*y[i])%5 for i in range(3))
            if max(z)<=3: options.append(e+f+sum(z))
        result.append(min(options,default=99))
    return result
def line_geometry(ms):
    m=set(ms)
    for p in sorted(m):
        for v in directions:
            line={enc(plus(D[p],mul(j,v))) for j in range(5)}
            if not line<=m: continue
            off=sorted(m-line)
            if not off: return {'kind':'line','line':sorted(line),'direction':v,'off':[]}
            if len(off)==2:
                midpoint=enc(mul(3,plus(D[off[0]],D[off[1]])))
                if midpoint in line:
                    return {'kind':'line_plus_symmetric_pair','line':sorted(line),'direction':v,
                            'off':off,'midpoint':midpoint}
    return None

start=time.monotonic()
eligible=[g for g in range(125) if g not in (1,5,25) and 1 in D[g]]
raw=[]; by_orbit={}
for gx,gy in itertools.combinations_with_replacement(eligible,2):
    x,y=D[gx],D[gy]
    # A nonempty zero would use x, y, or both; the baseline box is {0,1,2,3}^3.
    if 1 not in plus(x,y): continue
    d=distance_table(x,y)
    a=tuple((x[(i+1)%3]*y[(i+2)%3]+x[(i+2)%3]*y[(i+1)%3])%5 for i in range(3))
    sigma=tuple((3+x[i]+y[i])%5 for i in range(3))
    sg=enc(sigma)
    assert dot(a,sigma)==3 and any(a)
    m=[g for g in range(125) if d[g]==99]
    e11=[g for g in range(125) if d[g]>=11]
    f0=[g for g in range(125) if d[g]>=10 and dot(a,D[g])==0]
    fiber3=[g for g in range(125) if d[g]>=10 and dot(a,D[g])==3]
    assert all(dot(a,D[g])==4 for g in m)
    assert set(e11)==set(m)|{sg}
    assert len(f0)<=2 and fiber3==[sg]
    case='F0_empty' if not f0 else 'M_at_most_4' if len(m)<=4 else 'line_geometry'
    geometry=line_geometry(m) if case=='line_geometry' else None
    assert case!='line_geometry' or geometry is not None
    key=canonical(x,y)
    row={'added':[gx,gy],'case':case,'orbit':key}
    raw.append(row)
    if (gx,gy)==key:
        by_orbit[key]={'id':','.join(map(str,key)),'added':[gx,gy],'a':a,'sigma':sg,
                       'M':m,'E10_fiber0':f0,'case':case,'geometry':geometry}
assert len(raw)==738 and len(by_orbit)==131
assert {tuple(r['orbit']) for r in raw}==set(by_orbit)
orbits=collections.Counter(tuple(r['orbit']) for r in raw)
for key,n in orbits.items():
    x,y=[D[g] for g in key]
    actual={tuple(sorted((enc(tuple(x[i] for i in p)),enc(tuple(y[i] for i in p))))) for p in perms}
    assert len(actual)==n
    by_orbit[key]['orbit_size']=n

# Independent, Cartesian checker of the previously supplied scalar certificate.
scalar_path=ROOT/'h11_continue_scalar_egz_v2.json'
scalar=json.loads(scalar_path.read_text(encoding='utf-8'))
rows=scalar['certificates']
all_counts={n for n in itertools.product(range(10),repeat=5) if sum(n)==9}
lookup={tuple(r['n']):r for r in rows}
assert len(rows)==len(lookup)==len(all_counts)==715 and set(lookup)==all_counts
for n,r in lookup.items():
    k=r['k']
    assert len(k)==5 and sum(k)==5 and all(0<=k[i]<=n[i] for i in range(5))
    residue=sum(i*k[i] for i in range(5))%5
    assert residue==r['residue']
    p=[i for i in range(5) if 0<k[i]<n[i]]
    assert ((residue==0 and (len(p)>=2 or any(n[i]>=3 for i in p)))
            or (residue==2 and p))

report={'status':'ALL_FINITE_INPUTS_VERIFIED','scope':'B with an H11 three-triple core only; not A or all B',
        'raw_core_count':len(raw),'orbit_core_count':len(by_orbit),'scalar_count_vectors':len(rows),
        'raw_cases':dict(collections.Counter(r['case'] for r in raw)),
        'orbit_cases':dict(collections.Counter(r['case'] for r in by_orbit.values())),
        'elapsed_seconds':time.monotonic()-start,
        'scalar_certificate_sha256':hashlib.sha256(scalar_path.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'orbits':[by_orbit[k] for k in sorted(by_orbit)],'raw_coverage':raw}
out=ROOT/'h11_continue_certificate.json'
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('orbits','raw_coverage')}))
print('geometry',[r for r in report['orbits'] if r['case']=='line_geometry'])
