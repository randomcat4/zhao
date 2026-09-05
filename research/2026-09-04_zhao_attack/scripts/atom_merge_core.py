"""Merge checkpoint records, retaining completed roots and all prior attempts."""
import argparse
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--base',required=True)
parser.add_argument('--jsonl',required=True)
parser.add_argument('--output',required=True)
args=parser.parse_args()
result=json.loads(Path(args.base).read_text(encoding='utf-8'))
lines=[json.loads(s) for s in Path(args.jsonl).read_text(encoding='utf-8').splitlines()]
metadata=next(x for x in lines if x['type']=='metadata')
assert metadata['canonical_roots']==result['canonical_roots']
assert metadata['m']==result['m']
assert metadata['target']==result['n']
records={r['root']:r for r in result['runs']}
history=result.setdefault('attempt_history',[])
for record in lines:
    if record['type']!='root':
        continue
    root=record['root']
    if root in records:
        old=records[root]
        if old['completed_exhaustively']:
            for key in ('nodes','nodes_by_length','leaves_by_length','max_reached_length'):
                assert old[key]==record[key],(root,key)
        history.append(old)
    records[root]=record
result['runs']=[records[g] for g in result['canonical_roots'] if g in records]
result['completed_roots']=sum(r['completed_exhaustively'] for r in result['runs'])
result['all_roots_completed']=result['completed_roots']==len(result['canonical_roots'])
result['complete_record_node_total']=sum(r['nodes'] for r in result['runs'] if r['completed_exhaustively'])
result['max_reached_length']=max(r['max_reached_length'] for r in result['runs'])
result.setdefault('merged_jsonl_sources',[]).append(args.jsonl)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('completed_roots','all_roots_completed','complete_record_node_total','max_reached_length')}))
