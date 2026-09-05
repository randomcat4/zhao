# Algebra / counting route: complete scalar congruence breakpoint

STATUS: **INCOMPLETE** for both frozen inequalities and for K(C_p^4)=2p.

This is one bounded independent proof unit. No premises were changed, no Euler call or child agent was used, and no other current proof route was read. All sequences below count subsequences by positions. The new results are necessary conditions on any counterexample, together with a proof that the complete length-averaged mod-p system is consistent. They are not a counterexample to the frozen theorem.

## 1. Parameters and a self-contained algebraic identity

Let p>=5 be prime, D=4p-3, and take either

* A: m=3p-2, n=5p-4, r=D-m=p-1; or
* B: m=3p-1, n=5p-5, r=D-m=p-2.

In both cases n=D+r=2D-m. Suppose S has length n and has no nonempty zero-sum subsequence of length at most m. Write Z_j(U) for the number of zero-sum j-subsequences of a sequence U.

Every nonempty zero-sum subsequence of S has length in [m+1,D]. Indeed, if a zero-sum T has |T|>D, Davenport's definition supplies a nonempty proper zero-sum V inside it with |V|<=D. The two nonempty zero-sum pieces V and T\V have a shorter one of length at most floor(n/2)<=m. This contradicts the assumption. The last inequality holds at p=5 as well: floor(21/2)=10<=13 and floor(20/2)=10<=14.

For completeness, the group-algebra congruence used here needs no additional structural assumption. Over F_p, write

    F_p[C_p^4] = F_p[y_1,y_2,y_3,y_4]/(y_1^p,...,y_4^p),

where y_i=X^{e_i}-1. Every 1-X^g lies in the augmentation ideal I=(y_1,...,y_4). Since I^{4(p-1)+1}=0, every product of D or more factors 1-X^{g_i} is zero. Taking its identity coefficient gives, for every U with |U|>=D,

    sum_j (-1)^j Z_j(U) = 0  (mod p).                 (1)

This is also published Zhao--Hong Lemma 4.2; the local source is `math/2026-09-04_zhao_response/proofs/zhao_hong_2026.txt`, at its Lemma 4.2.

## 2. PROVED_HERE: the complete length-count vector is forced

For S, and also for every sequence S with one position deleted, one has

    Z_{3p} = 1  (mod p),
    Z_j = 0  (mod p) for all j in [m+1,D] other than 3p.       (2)

In particular, a hypothetical counterexample contains a 3p-term zero-sum atom. Furthermore every fixed position belongs to a multiple of p such atoms, and belongs to a multiple of p zero-sum j-subsequences for every other allowed length j.

### Proof

Let U be either S or S with one position removed, and set N=|U|. Sum (1) over all subsequences of U formed by deleting t positions. For every integer 0<=t<=N-D this yields

    binom(N,t) + sum_{j=m+1}^D binom(N-j,t) x_j = 0 (mod p), (3)
    x_j=(-1)^j Z_j(U).

There are r unknowns. Both N=n and N=n-1 permit all r rows t=0,...,r-1. The numbers N-j, as j runs in reverse order, are r consecutive integers. The square matrix

    [binom(b+i,t)]_{0<=t,i<r}

has determinant 1 over the integers for every nonnegative integer b. One proof subtracts each preceding column from its successor and uses Pascal's identity, then inducts on r. Therefore these r rows have a unique solution over F_p.

The index j=3p belongs to [m+1,D], including p=5. Also N-3p>=0. For every t<p,

    binom(N,t) = binom(N-3p,t) (mod p),

because t! is invertible modulo p and the two upper arguments agree modulo p. Thus x_{3p}=-1 and all other x_j=0 solve the r rows. They solve the additional row t=r when N=n as well, because r<p. As 3p is odd, this is exactly (2).

