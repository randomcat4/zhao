# Frozen local theorem: the nine 127-candidate cores

Status: **PROVED for the nine specified cores**, by finite coefficient certificates and the elementary quotient proof below. This is a local exclusion, not a proof of all endpoint A or B sequences.

## 1. Exact scope and coordinates

Work in G=F_5^4 with encoding

    enc(x_1,x_2,x_3,x_4)=x_1+5x_2+25x_3+125x_4.

Let e=e_1 and H={x_1=0}. For a triple of encoded vectors B, define the fifteen-position core

    W(B)=e_1^3 e_2^2 e_3^2 e_4^2 product_{g in B} g^2.

This note concerns exactly the following nine triples:

    (345,455,505), (215,225,565), (160,185,505),
    (45,180,305), (45,220,345), (45,415,485),
    (30,190,315), (30,210,335), (30,420,480).

Every encoded block is divisible by five, so all six doubled support elements are in H. Thus W(B)=e^3 U(B), where |U(B)|=12 and U(B) is contained in H.

**Local theorem.** Every twenty-position sequence in G containing any U(B) has a nonempty zero sum of length at most thirteen. In particular, none of the nine W(B) can extend to a bad B sequence of length twenty, or to a bad A sequence of length twenty-one. The theorem does not assume that the added positions are distinct, that their multiplicities are bounded, or that they avoid the core support.

The stronger twenty-position conclusion also applies to A: a twenty-one-position sequence containing U(B) has a twenty-position subsequence retaining U(B).

## 2. Finite profile and equivalence certificates

All nine U(B) are equivalent under GL(H), with e fixed in G. A convenient representative, using a=e_2,b=e_3,c=e_4, is

    U=a^2 b^2 c^2 (a+b)^2 (3a+2b+c)^2 (3a+2b+2c)^2.

Its total sum is

    sigma(U)=a+2b+3c != 0.

For each of the nine cores, an exhaustive check of the 3^6=729 coefficient tuples in {0,1,2}^6 proves that U(B) is zero-sum-free and has the following minimum-subsequence-length distribution over all 125 points of H. The empty subsequence is permitted for the target zero.

| Minimum length | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Number of targets | 1 | 6 | 19 | 36 | 35 | 19 | 8 | 1 |

The sole target of minimum length twelve is sigma(U(B)). Therefore every other target in H has a subsequence representation using at most six positions.

`scripts/atom_127_classify.py` produces `evidence/atom_127_classification.json`. For each core, it stores all 125 targets with an explicit minimum-length coefficient representation, every coordinate of a GL(H) matrix carrying its six support elements to the representative, and the nonzero determinant. There is no extension search in this certificate computation.

For convenient inspection, the matrices below act on column vectors in coordinates (e_2,e_3,e_4). Semicolons separate rows. Every matrix maps the indicated source support to the representative support above.

| Source B | Matrix to representative | Determinant mod 5 |
|---|---|---:|
| (345,455,505) | (1,3,1; 1,2,0; 0,2,0) | 2 |
| (215,225,565) | (1,0,3; 1,0,2; 0,1,2) | 1 |
| (160,185,505) | (1,0,1; 1,0,0; 0,1,0) | 1 |
| (45,180,305) | (1,1,0; 0,1,0; 0,0,1) | 1 |
| (45,220,345) | (1,1,3; 0,1,2; 0,0,1) | 1 |
| (45,415,485) | (1,1,3; 0,1,2; 0,0,2) | 2 |
| (30,190,315) | (1,0,0; 0,1,0; 0,0,1) | 1 |
| (30,210,335) | (1,0,3; 0,1,2; 0,0,1) | 1 |
| (30,420,480) | (1,0,3; 0,1,2; 0,0,2) | 2 |

The separate plain-integer verifier `scripts/atom_127_verify.py` checks every matrix image and determinant, all 6561 coefficient tuples across the nine cores, all 1125 saved target representations, the distance histograms, and the safe-addition lists. Its complete result is `evidence/atom_127_verification.json`. Both scripts use only finite modular arithmetic.

## 3. An eight-position lemma in C_5

Let R be any eight-position sequence of nonzero elements of C_5. Then either some value occurs at least six times, or R has two disjoint nonempty zero-sum subsequences whose total length is at most seven.

If R contains a pair x,-x, remove that pair. Among any five of the six positions left there is a nonempty zero sum of length at most five: the six partial sums, including the initial zero, contain a repetition. This gives the required two disjoint zero sums of total length at most seven.

Otherwise R uses at most one member of each of the two opposite pairs {1,4} and {2,3}, so it uses at most two values. A single value already occurs eight times. For two nonopposite values, after interchanging them if necessary and scaling, the values are x and 2x. If neither occurs six times, their multiplicities are (3,5), (4,4), or (5,3). In the first two cases take two disjoint copies of (x,2x,2x), of total length six. In the last case take the disjoint blocks (x,x,x,2x) and (x,2x,2x), of total length seven. This exhausts all cases.

## 4. Dense twelve-position hyperplane interface

