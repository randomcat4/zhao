#!/usr/bin/env python3
"""Independent finite-interface verifier for the F_5^4 three-anchor proof.
The universal theorem is analytic; this program checks the finite arithmetic,
position-deletion, graph, capacity, split, and multiplicity denominators.
Python 3.10+, standard library only.
"""
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json, random

P=5

def add(a,b): return tuple((x+y)%P for x,y in zip(a,b))
def mul(c,a): return tuple(c*x%P for x in a)

def ring_check():
    rows=[]
    for d in (3,4):
        deg=[sum(e) for e in product(range(P), repeat=d)]
        assert len(deg)==P**d and max(deg)==4*d
        rows.append({'d':d,'monomials':len(deg),'max_degree':max(deg),'nilpotence':4*d+1})
    return {'rows':rows,'total_monomials':sum(r['monomials'] for r in rows)}

def signed_identity_check(seed=20260905):
    rng=random.Random(seed); subsets=0; specs=[(3,13,4),(4,17,2)]
    for d,n,trials in specs:
        for _ in range(trials):
            seq=[tuple(rng.randrange(P) for _ in range(d)) for _ in range(n)]
            alt=0
            for mask in range(1<<n):
                s=[0]*d; bits=0
                for i,q in enumerate(seq):
                    if mask>>i&1:
                        bits+=1
                        for j in range(d): s[j]=(s[j]+q[j])%P
                if not any(s): alt=(alt+(-1 if bits&1 else 1))%P
            assert alt==0; subsets += 1<<n
    return {'seed':seed,'specs':specs,'subsets_checked':subsets}

def deletion_check():
    actual=congruent=exception=0
    for x in product(range(P),repeat=2):
        if x==(0,0): continue
        for s in product(range(P),repeat=2):
            y=tuple((s[i]-x[i])%P for i in range(2))
            for mx in range(1,5):
                for my in range(5):
                    if y==(0,0) and my: continue
                    if y==x and my!=mx: continue
                    actual+=1
                    z4d=my-int(y==x)
                    z4d1=int(s==x)
                    literal=(1+z4d-z4d1)%P
                    formula=(1+my-int(mul(2,x)==s)-int(x==s))%P
                    assert literal==formula
                    if literal: continue
                    congruent+=1
                    if mul(2,x)==s: raise AssertionError('half-value survivor')
                    if x==s:
                        exception+=1; assert y==(0,0) and my==0; continue
                    assert my==4
                    assert y!=(0,0) and y!=x
                    reverse=(1+mx-int(s==y))%P
                    if reverse==0: assert mx==4
    assert actual==11232
    return {'actual_rows':actual,'congruent_rows':congruent,'exception_rows':exception}

def graph_check(n=7):
    E=list(combinations(range(n),2)); m=len(E); idx={e:i for i,e in enumerate(E)}
    dis=[0]*m
    for i,e in enumerate(E):
        for j,f in enumerate(E):
            if set(e).isdisjoint(f): dis[i]|=1<<j
    tri=[]
    for a,b,c in combinations(range(n),3): tri.append((1<<idx[(a,b)])|(1<<idx[(a,c)])|(1<<idx[(b,c)]))
    star=[sum(1<<i for i,e in enumerate(E) if v in e) for v in range(n)]
    admissible=0
    for mask in range(1,1<<m):
        bad=False; mm=mask
        while mm:
            lsb=mm&-mm; i=lsb.bit_length()-1
            if dis[i]&mask: bad=True; break
            mm-=lsb
        if bad or any(mask&t==t for t in tri): continue
        admissible+=1
        if not any(mask&~sv==0 for sv in star): raise AssertionError(('graph counterexample',mask))
    assert admissible==420
    return {'n':n,'all_graphs':1<<m,'admissible':admissible,'counterexamples':0}

def anchor_split_check():
    anchor=[]
    for c in range(5):
        for qlen in range(1,11):
            j=(-c)%5
            if c==1: assert j==4
            else: assert j<=3 and qlen+j<=13
            anchor.append((c,qlen,j))
    split=[]
    for n,lo in ((14,2),(15,3)):
        for k in range(lo,12):
            comp=n-k; u=min(k,comp); repl=n-u+1
            assert u<=7 and repl<=13
            split.append((n,k,comp,u,repl))
    assert len(anchor)==50 and len(split)==19
    return {'anchor_rows':50,'split_rows':19}

def partitions(n,cap=None):
    out=[]
    def rec(rem,top,pref):
        if rem==0: out.append(tuple(pref)); return
        for v in range(min(rem,top),0,-1): rec(rem-v,v,pref+[v])
    rec(n,cap or n,[]); return out

def partition_check():
    allp=partitions(18); small=[p for p in allp if p[0]<=4]
    assert len(allp)==385 and len(small)==84 and len({p for p in allp})==385
    triples=Counter(1+p.count(3) for p in small)
    assert [triples[i] for i in range(1,8)]==[30,20,16,9,6,2,1]
    return {'total':385,'part_at_least_5':301,'max_part_le_4':84,'triple_histogram':dict(sorted(triples.items()))}

def main():
    report={'status':'PASS','scope':'finite interfaces only; analytic proof is PROOF.md + AUDIT.md',
            'ring':ring_check(),'signed_identity':signed_identity_check(),
            'deletion':deletion_check(),'graph':graph_check(),
            'anchor_split':anchor_split_check(),'partitions':partition_check()}
    root=Path(__file__).resolve().parent
    out=root/'independent_report.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    digest=sha256(out.read_bytes()).hexdigest()
    print('INDEPENDENT_AUDIT: PASS')
    print('signed_identity_subsets='+str(report['signed_identity']['subsets_checked']))
    print('deletion_actual_rows='+str(report['deletion']['actual_rows']))
    print('graphs_n7='+str(report['graph']['all_graphs'])+'; counterexamples=0')
    print('partitions='+str(report['partitions']['total']))
    print('anchor_rows=50; split_rows=19')
    print('report_sha256='+digest)

if __name__=='__main__': main()
