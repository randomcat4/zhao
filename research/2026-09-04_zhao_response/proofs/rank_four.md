# Rank-four candidate audit

STATUS: **INCOMPLETE** for the frozen claim `K(C_n^4)=2n` for every prime power n. For primes p>=5, the existing binomial machinery reduces the missing upper bounds to exactly two lengths, `m=3p-2,3p-1`. The reduction below is a symbolic proof, not an inference from finite experiments. It still needs independent verification.

## Frozen statement and scope

Let G=C_n^4, n>=2 a prime power, D=4n-3, and let K be the smallest M in [n,D-1] for which every integer m in [M,D-1] satisfies s_{<=m}(G)<=2D-m. The supplied cube construction gives K>=2n. This note investigates the upper bound, with priority given to n=p>=5 prime. It does not modify the frozen quantifiers. Higher prime powers are not settled by the prime argument.

## Current literature, checked 2026-09-04

The original source is Kevin Zhao, arXiv:2506.21383v1, 2025-06-26. Its Theorem 1.13(ii) proves only m=2p in rank four, not the full tail.

A **published revision** is now available: Kevin Zhao and S. A. Hong, “On zero-sum subsequences over finite abelian groups of length not exceeding a given number”, Colloquium Mathematicum, online 2026-09-01, DOI 10.4064/cm9599-7-2026. Publisher page: https://www.impan.pl/en/publishing-house/journals-and-series/colloquium-mathematicum/online/116530/on-zero-sum-subsequences-over-finite-abelian-groups-of-length-not-exceeding-a-given-number . Direct PDF: https://www.impan.pl/shop/en/publication/transaction/download/product/116530 . Copies are saved beside this note as zhao_hong_2026.pdf and zhao_hong_2026.txt.

Published Theorem 1.3(1), p.3, still proves only m=2p for C_p^4, p>=5. Published Theorem 1.2 covers specified prime-power multiples m=c1*p^(t+1), not arbitrary tail integers. Published Conjecture 6.1, p.29, retains the upper assertion s_{<=k}(G)<=2D(G)-k for rank>=2, D=D*, k>=(D+1)/2. It drops the original K-equality wording and the separately numbered Conjecture 6.2. The rank-four cube obstruction still contradicts this retained conjecture at k=2n-1. No implication here should be described as merely refuting an obsolete preprint statement.

The original preprint Conjecture 6.1 (the equality s_{<=D-2}=D+1 under exp(G)<(D-1)/2 and its other hypotheses) is **absent as a conjecture from the published revision**. The published Theorem 1.1 gives the general upper bound D+2 with exceptions, and its Lemma 2.3(v) retains the known equality only for G=C_p^r with 3<=r<p. This is not a published proof of the original general equality conjecture. Published Conjecture 6.1 is the upper branch of old Conjecture 6.2, renumbered and reparameterized.

The bounded search did not locate a theorem covering the two residual rank-four lengths. This is **STATUS_UNCERTAIN**, not a certified assertion that they are open or that the partial theorem below is new.

## Why the single point does not establish the tail

Monotonicity only gives s_{<=m}(G)<=s_{<=2p}(G)<=6p-6 when m>=2p. The required right-hand side is 8p-6-m, which decreases by one whenever m increases. Monotonicity alone cannot supply that decrease. No valid general single-point-to-tail lemma was found or assumed.

## Partial theorem: all but two lengths for primes

**Claim proved from Zhao's Lemmas 4.4 and 5.1.** If p>=5 is prime and

    m in [2p,4p-4] minus {3p-2,3p-1},

then s_{<=m}(C_p^4)<=8p-6-m.

Write D=4p-3, k=m+1, L=2D-m. Suppose S is a sequence of length L with no nonempty zero-sum subsequence of length <=m. We use two cited lemmas from the original paper, keeping its numbering:

* Lemma 5.1: if S has no zero-sum subsequence of length >D and binom(D,m) is nonzero modulo p, then S has a zero-sum subsequence of length <=m.
* Lemma 4.4: if a zero-sum sequence T has t=|T|>=2k, 2k>=D+2, and for some 1<=i<=2k-D the coefficient

      a_i = binom(t-k,k-i) + (-1)^i binom(t-k+i-1,k-1)

  is nonzero modulo p, then T has a zero-sum subsequence of length <=m.

The two cited lemmas are retained in the published revision as Lemma 4.4 (pp.19-20) and Lemma 4.6 (p.24), respectively. All binomial coefficients outside their usual nonnegative lower-index range are interpreted as zero. We use Lucas' theorem for reduction modulo p.

First, D has base-p digits (3,p-3). Thus binom(D,m) is nonzero for every m in the claimed set; the only zeros in [2p,4p-4] are m=3p-2,3p-1.

If S has no zero sum longer than D, Lemma 5.1 contradicts the assumed absence of short zero sums. Otherwise take a zero-sum T with t>D. If t<2k, the definition of D gives a proper nonempty zero sum U in T of length <=D; both U and its nonempty complement have sum zero, and the shorter has length <=floor(t/2)<=k-1. Thus we only have to treat 2k<=t<=L.

