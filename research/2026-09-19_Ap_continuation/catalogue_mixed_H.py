"""Finite graph shapes with vertex cover <=2, maximum degree4, and no C4.

Graphs are encoded canonically through all ordered choices of a two-vertex
cover, so no external graph library is required. This is not A_p exclusion.
"""
from itertools import combinations, product
from pathlib import Path
import json


def covers(n,edges,k):
    return [frozenset(c) for c in combinations(range(n),k) if all(i in c or j in c for i,j in edges)]


def canonical(n,edges):
    options=[]
    adj=[set() for _ in range(n)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    for i,j in combinations(range(n),2):
        if not all(u in [i,j] or v in [i,j] for u,v in edges):continue
        common=len((adj[i]-{j}) & (adj[j]-{i}))
        a=len(adj[i]-{j})-common;b=len(adj[j]-{i})-common
        options.append((int(j in adj[i]),common,min(a,b),max(a,b)))
    return min(options)


def main():
    results={}
    for link,common,a,b in product(range(2),range(2),range(5),range(5)):
        if link+common+max(a,b)>4:continue
        edges=[];n=2
        if link:edges.append((0,1))
        if common:edges.extend([(0,n),(1,n)]);n+=1
        for _ in range(a):edges.append((0,n));n+=1
        for _ in range(b):edges.append((1,n));n+=1
        active=sorted(set(v for e in edges for v in e))
        if len(active)<2:continue
        ren={v:i for i,v in enumerate(active)}
        edges=[tuple(sorted((ren[i],ren[j]))) for i,j in edges];n=len(active)
        key=canonical(n,edges)
        if key in results:continue
        one=covers(n,edges,1);two=covers(n,edges,2)
        three=covers(n,edges,3) if n>=3 else []
        minthree=[c for c in three if not any(d<c for d in two) and not any(d<c for d in one)]
        results[key]={"n":n,"edges":edges,"vertex_cover_number":1 if one else 2,
                      "two_covers":[sorted(c) for c in two],
                      "minimal_three_covers":[sorted(c) for c in minthree]}
    report=[{"canonical":key,**val} for key,val in sorted(results.items())]
    survivors=[]
    for q in report:
        adjacency=[set() for _ in range(q['n'])]
        for i,j in q['edges']:adjacency[i].add(j);adjacency[j].add(i)
        if q['vertex_cover_number']==2 and len(q['two_covers'])==1:
            assert len(q['minimal_three_covers'])<=3
            q['exclusion']='unique_two_cover'
        elif max(map(len,adjacency))==4:
            q['exclusion']='degree_four'
        elif any(len(adjacency[i])==3 and any(u not in adjacency[i]|{i} and v not in adjacency[i]|{i} for u,v in q['edges']) for i in range(q['n'])):
            q['exclusion']='degree_three_with_distant_edge'
        else:
            q['exclusion']=None
            survivors.append(q)
    assert len(report)==32 and len(survivors)==9 and max(q['n'] for q in survivors)==5
    final_survivors=[]
    for q in report:
        es={frozenset(e) for e in q['edges']}
        triangle=any(all(frozenset(e) in es for e in combinations(c,2))
                     for c in combinations(range(q['n']),3))
        matching_two=any(not e & f for e,f in combinations(es,2))
        q['star_reduction_exclusion']=(q['exclusion'] or
            ('triangle' if triangle else 'two_disjoint_edges' if matching_two else None))
        if q['star_reduction_exclusion'] is None:
            final_survivors.append(q)
    assert sorted((q['n'],len(q['edges'])) for q in final_survivors)==[(2,1),(3,2),(4,3)]
    Path(__file__).with_name("mixed_H_graph_catalogue.json").write_text(json.dumps(report,indent=2)+"\n")
    print('graph shapes',len(report))
    print('remaining shapes',len(survivors),'maximum active vertices',max(q['n'] for q in survivors))
    print('after hand-proved triangle and matching exclusions:',len(final_survivors),'stars')
    for q in report:
        if q['vertex_cover_number']==2:
            print(q['canonical'],'n',q['n'],'two',len(q['two_covers']),'minimal3',len(q['minimal_three_covers']))


if __name__=='__main__':main()
