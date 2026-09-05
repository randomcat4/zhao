"""Finite four-subset check on the saved 3322 length-16 leaf safe lists.

This is not an unrestricted suffix search. Each rejected four-subset is saved
with an explicit <=13-position zero-sum witness, independently rechecked.
"""
import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('--source',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--combination-limit',type=int,default=100000)
args=parser.parse_args()
start=time.monotonic()
rows=[json.loads(s) for s in Path(args.source).read_text(encoding='utf-8').splitlines()]
meta=rows[0]
assert meta['mode']=='3322' and meta['m']==13 and meta['target']==16
assert rows[-1]['all_roots_completed']
leaves=[r for r in rows if r['type']=='leaf_profile']
assert len(leaves)==15684
basis=(1,5,25,125)
core_basis=[1]*3+[5]*3+[25]*2+[125]*2
distribution=Counter()
eligible=[]
denominator=0
for record in leaves:
    support=set(basis)|set(record['blocks'])
    outside=[g for g in record['safe_single_additions'] if g not in support]
    distribution[len(outside)]+=1
    number=math.comb(len(outside),4) if len(outside)>=4 else 0
    denominator+=number
    if number: eligible.append((record,outside))
print(json.dumps({'leaf_denominator':len(leaves),'outside_safe_count_distribution':dict(sorted(distribution.items())),
                  'eligible_leaves':len(eligible),'four_subset_denominator':denominator}),flush=True)
if denominator>args.combination_limit:
    raise RuntimeError('Exact four-subset denominator exceeds the stated bounded scope')
Q=625
digits=np.array([[(g//5**i)%5 for i in range(4)] for g in range(Q)],dtype=np.int16)
weight=np.array([1,5,25,125],dtype=np.int16)
minus=((digits[None,:,:]-digits[:,None,:])%5)@weight
negative=((-digits)%5)@weight
def append(d,masks,g,index):
    proposal=d[minus[g]]+1
    improve=proposal<d
    updated=np.minimum(d,proposal)
    new_masks=masks.copy()
    new_masks[improve]=masks[minus[g]][improve]|np.uint32(1<<index)
    return updated,new_masks
checks=[]
survivors=[]
for record,outside in eligible:
    core=core_basis+[g for g in record['blocks'] for _ in range(2)]
    assert len(core)==16
    d=np.full(Q,99,dtype=np.int16)
    d[0]=0
    masks=np.zeros(Q,dtype=np.uint32)
    for i,g in enumerate(core):
        assert d[negative[g]]>=13
        d,masks=append(d,masks,g,i)
    assert [g for g in range(Q) if d[negative[g]]>=13]==record['safe_single_additions']
    for chosen in itertools.combinations(outside,4):
        ds,ms=d,masks
        full=core+list(chosen)
        witness=None
        for j,g in enumerate(chosen):
            if ds[negative[g]]<13:
                mask=int(ms[negative[g]])|(1<<(16+j))
                witness=[i for i in range(20) if mask>>i&1]
                assert 1<=len(witness)<=13
                assert np.all(np.sum(digits[[full[i] for i in witness]],axis=0)%5==0)
                break
            ds,ms=append(ds,ms,g,16+j)
        if witness is None:
            survivors.append({'blocks':record['blocks'],'chosen_outside':chosen,'expanded_encoded_sequence':full})
        checks.append({'blocks':record['blocks'],'chosen_outside':chosen,'zero_sum_positions_zero_based':witness})
assert len(checks)==denominator
result={'status':'EXHAUSTIVE_NO_SURVIVORS' if not survivors else 'EXHAUSTIVE_WITH_SURVIVORS',
    'group':'C_5^4','core_basis_encoded':core_basis,'core_length':16,'added_outside_distinct_positions':4,'cutoff':13,
    'leaf_denominator':len(leaves),'outside_safe_count_distribution':dict(sorted(distribution.items())),
    'eligible_leaf_count':len(eligible),'four_subset_denominator':denominator,'checked_four_subsets':len(checks),
    'survivor_count':len(survivors),'survivors':survivors,'all_checks_with_explicit_witness':checks,
    'source':args.source,'source_sha256':hashlib.sha256(Path(args.source).read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.monotonic()-start}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','checked_four_subsets','survivor_count','seconds')}))