For m>=3p this last interval is empty, since L<=5p-6<6p+2<=2k. This proves the entire interval [3p,4p-4].

It remains to consider m in [2p,3p-3]. Write

    k=2p+d,  1<=d<=p-2,
    x=t-k=up+v,  0<=v<=p-1.

The inequalities 2k<=t<=L imply

    2p+d <= x <= 4p-5-2d,

so u is either 2 or 3. In particular u=2 forces v>=d. The available coefficient indices extend to 2k-D=2d+3.

### Case 1: d=1

If v<=p-2, Lucas gives a_2=binom(u,2), which is 1 or 3 modulo p and hence nonzero. If v=p-1, the upper bound on x excludes u=3; consequently u=2 and a_2=binom(2,1)+binom(3,2)=5. Such an x is feasible only if 3p-1<=4p-7, or p>=6, so primality gives p>=7. Again the coefficient is nonzero. In both subcases 2<=2d+3.

### Case 2: d>=2 and v=p-1

Lucas gives a_2=binom(u,2)*binom(p-1,d-2)=binom(u,2)*(-1)^(d-2), because the second binomial has a zero units digit in its upper argument and units digit d-1>0 in its lower argument. This is nonzero for u=2,3 and p>=5.

### Case 3: d>=2 and d-2<=v<=p-2

Lucas and Pascal's identity give

    a_2 = binom(u,2) [binom(v,d-2)+binom(v+1,d-1)]
        = binom(u,2) binom(v,d-2) (v+d)/(d-1) mod p.

All factors except possibly v+d are nonzero. Thus only v+d=p needs further treatment. Then x=(u+1)p-d. The upper bound x<=4p-5-2d rules out u=3. Hence u=2, v>=d, and 2d<=p-1. At the permitted index i=2d, Lucas gives

    a_(2d) = binom(3p-d,2p-d) + binom(3p+d-1,2p+d-1)
            = 2+3 = 5 mod p.

Feasibility also implies 3p-d<=4p-5-2d, or d<=p-5. Since d>=2, p>=7 and this coefficient is nonzero. The index 2d is at most 2d+3.

### Case 4: d>=2 and 0<=v<d-2

Here u=3, because u=2 would force v>=d. Put q=d-v, so q>=3. If q is even, choose i=q. Lucas gives

    a_q = binom(3,2)*binom(v,v) + binom(3,2)*binom(d-1,d-1)
        = 6 mod p,

which is nonzero for p>=5.

If q is odd, choose i=q+1. Lucas gives

    a_(q+1) = 3 [binom(v,v-1)+binom(d,d-1)]
            = 3(v+d) mod p.

This includes v=0 under the zero convention. The only possible vanishing would be v+d=p. But u=3 would then give x=4p-d>4p-5-2d, contrary to the bound on x. Thus this coefficient is nonzero. Both chosen indices are <=d+1<=2d+3, and their base-p units digits are within range since d<=p-2.

These cases exhaust x. Lemma 4.4 now gives the contradiction and proves the partial theorem.

## Exact residual proof obligations

For primes p>=5, the full candidate K=2p is now equivalent, using the supplied lower bound and the partial theorem above, to the conjunction

    s_{<=3p-2}(C_p^4) <= 5p-4,
    s_{<=3p-1}(C_p^4) <= 5p-5.

For example the first unresolved prime p=5 requires s_{<=13}(C_5^4)<=21 and s_{<=14}(C_5^4)<=20. These are not counterexamples; they are the two uncovered obligations. At m=3p-3 the proved upper bound is 5p-3. Monotonicity preserves that number and misses the two target bounds by 1 and 2, respectively; it does not fill either hole.

At either residual length, any hypothetical bad sequence automatically has no zero-sum subsequence longer than D: such a zero sum would split into a short one because L<2k. Thus the gap is entirely in the “no long zero sums” part of the argument. Lemma 5.1 cannot contradict that case, since Lucas gives binom(4p-3,3p-2)=binom(4p-3,3p-1)=0 modulo p. Merely repeating the same determinant or binomial argument does not close this gap. A stronger constraint on these bad sequences, a different congruence, or a verified external theorem is needed.

Consequently this note does **not** prove K=2p, let alone K=2n for all prime powers. It does prove, subject to independent checking of this derivation and the cited lemmas, 2p<=K<=3p for prime p>=5.

## Provenance and checks

One bounded rank-four audit/proof unit; no Euler calls, no subagents. Exact BigInt probes of the two cited lemmas for all primes 5<=p<=97 and all m in [2p,4p-4] first identified the two holes. The proof above supersedes the finite probe as support for the partial theorem. No finite probe is being used as a proof of a universal claim. No novelty claim is made. Higher prime powers and the small prime cases p=2,3 remain outside this partial derivation.
