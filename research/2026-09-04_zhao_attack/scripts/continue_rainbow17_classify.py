"""Classify proper three-colour 2-matching graphs with no rainbow 3-matching.

The linear certificates use only the three equal-pair-sum relations over F5.
"""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
RED=((0,1),(2,3))


def normalize_edges(edges):
    labels={};nxt=0;result=[]
    for color in edges:
        row=[]
        for edge in color:
            pair=[]
            for old in edge:
                if old not in labels:labels[old]=nxt;nxt+=1
                pair.append(labels[old])
            row.append(tuple(pair))
        result.append(tuple(row))
    return tuple(result)


def matchings(current_n,forbidden):
    result=set()
    def visit(slots,max_label):
        if len(slots)==4:
            edges=tuple(sorted((tuple(sorted(slots[:2])),tuple(sorted(slots[2:])))))
            if edges[0]==edges[1] or any(e in forbidden for e in edges):return
            result.add(edges);return
        used=set(slots)
        for v in range(max_label+2):
            if v in used:continue
            visit(slots+[v],max(max_label,v))
    visit([],current_n-1)
    return sorted(result)


def rainbow(edges):
    return any(not (r&g or r&b or g&b)
               for r in map(set,edges[0]) for g in map(set,edges[1]) for b in map(set,edges[2]))


def permutations_of_slots():
    result=[]
    for swap_edges in product((0,1),repeat=3):
      for flip in product((0,1),repeat=6):
        indices=[]
        for c in range(3):
            order=(1,0) if swap_edges[c] else (0,1)
            for e in order:
                slots=[4*c+2*e,4*c+2*e+1]
                if flip[2*c+e]:slots.reverse()
                indices.extend(slots)
        result.append(indices)
    return result
SLOT_PERMS=permutations_of_slots()


def canonical(edges):
    slots=[v for color in edges for edge in color for v in edge]
    best=None
    for perm in SLOT_PERMS:
        labels={};nxt=0;word=[]
        for index in perm:
            old=slots[index]
            if old not in labels:labels[old]=nxt;nxt+=1
            word.append(labels[old])
        word=tuple(word)
        if best is None or word<best:best=word
    return best


def vector(n,terms):
    row=[0]*n
    for i,c in terms:row[i]=(row[i]+c)%5
    return tuple(row)


def add(a,b):return tuple((x+y)%5 for x,y in zip(a,b))
def scale(c,a):return tuple(c*x%5 for x in a)


def certificate(edges):
    n=1+max(v for color in edges for edge in color for v in edge)
    relations=[];targets=[]
    for color in edges:
        a,b=color[0];c,d=color[1]
        relations.append(vector(n,((a,1),(b,1),(c,-1),(d,-1))))
        targets.append(vector(n,((a,1),(b,1))))
    span={}
    for coeff in product(range(5),repeat=3):
        value=(0,)*n
        for c,row in zip(coeff,relations):value=add(value,scale(c,row))
        span.setdefault(value,coeff)
    for i in range(n):
      for j in range(i+1,n):
        value=vector(n,((i,1),(j,-1)))
        if value in span:return {'kind':'forced_vertex_equality','vertices':[i,j],'relation_coefficients':span[value]}
    for i in range(3):
      for j in range(i+1,3):
        value=add(targets[i],scale(-1,targets[j]))
        if value in span:return {'kind':'forced_target_equality','colors':[i,j],'relation_coefficients':span[value]}
    for c,target in enumerate(targets):
        if target in span:return {'kind':'forced_zero_target','color':c,'relation_coefficients':span[target]}
        for i in range(n):
            value=add(target,vector(n,((i,-1),)))
            if value in span:return {'kind':'forced_target_vertex_equality','color':c,'vertex':i,
                                     'relation_coefficients':span[value]}
    # A subset of U forced to sum to zero.
    for size in range(1,n+1):
      for mask in range(1,1<<n):
        if mask.bit_count()!=size:continue
        value=tuple((mask>>i)&1 for i in range(n))
        if value in span:return {'kind':'U_zero_subset','vertices':[i for i in range(n) if mask>>i&1],
                                 'relation_coefficients':span[value]}
    # Replace D from a 17-atom by nonempty external target positions Q.
    for qmask in range(1,8):
        q=[c for c in range(3) if qmask>>c&1]
        tq=(0,)*n
        for c in q:tq=add(tq,targets[c])
        for dmask in range(1,1<<n):
            if dmask.bit_count()-len(q)<3:continue
            indicator=tuple((dmask>>i)&1 for i in range(n))
            value=add(indicator,scale(-1,tq))
            if value in span:
                return {'kind':'atom_replacement_zero','delete_vertices':[i for i in range(n) if dmask>>i&1],
                        'add_colors':q,'resulting_length':17-dmask.bit_count()+len(q),
                        'relation_coefficients':span[value]}
    # Direct positive zero sum among graph vertices and target positions.
    for qmask in range(8):
        q=[c for c in range(3) if qmask>>c&1];tq=(0,)*n
        for c in q:tq=add(tq,targets[c])
        for dmask in range(1<<n):
            if not q and not dmask or dmask.bit_count()+len(q)>14:continue
            indicator=tuple((dmask>>i)&1 for i in range(n))
            value=add(indicator,tq)
            if value in span:return {'kind':'direct_short_zero','vertices':[i for i in range(n) if dmask>>i&1],
                'colors':q,'length':dmask.bit_count()+len(q),'relation_coefficients':span[value]}
    return None