Let H be a hyperplane of G and U a twelve-position zero-sum-free sequence in H. Write sigma=sigma(U), and assume that every h in H other than sigma is represented by a subsequence of U of length at most six. Then every twenty-position sequence S containing U has a nonempty zero sum of length at most thirteen.

Assume the contrary and put t=-sigma. Because U is zero-sum-free, sigma and t are nonzero. The target sigma is represented by U itself, and every other target has a representation of length at most six. Thus an extra position g of S lying in H would be cancelled by at most twelve positions of U, giving a forbidden zero sum of length at most thirteen. Consequently S has exactly the twelve specified positions in H, and its remaining eight positions R all have nonzero image in G/H=C_5.

Consider any nonempty subsequence Q of R with |Q|<=7 and with quotient sum zero. Its actual sum lies in H. If sigma(Q) were not t, then -sigma(Q) would not be sigma, and at most six positions of U would cancel Q. This would produce a zero sum of length at most 7+6=13. Hence

    sigma(Q)=t

for every such Q.

Apply the eight-position lemma to the quotient sequence of R. If it supplies two disjoint zero-sum subsequences Q_1,Q_2 whose combined length is at most seven, the rule above applies to Q_1, Q_2, and their union. It gives

    sigma(Q_1)=sigma(Q_2)=sigma(Q_1 Q_2)=t,

but additivity gives sigma(Q_1 Q_2)=2t. Thus t=0, a contradiction.

In the other case, choose six positions of R with the same nonzero quotient value. Every five of these positions have quotient sum zero, and therefore actual sum t. Comparing two five-position subsequences omitting different positions shows that all six actual group elements are equal. Five copies of any element of G sum to zero, contradicting either the nonzero value t or the assumed absence of a short zero sum.

This proves the interface. It needs no multiplicity classification of S, no prior exclusion of four tripled elements, and no hypothesis that the eight outside positions are distinct. The argument uses only the elementary C_5 lemma just proved and the finite profile hypothesis.

Applying the interface to the nine certified U(B) proves the frozen local theorem.

## 5. Exact safe-candidate geometry and an alternative e^3 proof

This section preserves the independent argument obtained directly from the nine e^3 U cores. It is not needed for the shorter interface proof.

Write C=-sigma(U), and write a group point as k e+h with h in H. Since W=e^3 U is a direct-sum concatenation, its minimum subsequence length for the target k e+h is k+d_U(h) for k=0,1,2,3, and the target is unattained for k=4. These formulas were also checked against all 4*3^6=2916 coefficient tuples for every core.

It follows, with the signs fixed as written, that the exact individually safe additions are

    cutoff 13: (e+H) union {2e+C,3e+C,4e+C};
    cutoff 14: (e+H) union {2e+C,3e+C}.

The first set has 128 elements and the second has 127. Removing the existing core support removes e only, giving respectively 127 and 126 outside-support candidates. In particular, the A outside-support set is a 125-point coset with one point removed, together with three exceptional points. It is not a complete 125-point coset together with two points.

Suppose an endpoint extension contains an exceptional value y=k e+C. If it also contains x=e+h with h!=0, combine y,x with 4-k of the three fixed copies of e. The quotient sum is zero; the actual H sum is C+h, whose negative is sigma(U)-h != sigma(U). It can therefore be cancelled by at most six positions of U. The resulting zero sum has length at most (6-k)+6<=10. Thus the presence of any exceptional value forces all values in e+H to equal e. Every outside-H position then belongs to the plane K=span(e,C).

For A there are nine outside-H positions. The standard value D(C_5^2)=9 gives a zero sum of length at most nine in this plane. For B there are eight outside-H positions T. If T is not zero-sum-free, it already contains a forbidden short zero sum. If T is zero-sum-free, its length is D(K)-1, so its subsequence sums, including the empty sum, cover K: otherwise appending the negative of an omitted point contradicts D(K)=9. Since C!=sigma(U), the element C is represented inside U using at most six positions. A subsequence of T sums to -C using at most eight positions, giving a zero sum of length at most fourteen. This excludes the exceptional-value case in both endpoints.

If there is no exceptional value, all eight or nine outside-H positions lie in e+H. Every five-position sum lies in H and must equal C, since any other sum would be cancelled inside U with at most six positions, giving a zero sum of length at most eleven. Among at least six positions, equality of all five-position sums forces all actual values to be equal. This again produces a five-position zero sum.

The alternative proof uses the standard plane Davenport value already present in the earlier route. The main proof in Sections 3-4 avoids that additional dependency entirely.

## 6. Scope of completion

All nine previously exceptional 127-candidate cores are excluded from both endpoints; indeed their twelve-position H parts force a <=13 zero sum already at length twenty. No five-subset combinations were enumerated in this work unit. The other length-fifteen cores, the incomplete H=11 outside search, and the global endpoint claims are outside this local result.

The dense-hyperplane interface was communicated by the root agent and independently checked here. The e^3 proof in Section 5 was obtained on this route and retained for review. No other current working proof draft was used.
