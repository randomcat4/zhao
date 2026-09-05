"""Reconcile the complete raw logs and denominators, without trusting status labels.
This is a log/coverage audit. run_all.py also reruns the mathematical checkers and
both exhaustive searches; this file alone is not a replacement for those runs.
"""
import sys
if sys.flags.optimize: raise RuntimeError('Run without -O.')
from pathlib import Path
from math import comb
from collections import Counter
import argparse,json,re

ROOT=Path(__file__).resolve().parent

def require(condition,message):
    if not condition: raise ValueError(message)

def integer(tokens,key):return int(tokens[tokens.index(key)+1])

def read_roots(path):
    rows=[]
    for line in path.read_text().splitlines():
        a=tuple(map(int,line.split()));require(a[0]==len(a)-1,'root size');rows.append(a[1:])
    require(len(rows)==len(set(rows))==1786,'root denominator')
    require(Counter(map(len,rows))=={7:1084,8:659,9:43},'root size census')
    return rows

def read_run(directory,name):
    require((directory/f'{name}.exit').read_text().strip()=='0',f'{name}: nonzero or missing exit')
    require((directory/f'{name}.err').read_bytes()==b'',f'{name}: nonempty stderr')
    return (directory/f'{name}.log').read_text()

def search_rows(text,expected_order,kind):
    lines=text.splitlines();rows={};found=[]
    for line in lines:
        if line.startswith('root '):
            t=line.split();i=int(t[1]);require(i not in rows,'duplicate root ID')
            marker='root_labels' if kind=='reference' else 'labels'
            labels=tuple(map(int,t[t.index(marker)+1:]))
            require(0<=i<len(expected_order) and labels==expected_order[i],'root label/order mismatch')
            h=integer(t,'h');require(h==len(labels),'h mismatch')
            row={k:integer(t,k) for k in ('pool','nodes','maxdepth','color_prunes','size_prunes')}
            row['h']=h;row['labels']=labels
            require(0<=row['pool']<=499 and row['nodes']>0,'pool/node bounds')
            require(h+1<=row['maxdepth']<=21,'prefix bounds')
            if kind!='reference':
                row.update({k:integer(t,k) for k in ('expected','closed','fallbacks')})
                denominator=comb(499,20-h)
                require(row['expected']==row['closed']==denominator,'per-root raw coverage mismatch')
            rows[i]=row
        elif line.startswith('NORMAL_EXIT '):found.append(line)
        else:raise ValueError('unexpected line in full search log: '+line[:100])
    require(set(rows)==set(range(1786)) and len(found)==1,'missing roots or final summary')
    t=found[0].split();require(integer(t,'total_nodes')==sum(r['nodes'] for r in rows.values()),'node sum mismatch')
    if kind=='reference':require(integer(t,'denominator')==integer(t,'closed')==1786,'reference final count')
    else:
        total=sum(comb(499,20-len(r)) for r in expected_order)
        require(t[t.index('roots')+1]=='1786/1786','verifier final root count')
        require(integer(t,'expected')==integer(t,'closed')==total,'verifier final raw count')
        require(integer(t,'maximum_depth')==max(r['maxdepth'] for r in rows.values()),'max-depth summary')
        require(integer(t,'exact_size_fallbacks')==sum(r['fallbacks'] for r in rows.values()),'fallback summary')
        require(integer(t,'translation_tests')==390625,'translation denominator')
    return rows

def validate(source,logs):
    roots=read_roots(source/'rank3_roots.txt')
    reference=search_rows(read_run(logs,'search_reference'),sorted(roots,key=len,reverse=True),'reference')
    independent=search_rows(read_run(logs,'verify_extensions'),roots,'independent')
    a={r['labels']:r['pool'] for r in reference.values()}
    b={r['labels']:r['pool'] for r in independent.values()}
    require(a==b,'independently computed initial candidate pools differ')
    r=json.loads(read_run(logs,'verify_roots'))
    require(r['rank3_nodes']==450754 and r['maximum']==9,'rank-three bound')
    require(r['normalized_denominator']==r['normalized_processed']==406416 and r['uncovered']==0,'rank-three orbit coverage')
    f=json.loads(read_run(logs,'verify_farkas'))
    require(f['unquotiented_denominator']==f['processed']==9590 and f['minimum_score']==0 and f['rhs']==-2844400,'profile certificate')
    x=json.loads(read_run(logs,'audit_interfaces'))
    require(x['residue_tuple_denominator']==x['residue_tuples_processed']==3125,'deletion templates')
    require(x['position_deletion_sets']==7547 and x['position_deletion_equations']==9364,'position deletion index count')
    g=read_run(logs,'generate_roots')
    gc={int(t[1]):int(t[2]) for line in g.splitlines() if (t:=line.split())[0]=='size_count'}
    require(gc=={3:1,4:90,5:3000,6:41247,7:195462,8:193464,9:17490,10:0,11:0,12:0},'generator full census')
    regenerated=logs/'rank3_roots.regenerated.txt'
    require(regenerated.read_bytes()==(source/'rank3_roots.txt').read_bytes(),'root regeneration differs bytewise')
    for name,fields in (
        ('unit_search_reference',{'direct_subset_states':4194303,'minimum_length_cells':13750}),
        ('unit_verify_extensions',{'independent_pairs':193440,'third_point_tests':120900000,'direct_subset_states':4194303,'reachability_cells':27500,'exact_size_boundaries':9,'binomial_cells':7000,'translation_tests':390625})):
        t=read_run(logs,name).split();require(t[0]=='NORMAL_EXIT','unit abnormal')
        require(all(integer(t,k)==v for k,v in fields.items()),'unit denominator mismatch')
    legacy=json.loads(read_run(logs,'audit_legacy_models'))
    require(legacy['formal_15_blocks']['complete_C7_size']==238 and legacy['fourteen_atom']['outside_pair_denominator']==91,'red-team controls')
    total=sum(comb(499,20-len(r)) for r in roots)
    result={'root_denominator':1786,'reference_roots_closed':len(reference),'independent_roots_closed':len(independent),
            'raw_extension_denominator':total,'raw_extensions_closed':sum(r['closed'] for r in independent.values()),
            'reference_nodes':sum(r['nodes'] for r in reference.values()),'independent_nodes':sum(r['nodes'] for r in independent.values()),
            'independent_maximum_depth':max(r['maxdepth'] for r in independent.values()),
            'normalized_rank3_objects':406416,'profile_denominator':9590,'profile_rhs':-2844400,
            'm_values_total':len(range(20,comb(21,7)+1,5)),
            'pool_ranges_by_h':{h:[min(r['pool'] for r in independent.values() if r['h']==h),max(r['pool'] for r in independent.values() if r['h']==h)] for h in (7,8,9)},
            'all_denominators_equal':True,'exit':'NORMAL',
            'scope':'Complete computational interfaces and exact log reconciliation; hand-proof reductions must also be audited.'}
    require(total==17972093794219884182340301482 and result['raw_extensions_closed']==total,'final denominator')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT);p.add_argument('--logs',type=Path,default=ROOT);args=p.parse_args()
    print(json.dumps(validate(args.source.resolve(),args.logs.resolve()),indent=2))
