        V = set(range(n))
        for k, coefficient in [(2,1),(4,3)]:
            B = set(range(k)); BC=V-B
            for i in range(n):
                contrib = sum((-1)**len(U) for U in (B,BC) if i not in U)
                expected = 1 - 2*int(i in B)
                assert contrib == expected
                checked += 1
            c1 = ((-1)**k)*coefficient + ((-1)**(n-k))*(-coefficient)
            ell = ((-1)**k)*k + ((-1)**(n-k))*(n-k)
            assert c1 % p == 2*coefficient % p
            assert ell % p == 2*k % p
        assert pow(2,-1,p) == (p+1)//2
    assert det_q([[1,3],[2,4]]) == -2
    return {"single_deletion_contributions":checked,
            "quad_degree_residue":"+(p+1)/2, not (p-1)/2",
            "moment_matrix_determinant":-2}


def check_small_type_annihilators() -> list[dict]:
    out=[]
    for j in range(5):
        pts = [(Fraction(2*(c+d)-j,2),c)
               for c in range(1,4) for d in range(1,j+2)
               if c != 2 or d >= 2]
        parity = (j+1)%2
        mon=[(a,b) for a in range(j+3) for b in range(j+3-a)
             if (a+b)%2 == parity]
        A=[[x**a*Fraction(c)**b for a,b in mon] for x,c in pts]
        rk=rank_q(A)
        assert rk == len(mon)
        out.append({"j":j,"formal_types":len(pts),"polynomial_dimension":len(mon),
                    "rank_over_Q":rk,"annihilator_dimension":len(mon)-rk})
    return out


def partitions(n: int, maxpart: int|None=None):
    if n == 0:
        yield []
        return
    if maxpart is None:
        maxpart=n
    for j in range(min(n,maxpart),1-1,-1):
        for rest in partitions(n-j,j):
            yield [j]+rest


def check_kernel_lemma() -> dict:
    out=[]
    for k in range(3,11):
        vals=[]
        for part in partitions(k-1):
            prod=math.prod(math.comb(b+k-1,b) for b in part)
            assert prod <= k**(k-1)
            vals.append(prod)
        assert max(vals)==k**(k-1)
        out.append({"uniformity":k,"max_degree_bound":max(vals)})
    assert 4**3 == 64 and (131+1)//2 > 64
    return {"partition_bounds":out,"quad_prime_cutoff":131}


def check_full_quad_counterfamily() -> dict:
    base=[1,10,100]
    u=[1000,10000,100000]
    pairs=[(0,1),(0,2),(1,2)]
    v=[-base[i]-base[j]-u[t] for t,(i,j) in enumerate(pairs)]
    values=base+[z for uv in zip(u,v) for z in uv]
    intended=[tuple(sorted((i,j,3+2*t,4+2*t))) for t,(i,j) in enumerate(pairs)]
    zeros=[]; checked=0
    for C in it.combinations_with_replacement(range(9),4):
        checked+=1
        if sum(values[i] for i in C)==0:
            zeros.append(C)
    assert sorted(zeros)==sorted(intended)
    assert checked==math.comb(12,4)
    threshold=4*max(abs(x) for x in values)
    assert threshold==400440
    p=threshold+1
    while any(p%d==0 for d in range(2,math.isqrt(p)+1)):
        p+=1
    m=3
    S=[(x,0) for x in base]
    target=(0,3)
    desired=[]
    for t,(i,j) in enumerate(pairs):
        for z in range(m):
            k=len(S)
            S.extend([(u[t]%p,z),(v[t]%p,(3-z)%p)])
            desired.append(frozenset((i,j,k,k+1)))
    assert len(set(S))==len(S)
    all_blocks=[]
    for C in it.combinations(range(len(S)),4):
        if tuple(sum(S[i][d] for i in C)%p for d in range(2))==target:
            all_blocks.append(frozenset(C))
    assert set(all_blocks)==set(desired)
    assert all(A&B for A,B in it.combinations(all_blocks,2))
    assert not set.intersection(*(set(B) for B in all_blocks))
    assert set.union(*(set(B) for B in all_blocks))==set(range(len(S)))
    m_full=(p-1)//2
    assert 3+6*m_full==3*p
    assert ((1-2*m_full)*sum(base))%p==222
    return {"first_coordinate_multisets_checked":checked,
            "only_zero_types":[list(x) for x in zeros],
            "valid_for_every_prime_greater_than":threshold,
            "concrete_prime":p,"concrete_m":m,
            "concrete_full_family_blocks":len(all_blocks),
            "full_parameter_union_size":"3p",
            "not_Ap_counterexample":"total first coordinate is 222 mod p; private degree is 1"}


