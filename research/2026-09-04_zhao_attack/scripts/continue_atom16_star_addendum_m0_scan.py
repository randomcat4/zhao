"""Complete bounded scan of d=4,M=0 forced 13-position cores.

Only the forced core and each of its 625 one-position extensions are tested.
There is no suffix DFS.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import time

BASE=Path(__file__).resolve().parents[1]
V=tuple(tuple(g//5**j%5 for j in range(4)) for g in range(625))
def enc(v):return sum(x*5**j for j,x in enumerate(v))
def addv(a,b):return enc(tuple((x+y)%5 for x,y in zip(V[a],V[b])))
PLUS=tuple(tuple(addv(a,b) for b in range(625)) for a in range(625))
NEG=tuple(enc(tuple(-x%5 for x in V[g])) for g in range(625))
def digest(name):return sha256((BASE/name).read_bytes()).hexdigest()


def build(seq):
    distance=[99]*625;distance[0]=0
    for g in seq:
        if distance[NEG[g]]<14:return None
        new=distance[:]
        for h in range(625):
            target=PLUS[h][g]
            if distance[h]+1<new[target]:new[target]=distance[h]+1
        distance=new
    return distance


def forced(x,ys):
    gs=[PLUS[x][y] for y in ys]
    support={x,*ys,*gs}
    if len(support)!=9 or 0 in support:return None
    return [x]+sum(([gs[i],ys[i],ys[i]] for i in range(4)),[]),sorted(support)


def main():
    started=time.perf_counter();e=(1,5,25,125)
    charts=(('basis_y1_y2_y3_y4',lambda z:(z,list(e))),
            ('basis_x_y1_y2_y3',lambda z:(e[0],[z,e[1],e[2],e[3]])))
    records=[];summaries=[]
    for name,chart in charts:
        checked=eligible=safe_cores=625
        eligible=0;safe_cores=0;candidate_hist=Counter();raw_hist=Counter()
        for z in range(625):
            x,ys=chart(z);item=forced(x,ys)
            if item is None:continue
            eligible+=1;seq,support=item;distance=build(seq)
            if distance is None:continue
            safe_cores+=1
            raw=[g for g in range(625) if distance[NEG[g]]>=14]
            outside=[g for g in raw if g not in support]
            raw_hist[len(raw)]+=1;candidate_hist[len(outside)]+=1
            records.append({'chart':name,'free_generator_encoded':z,
                'forced_sequence':seq,'forced_support':support,
                'minimum_distance_histogram':dict(sorted(Counter(distance).items())),
                'safe_next_values_all_625':raw,'safe_next_values_outside_support':outside})
        summaries.append({'chart':name,'all_free_vectors_checked':checked,
            'eligible_distinct_supports':eligible,'short_zero_free_forced_cores':safe_cores,
            'raw_safe_count_histogram':dict(sorted(raw_hist.items())),
            'outside_safe_count_histogram':dict(sorted(candidate_hist.items()))})
    assert [r['short_zero_free_forced_cores'] for r in summaries]==[36,69]
    assert len(records)==105
    assert all(set(r['safe_next_values_outside_support'])
               ==set(r['safe_next_values_all_625'])-set(r['forced_support']) for r in records)
    assert summaries[0]['outside_safe_count_histogram']=={35:24,40:12}
    assert summaries[1]['outside_safe_count_histogram']=={35:24,36:6,40:12,137:18,145:9}
    inputs=('proofs/continue_atom16_star.md','proofs/continue_atom16_star_addendum.md',
            'scripts/continue_atom16_star_addendum_m0_scan.py')
    output={'status':'COMPLETE_D4_M0_FORCED_CORE_AND_ONE_STEP_SCAN',
        'scope':'Two complete rank-four basis charts; exactly 2*625 core parameters and all 625 next values; no suffix DFS',
        'summaries':summaries,'safe_core_records':records,'safe_core_record_count':len(records),
        'input_sha256':{name:digest(name) for name in inputs},'seconds':time.perf_counter()-started}
    (BASE/'evidence/continue_atom16_star_addendum_m0_scan.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    for name,expected in output['input_sha256'].items():assert digest(name)==expected
    print(json.dumps({'status':output['status'],'summaries':summaries,'records':len(records),'seconds':output['seconds']}))


if __name__=='__main__':main()
