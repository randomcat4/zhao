"""Rebuild every recorded double-block leaf and check all 625 distances.

This does not extend any leaf or start a new search tree. Completeness is checked
against the separately preserved, already completed original tree records.
"""
import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('--leaf-file',required=True)
parser.add_argument('--tree-file',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
start=time.monotonic()
leaf_rows=[json.loads(s) for s in Path(args.leaf_file).read_text(encoding='utf-8').splitlines()]
tree_rows=[json.loads(s) for s in Path(args.tree_file).read_text(encoding='utf-8').splitlines()]
lm,tm=leaf_rows[0],tree_rows[0]
assert lm['mode']==tm['mode'] and lm['m']==tm['m']==13
assert lm['initial_safe_candidates']==tm['initial_safe_candidates']
assert lm['canonical_roots']==tm['canonical_roots']
mode=lm['mode']
target=17 if mode=='3222' else 16
mult=(3,2,2,2) if mode=='3222' else (2,2,2,2)
basis=(1,5,25,125)
lr={r['root']:r for r in leaf_rows if r['type']=='root'}
tr={r['root']:r for r in tree_rows if r['type']=='root'}
assert set(lr)==set(tr)==set(lm['canonical_roots'])
leaves=[r for r in leaf_rows if r['type']=='leaf_profile']
by_root=Counter(r['root'] for r in leaves)
assert len({tuple(r['blocks']) for r in leaves})==len(leaves)
for root,r in tr.items():
    assert r['completed_exhaustively'] and lr[root]['completed_exhaustively']
    for k in ('nodes','nodes_by_length','max_reached_length'):
        assert r[k]==lr[root][k],(root,k)
    assert by_root[root]==r['nodes_by_length'].get(str(target),0)
    assert by_root[root]==(r['terminal_count'] if mode=='3222' else r['leaves_by_length'].get('16',0))
digits=np.array([[(g//5**i)%5 for i in range(4)] for g in range(625)],dtype=np.int16)
weight=np.array([1,5,25,125],dtype=np.int16)
subtract=((digits[None,:,:]-digits[:,None,:])%5)@weight
negative=((-digits)%5)@weight
base=np.full(625,99,dtype=np.int16)
base[0]=0
for g,n in zip(basis,mult):
    for _ in range(n): base=np.minimum(base,base[subtract[g]]+1)
safe_counts=Counter()
max_distances=Counter()
coverages=Counter()
safe_in_support=Counter()
for record in leaves:
    d=base
    for g in record['blocks']:
        for _ in range(2):
            assert d[negative[g]]>=13
            d=np.minimum(d,d[subtract[g]]+1)
    hist={str(int(k)):int(v) for k,v in zip(*np.unique(d,return_counts=True))}
    safe=np.flatnonzero(d[negative]>=13).tolist()
    safe14=np.flatnonzero(d[negative]>=14).tolist()
    assert hist==record['distance_counts']
    assert safe==record['safe_single_additions']
    assert safe14==record['safe_single_additions_cutoff14']
    assert int(np.sum(d<99))==record['coverage']
    assert int(np.max(d))==record['maximum_distance']
    safe_counts[len(safe)]+=1
    max_distances[int(np.max(d))]+=1
    coverages[int(np.sum(d<99))]+=1
    support=set(basis)|set(record['blocks'])
    safe_in_support[sum(g in support for g in safe)]+=1
result={'status':'ALL_LEAF_PROFILES_REBUILT_AND_MATCHED','mode':mode,'cutoff':13,
    'root_count':len(tr),'leaf_count':len(leaves),'leaf_denominator_matches_original_tree':True,
    'safe_single_addition_count_distribution':dict(sorted(safe_counts.items())),
    'maximum_distance_distribution':dict(sorted(max_distances.items())),
    'coverage_distribution':dict(sorted(coverages.items())),
    'safe_additions_already_in_support_count_distribution':dict(sorted(safe_in_support.items())),
    'seconds':time.monotonic()-start,
    'leaf_source':args.leaf_file,'leaf_source_sha256':hashlib.sha256(Path(args.leaf_file).read_bytes()).hexdigest(),
    'tree_source':args.tree_file,'tree_source_sha256':hashlib.sha256(Path(args.tree_file).read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
