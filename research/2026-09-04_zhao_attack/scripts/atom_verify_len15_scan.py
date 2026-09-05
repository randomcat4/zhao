"""Recheck the length-15 node denominator and profiles without extending nodes."""
import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path
import numpy as np

base=Path(__file__).resolve().parent.parent
source=base/'evidence/atom_3222_len15_scan.jsonl'
tree_path=base/'evidence/atom_3222_m13_blocks.jsonl'
tree_rows=[json.loads(s) for s in tree_path.read_text(encoding='utf-8').splitlines()]
tree_meta=tree_rows[0]
tree={r['root']:r for r in tree_rows if r['type']=='root'}
start=time.monotonic()
digits=np.array([[(g//5**i)%5 for i in range(4)] for g in range(625)],dtype=np.int16)
weights=np.array([1,5,25,125],dtype=np.int16)
minus=((digits[None,:,:]-digits[:,None,:])%5)@weights
negative=((-digits)%5)@weights
fixed=(1,1,1,5,5,25,25,125,125)
initial=np.full(625,99,dtype=np.int16)
initial[0]=0
for g in fixed: initial=np.minimum(initial,initial[minus[g]]+1)
root_count=Counter()
histogram=Counter()
denominator=0
seen=set()
extreme=[]
root_records={}
summary=None
with source.open(encoding='utf-8') as stream:
    for line in stream:
        r=json.loads(line)
        if r['type']=='metadata':
            assert r['canonical_roots']==tree_meta['canonical_roots']
            assert r['initial_safe_candidates']==tree_meta['initial_safe_candidates']
        elif r['type']=='root': root_records[r['root']]=r
        elif r['type']=='summary': summary=r
        else:
            assert r['type']=='leaf_profile' and r['length']==15
            blocks=tuple(r['blocks'])
            assert len(blocks)==3 and blocks not in seen
            seen.add(blocks)
            root_count[r['root']]+=1
            d=initial
            for g in blocks:
                for _ in range(2):
                    assert d[negative[g]]>=13
                    d=np.minimum(d,d[minus[g]]+1)
            assert {str(int(k)):int(v) for k,v in zip(*np.unique(d,return_counts=True))}==r['distance_counts']
            safe=np.flatnonzero(d[negative]>=13).tolist()
            assert safe==r['safe_single_additions']
            support={1,5,25,125}|set(blocks)
            outside=[g for g in safe if g not in support]
            assert outside==r['outside_safe_additions']
            count=len(outside)
            combinations=math.comb(count,5) if count>=5 else 0
            assert combinations==r['five_subset_count']
            histogram[count]+=1
            denominator+=combinations
            if count>20: extreme.append({'blocks':blocks,'outside_safe_count':count,'coverage':r['coverage'],'distance_counts':r['distance_counts']})
assert summary is not None and summary['all_roots_completed']
assert set(root_records)==set(tree)
for root,r in tree.items():
    expected={k:v for k,v in r['nodes_by_length'].items() if int(k)<=15}
    assert root_records[root]['nodes_by_length']==expected
    assert root_records[root]['nodes']==sum(expected.values())
    assert root_count[root]==r['nodes_by_length'].get('15',0)
assert sum(root_count.values())==summary['leaf_profile_count']==107656
assert denominator==summary['five_subset_denominator']==2336039691
assert dict(sorted(histogram.items()))=={int(k):v for k,v in summary['outside_safe_count_distribution'].items()}
result={'status':'ALL_107656_NODE_PROFILES_REBUILT_AND_MATCHED','original_tree_root_count':len(tree),
    'length15_node_count':sum(root_count.values()),'maximum_outside_safe_count':max(histogram),
    'outside_safe_count_distribution':dict(sorted(histogram.items())),
    'five_subset_denominator':denominator,'five_subsets_enumerated':0,
    'extreme_nodes_with_more_than20_candidates':extreme,
    'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(base/'evidence/atom_3222_len15_scan_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','length15_node_count','maximum_outside_safe_count','five_subset_denominator','five_subsets_enumerated','seconds')}))
