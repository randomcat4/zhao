"""Verify finite-combination coverage and explicit witnesses without any DP."""
import hashlib
import itertools
import json
from pathlib import Path

base=Path(__file__).resolve().parent.parent
source=base/'evidence/atom_3322_outside_micro.json'
data=json.loads(source.read_text(encoding='utf-8'))
leaf_source=base/'evidence/atom_3322_leaf_profiles.jsonl'
leaves=[json.loads(s) for s in leaf_source.read_text(encoding='utf-8').splitlines()]
leaves=[r for r in leaves if r['type']=='leaf_profile']
fixed=[1]*3+[5]*3+[25]*2+[125]*2
expected=set()
for leaf in leaves:
    blocks=tuple(leaf['blocks'])
    support={1,5,25,125}|set(blocks)
    outside=[g for g in leaf['safe_single_additions'] if g not in support]
    for chosen in itertools.combinations(outside,4): expected.add((blocks,chosen))
actual=set()
lengths={}
for record in data['all_checks_with_explicit_witness']:
    key=(tuple(record['blocks']),tuple(record['chosen_outside']))
    assert key not in actual
    actual.add(key)
    sequence=fixed+[g for g in record['blocks'] for _ in range(2)]+record['chosen_outside']
    assert len(sequence)==20
    indices=record['zero_sum_positions_zero_based']
    assert indices is not None and 1<=len(indices)<=13
    assert len(set(indices))==len(indices)
    assert all(0<=i<20 for i in indices)
    for j in range(4): assert sum(sequence[i]//5**j%5 for i in indices)%5==0
    lengths[len(indices)]=lengths.get(len(indices),0)+1
assert actual==expected
assert len(actual)==data['four_subset_denominator']==data['checked_four_subsets']==8709
assert data['survivor_count']==0
result={'status':'ALL_8709_EXPLICIT_WITNESSES_VERIFIED','coverage_matches_all_saved_four_subsets':True,
    'checked_combinations':len(actual),'witness_length_distribution':dict(sorted(lengths.items())),
    'method':'plain integer coordinates; no distance DP and no search',
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'leaf_source_sha256':hashlib.sha256(leaf_source.read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(base/'evidence/atom_3322_outside_micro_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