Subtract the result for U=S with a fixed position deleted from the result for S to obtain the stated incidence congruences. A 3p-zero-sum is an atom: a proper nonempty zero-sum inside it would leave a nonempty zero-sum complement, and one of the two pieces would have length at most floor(3p/2)<=m.

### Explicit smallest-prime boundary

For p=5, case A has n=21,m=13,D=17. The forced vector on lengths 14,15,16,17 is (0,1,0,0) modulo 5, for S and for each 20-position subsequence obtained by deleting one position. Case B has n=20,m=14,D=17, and the vector on lengths 15,16,17 is (1,0,0), for S and for each 19-position subsequence obtained by deleting one position. These statements follow from the symbolic proof; they are not finite evidence substituted for it.

## 3. PROVED_HERE: exact failure of the full scalar method

The complete system (3), with every available row t=0,...,n-D, is consistent and has the unique solution just displayed. Thus no linear combination of these rows can contradict counterexample existence. This is a strictly more explicit diagnosis than merely observing one binomial coefficient vanishes: it gives the full modular solution and proves its uniqueness for every prime p>=5.

The usual Chevalley--Warning congruence with a fifth equation recording subsequence length adds no contradiction to this vector, even after adjoining any number a of zero elements.

To see this, regard (2) as a *formal* count vector, with Z_0=1, Z_{3p}=1, and all other entries zero. After adjoining a zero elements, the formal counts are

    Z'_j = binom(a,j) + binom(a,j-3p).

For every residue c modulo p,

    sum_{j congruent c mod p} (-1)^j Z'_j = 0 (mod p).       (4)

In fact the two sums cancel exactly over the integers: shift j by 3p in the second sum, preserve its residue, and reverse its sign. Consequently every homogeneous length-mod-p Chevalley--Warning identity whose variable-count threshold is met is satisfied by the vector. In particular the extra length equation for case A gives Z_{3p}=1, and adding one zero in case B gives the same condition.

This is a no-go statement for **length-averaged scalar mod-p congruences and these padded length-residue identities only**. It is not a claim that all individual-subsequence congruences, all nonzero group coefficients, higher p-adic identities, or the actual F_p-linear representation by group elements are exhausted. The formal count vector is not an actual group sequence.

## 4. PROVED_HERE: a small-support exclusion

Any counterexample in either case has at least six distinct elements in its support.

Every multiplicity is at most p-1, since p copies give a p-term zero sum. Therefore case A, whose length is 5(p-1)+1, needs at least six support elements by counting.

In case B, support at most five would require exactly five distinct elements, each of multiplicity p-1. Their span must have rank four; otherwise D(C_p^s)=s(p-1)+1<=3p-2<=m for s<=3 gives a forbidden short zero sum. Choose four support vectors forming a basis, and write the fifth as v=sum_{i=1}^4 a_i e_i. For each t=1,...,p-1 there is an available zero-sum subsequence consisting of t copies of v and [-t a_i]_p copies of e_i, where residues are taken in [0,p-1]. Let its length be l(t). Then

    l(t)+l(p-t) = (1 + #{i:a_i != 0})p <= 5p.

Both sequences are nonempty. One therefore has length at most floor(5p/2)<=3p-1, a contradiction. All basis-coordinate multiplicities used are available, and repeated elements were handled at the start.

This lemma concerns a class of sequences; it is not an exact evaluation of K for a new prime subfamily.

## 5. Minimal remaining obstruction and verdict

The route has not proved that actual rank-four sequences can or cannot realize the modular pattern (2). A completion must exploit a constraint not implied by the scalar system above; for example, actual position-incidence constraints together with the rank-four realization, stronger integer/p-adic information, or additional structural information on the forced 3p-atoms.

The exact frozen goals remain INCOMPLETE, including p=5. No value K(C_p^4)=2p is asserted, no counterexample to either inequality is supplied, and no novelty claim is made. Finite modular row-reduction probes at p=5,7,11,13 suggested (2); the general proof in Section 2 supersedes those probes. No Lean verification was performed.