def projective_vectors(p:int):
    for i in range(4):
        for tail in it.product(range(p), repeat=3-i):
            yield (0,)*i+(1,)+tail


def check_squarefree_relaxation() -> list[dict]:
    out=[]
    for p in [5,7,11,13,17,19]:
        squares={x*x%p for x in range(1,p)}
        d=next(x for x in range(1,p) if x not in squares)
        xy=[(0,0),(1,0),(p-1,0),(0,1)]
        used=set(xy)
        for x,y in it.product(range(p), repeat=2):
            if (x,y) not in used:
                xy.append((x,y)); used.add((x,y))
            if len(xy)==5*p-5:
                break
        assert len(xy)==5*p-5
        S=[(1,x,y,(x*x-d*y*y)%p) for x,y in xy]
        S.append((2,0,0,1))
        assert len(set(S))==len(S)==5*p-4
        canon=[]
        for v in S:
            scale=pow(next(x for x in v if x),-1,p)
            canon.append(tuple(scale*x%p for x in v))
        assert len(set(canon))==len(S)
        lookup=set(S); aps=0
        for v,w in it.combinations(S,2):
            mid=tuple((x+y)*pow(2,-1,p)%p for x,y in zip(v,w))
            if mid in lookup:
                aps+=1
        assert aps==0
        diffs=[[(x-y)%p for x,y in zip(v,S[0])] for v in S[1:]]
        assert rank_mod(diffs,p)==4
        assert sum(v[0] for v in S)%p == p-3
        maximum_n0=0; number=0
        for lam in projective_vectors(p):
            n0=sum(sum(a*b for a,b in zip(lam,v))%p==0 for v in S)
            maximum_n0=max(maximum_n0,n0); number+=1
        assert number==p**3+p**2+p+1
        assert maximum_n0<=3*p-3
        out.append({"p":p,"n":len(S),"nonsquare":d,
                    "D_eq":0,"D_col":0,"A_ap":0,"affine_rank":4,
                    "projective_functionals_checked":number,
                    "max_n0":maximum_n0,
                    "forbidden_lengths_from_first_coordinate":[1,p-2]})
    return out


def main() -> None:
    report={"status":"FINITE_INTERFACES_PASS_ONLY",
            "proves_Ap":False,"proves_height_p_minus_5":False,
            "normal_forms":check_normal_forms(),
            "core_interfaces":check_core_interfaces(),
            "quad_moments":check_quad_moments(),
            "formal_low_degree_probe":check_small_type_annihilators(),
            "kernel_lemma":check_kernel_lemma(),
            "full_quad_counterfamily":check_full_quad_counterfamily(),
            "squarefree_relaxation":check_squarefree_relaxation()}
    report["script_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=ROOT/'verification_report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({"status":report["status"],
                     "parameter_cases":report["normal_forms"]["parameter_cases"],
                     "coefficient_checks":report["normal_forms"]["coefficient_checks"],
                     "quad_counterfamily_type_checks":report["full_quad_counterfamily"]["first_coordinate_multisets_checked"],
                     "report":path.name},ensure_ascii=False))

if __name__=='__main__':
    main()
