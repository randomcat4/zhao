# Structural and small-support route

STATUS: **INCOMPLETE** for the conjunction in frozen_theorem_v1.md, and hence for K(C_p^4)=2p. No counterexample was found. This is one bounded work unit; no Euler call, no spawned agents, no reading of other first-round drafts.

## Exact outputs and their scope

1. **PROVED:** for every prime p>=5, a counterexample at either frozen endpoint must span C_p^4 and have at least six distinct support elements.
2. **EXHAUSTIVE COMPUTATIONAL CHECK, NOT A GENERAL PROOF:** for p=5, neither endpoint admits a counterexample supported on at most six distinct elements. The exact, exhaustive integer computation is supplied in structural_support6.ps1. Together with item 1 and the rank reduction, it leaves only full-rank support at least seven for p=5. This does not determine K(C_5^4).
3. The bounded primary-source search below did not identify a stronger published theorem closing either endpoint. Literature status remains uncertain, not certified open.

## Elementary structural restrictions (PROVED_HERE)

Write (N,m)=(5p-4,3p-2) or (5p-5,3p-1), and suppose S has length N and no nonempty zero sum of length at most m.

**Full rank.** If the support spans a subgroup of rank at most three, Davenport's formula for elementary p-groups gives a zero sum of length at most D(C_p^3)=3p-2<=m. Thus S spans rank four.

**Multiplicity bound.** Zero cannot occur, and every other element has order p, so every multiplicity is at most p-1.

**Support bound for the first endpoint.** Five support elements can account for at most 5(p-1)=5p-5<N terms. Thus support has size at least six.

**Support bound for the second endpoint.** If support has size at most five, the multiplicity bound forces exactly five elements, each repeated p-1 times. Let them be g_1,...,g_5. A nonzero relation c_1g_1+...+c_5g_5=0 over F_p exists. For each t in F_p^*, take the least nonnegative residues [tc_i]_p as subsequence multiplicities. These lie in [0,p-1], so each gives a nonempty zero sum in S. If h is the number of nonzero c_i, each nonzero coordinate runs once through 1,...,p-1 as t varies. Therefore the average subsequence length is hp/2<=5p/2. Some nonempty zero sum has integer length at most floor(5p/2)<=3p-1. This contradicts the hypothesis. No classification of long atoms is assumed.

**All zero sums are atoms.** A zero sum T with |T|>D=4p-3 contains a proper nonempty zero sum U with |U|<=D. Both U and T\U are nonempty zero sums, and the shorter has length at most floor(N/2)<=m at either endpoint. Thus no zero sum is longer than D. A nonminimal zero sum of any length at most D also splits and has a component shorter than m. Consequently all nonempty zero sums in a bad S are minimal, with lengths in [3p-1,4p-3] at the first endpoint and [3p,4p-3] at the second.

These restrictions are strictly weaker than the target; they do not establish a new equivalent lemma as purported progress.

## Exact p=5, support-six computation

The executable requires only PowerShell's built-in C# compiler:

    & .\math\2026-09-04_zhao_exact\proofs\structural_support6.ps1

Actual completed output on 2026-09-04:

    matrices=191890 patterns20=120 patterns21=56 checks20=23026800 checks21=10745840 bad20=0 bad21=0

All arithmetic is exact integer arithmetic. The executable writes a BAD line for every counterexample it finds; there were no such lines. This is an exhaustive check of the specified family, not randomized sampling or a claim of Lean verification.

### Why the finite parameterization is exhaustive

Any rank-four support of size six has four linearly independent elements. Apply a group automorphism and order its support to write the six columns as

    A = [ I_4 | a | b ].

The two extra columns are distinct, nonzero, and different from the four standard basis vectors. There are 620 eligible vectors in F_5^4 and binom(620,2)=191890 unordered pairs. Ordering a<b loses nothing, because all multiplicity vectors are enumerated, including swaps of their last two entries.

For length20 the six positive multiplicities w_i are in [1,4] and sum to20: exactly120 vectors. For length21 the analogous count is56. The script enumerates them without assuming any order among the four basis multiplicities.

For each matrix, every residue vector in its kernel is uniquely

    ([-t a_1-u b_1]_5,...,[-t a_4-u b_4]_5,t,u),
    (t,u) in F_5^2.

Because all multiplicities are below5, a nonempty subsequence zero sum corresponds exactly to one of the24 nonzero such vectors with all six entries <=w_i. Its length is the integer sum of the entries. The script explicitly looks for length<=14 in the length20 case and length<=13 in the length21 case. Every enumerated pair and multiplicity vector has such a witness.

Rank at most three and support at most five have already been handled analytically, so this covers all p=5 sequences of support at most six. It does not cover seven or more support elements, nor does it prove the analogous support-six claim for unbounded primes. A fresh reviewer can audit the normalization and rerun the 34-million-case check; no independent external verification has yet been performed on this artifact.

## Primary-source comparison and exact non-implications

* Zhao–Hong, *On zero-sum subsequences over finite abelian groups of length not exceeding a given number*, published online 2026-09-01, DOI 10.4064/cm9599-7-2026. The supplied local full text was checked. Theorem1.3(1) covers m=2p; Theorem1.3(2) covers m=3p in rank four. Neither states either missing endpoint. Theorem1.1 concerns D-2=4p-5, which also misses them, including p=5 where the endpoints are13,14 and D-2=15.
* Benjamin Girard, *On the existence of zero-sum subsequences of distinct lengths*, Rocky Mountain J. Math.42 (2012),583–596; [author's arXiv full text](https://arxiv.org/pdf/0903.3458), Theorem2.3. At length D+i-1 it allows avoidance of any i-1 prescribed nonzero residues modulo p. Here i=p or p-1. Because the possible zero-sum lengths lie in the intervals displayed above, one may avoid all their nonzero residues and thereby force a zero sum of length exactly3p. This is useful structure but is compatible with the bad-sequence hypothesis; it is not the desired shorter zero sum.
* Gao–Li–Zhao–Zhuang, *On sequences over a finite abelian group with zero-sum subsequences of forbidden lengths*, Colloq. Math.144 (2016),31–44, DOI10.4064/cm6488-8-2015; [publisher full text](https://www.impan.pl/shop/en/publication/transaction/download/product/91401). Theorem1.5 gives disc(C_p^4)=5p-3, which exceeds both target sequence lengths. Theorem5.5 addresses a single forbidden length not divisible by p and cannot exclude the forced3p zero sum. Theorem5.6 treats multiples kp with k<=ceil(r/2), hence k<=2 in rank four, and does not cover k=3. These results do not provide the missing implication.

## Remaining obstacle and route assessment

A bad sequence would be a full-rank sequence with bounded multiplicities, only long minimal zero sums, and at least one minimal zero sum of length3p. The available inverse results for normal sequences impose a different hypothesis (an upper bound on *all* zero-sum lengths near |S|-D+1); the present bad sequence is not such a normal sequence. No valid transformation to that setting was obtained. Invoking normal-sequence structure here without proving that transformation would be a gap.

For p=5 the explicit restricted check rules out the smallest possible support, but at least seven support elements remain. The frozen two-endpoint theorem is therefore **INCOMPLETE**. No assertion of novelty, global truth, or exact K(C_5^4) is justified by this work unit.