def main():
    canonical_types={};raw=0;green_count=0;blue_count=0
    for green in matchings(4,set(RED)):
        green_count+=1;n=1+max(v for e in green for v in e)
        forbidden=set(RED)|set(green)
        for blue in matchings(n,forbidden):
            blue_count+=1;edges=(RED,green,blue)
            if rainbow(edges):continue
            raw+=1;key=canonical(edges)
            canonical_types.setdefault(key,normalize_edges(edges))
    records=[];uncovered=[]
    for key,edges in sorted(canonical_types.items()):
        cert=certificate(edges);n=1+max(v for c in edges for e in c for v in e)
        row={'canonical_slot_partition':key,'vertex_count':n,'edges_by_color':edges,'certificate':cert}
        records.append(row)
        if cert is None:uncovered.append(row)
    # A concrete realization of the first uncovered six-vertex type.  The
    # final coordinate is zero only because three independent coordinates
    # already suffice; all vectors are elements of F5^4.
    u=((1,0,0,0),(4,1,1,0),(0,1,0,0),(0,0,1,0),(2,0,4,0),(4,0,2,0))
    targets=((0,1,1,0),(1,1,0,0),(1,0,1,0))
    example_edges=(RED,((0,2),(1,4)),((0,3),(4,5)))
    def value_sum(values):return tuple(sum(v[j] for v in values)%5 for j in range(4))
    target_pairs=[]
    for target in targets:
        pairs=[pair for pair in __import__('itertools').combinations(range(6),2)
               if value_sum((u[pair[0]],u[pair[1]]))==target]
        target_pairs.append(pairs)
    assert tuple(tuple(row) for row in target_pairs)==example_edges
    assert not rainbow(example_edges)
    assert len(set(u+targets))==9 and all(any(x for x in v) for v in u+targets)
    direct_zero=[]
    all_values=u+targets
    for mask in range(1,1<<9):
        if value_sum([all_values[i] for i in range(9) if mask>>i&1])==(0,0,0,0):direct_zero.append(mask)
    assert not direct_zero
    replacement=[]
    for dmask in range(1,1<<6):
      for qmask in range(1,8):
        if dmask.bit_count()-qmask.bit_count()<3:continue
        if value_sum([u[i] for i in range(6) if dmask>>i&1])==value_sum([targets[c] for c in range(3) if qmask>>c&1]):
            replacement.append((dmask,qmask))
    assert not replacement
    example_key=canonical(example_edges)
    assert example_key in canonical_types and any(tuple(x['canonical_slot_partition'])==example_key for x in uncovered)
    counterexample={'edges_by_color':example_edges,'U_vectors':u,'target_vectors':targets,
      'target_pair_lists':target_pairs,'no_rainbow_3_matching':True,
      'all_511_nonempty_subsets_of_U_and_targets_checked':True,'nonempty_zero_subsets':direct_zero,
      'atom_replacement_identities_with_delete_minus_add_at_least_3':replacement,
      'interpretation':'Counterexample to the pure six-edge local lemma; no claim of extension to a 17-atom'}
    output={'status':'LOCAL_SIX_EDGE_LEMMA_DISPROVED',
      'scope':'Proper 3-colour graphs, two disjoint edges per colour, no rainbow 3-matching; F5 linear consequences',
      'fixed_red_green_matchings':green_count,'blue_augmentations_considered':blue_count,
      'raw_no_rainbow_augmentations':raw,'color_preserving_isomorphism_types':len(records),
      'certificate_kind_histogram':dict(Counter(r['certificate']['kind'] for r in records if r['certificate'])),
      'records':records,'uncovered':uncovered,'explicit_counterexample':counterexample,
      'script_sha256_before_output':sha256(Path(__file__).read_bytes()).hexdigest()}
    target=BASE/'evidence/continue_rainbow17_classify.json';target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    assert sha256(Path(__file__).read_bytes()).hexdigest()==output['script_sha256_before_output']
    print(json.dumps({k:output[k] for k in ('status','raw_no_rainbow_augmentations','color_preserving_isomorphism_types','certificate_kind_histogram')}))


if __name__=='__main__':main()
