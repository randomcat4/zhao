CORRECT

# Fresh adversarial review of the squarefree projection proof

## Object reviewed

The frozen target is the statement in
`harvested_chat/squarefree_projection_proof.md`: every 21-element subset of
\(\mathbb F_5^4\) has a nonempty zero-sum subset of size at most 13.  I treated
the harvested status label as having no evidentiary value and reconstructed the
finite certificate from the numbers and definitions printed in the proof.

## External inputs

The only two mathematical inputs used by the argument are correctly stated.
The published version of Ordaz--Philipp--Santos--Schmid, *On the Olson and the
Strong Davenport constants*, Theorem 8.1(3), states
\(SD(C_5^4)=16\) and \(O(C_5^3)=12\).  Definition 3.1 and its following
paragraph define \(SD\) as the maximum cardinality of a squarefree minimal
zero-sum sequence, exactly the meaning needed in P1 and P7.  The published
source checked was <https://jtnb.centre-mersenne.org/item/10.5802/jtnb.784.pdf>.

## P1--P2: group-ring and deletion equations

The augmentation ideal calculation is sound.  In characteristic five,
\(I^{4d+1}=0\), so the coefficient of the identity in
\(\prod_{i\in Q}(1-X^{v_i})\) gives
\(1+\sum_k(-1)^kZ_k(Q)=0\pmod 5\) for \(|Q|\ge4d+1\).  Summing this over the
\(q\)-subsets of an \(n\)-set counts each \(k\)-zero-sum subset
\(\binom{n-k}{q-k}\) times, giving equation (3) with the displayed signs.

Under the counterexample hypothesis, a zero-sum of length 17--21 contains a
squarefree minimal zero-sum of length 14--16 by \(SD(C_5^4)=16\); its nonempty
complement has length at most seven and is also zero-sum.  Hence only lengths
14--16 remain.  Exhaustive solution of every deletion equation over
\(\mathbb F_5\) gives precisely:

- \(n=17\): \(1+a-b+c=0\);
- \(n=18\): \(a=c\), \(b=1+2c\);
- \(n=19,20,21\): \((a,b,c)=(0,1,0)\).

The complement identity
\(\lambda_j(D)=Z_{21-j}(S\setminus D)\) has the correct containment/avoidance
direction.

## P3--P5: the two short bounds and the anchors

Deleting one occurrence of \(x\) from a length \(4d+2\) sequence leaves only
possible zero-sums of lengths \(4d\) and \(4d+1\), and their exact counts give

\[
1+m(t-x)-\mathbf1_{2x=t}-\mathbf1_{x=t}=0\pmod5.
\]

Five equal values are already a forbidden length-five zero-sum, so all
multiplicities are at most four.  The case \(2x=t\) is impossible (the omitted
case \(x=t\) would force \(x=t=0\), also forbidden).  All values other than
\(t\) therefore occur in pairs \(\{x,t-x\}\), each value four times.  For
\(d=3\), the total 14 is impossible modulo eight.  For \(d=4\), the total 18
forces two such pairs and two copies of \(t\); four copies from each pair plus
one member of each value in the other pair form the stated length-ten
zero-sum.  Thus both bounds in P3 follow.

P4's graph argument is complete: every vertex deletion leaves an opposite
pair; two disjoint edges would give a four-term zero-sum; a triangle would
force \(2x=0\) for a nonzero label.  A triangle-free graph with matching
number at most one is a star plus isolated vertices, and deleting its centre
contradicts the deletion property.

In P5, both the proportional-pair anchor and the three-term progression anchor
use actual positions outside \(R\), and realize sums \(a,2a,3a\) with at most
1, 2, and 3 positions.  Every projected label in \(R\) is nonzero.  A projected
zero-sum of size at most ten can have actual sum only \(a\); each other residue
is cancelled by a disjoint anchor within the forbidden length 13.  P3 and P4
then yield projected zero-sum splittings with smaller block sizes 2--7 and
3--7 respectively, so replacement by the external \(a\)-position has the
claimed length and uses no position twice.

## P6--P8: seventeen-position complement geometry

The one-, two-, and three-element complement blocks all have sum \(t\).
Squarefreeness gives \(c\le1\); distinct two-blocks are disjoint; five such
blocks, or four together with the singleton \(t\), give a forbidden short
zero-sum.  The other intersection statements in P6 follow directly from
distinct labels, absence of zero, and P5.

For P7, if \(x\notin U\), then \(Q\setminus\{x\}\) is fully zero-sumfree: any
14--16 zero-sum there would have a complement block containing \(x\), contrary
to \(x\notin U\), while shorter zero-sums are excluded globally.  If
\(x-t\) were absent, adjoining it would be a squarefree minimal 17-term
zero-sum, contradicting \(SD(C_5^4)=16\).  Conversely, an element of a
complement block cannot have a predecessor, by the one-, two-, and three-term
arguments printed in the proof.  Thus heads are exactly \(Q\setminus U\).
No position is both a head and a tail because that would give a three-term
progression.  The edges are therefore a matching, \(e=17-|U|\le8\), with all
tails in \(U\).

An independent integer enumeration using only \(c\in\{0,1\}\),
\(0\le b\le4-c\), and \(1+a-b+c=0\pmod5\) confirms that the complete list
violating either inequality (10) is exactly the seven triples in (11).
The five easy cases have the stated union/tail-count contradictions.

The two delicate exclusions also close:

- In \((4,0,0)\), a two-tail block must meet every block having a tail.
  Connectedness yields \(r\ge h-1\), while \(e=5+r\le2h\).  The unique
  possibility is \(r=3,e=8,h=4\).  Every block then has two tails, so every
  pair of blocks meets once.  The two incidence equalities force one common
  point \(w\) and eight private points; equality of tail incidences makes the
  private points precisely the tails.  Summing the four blocks and then all 17
  points gives \(t=t+3w\), hence \(w=0\), a valid contradiction.
- In \((4,1,1)\), every two-tail triple attaches to one endpoint of the
  two-block.  The proof's two constructions exclude two such triples both for
  equal and distinct endpoints, with all positions distinct because heads lie
  outside \(U\) and the head-tail graph is a matching.  With at most one
  two-tail triple, pairwise intersection of all tail-bearing triples gives
  \(r\ge h-1\) when \(k=0\), and connectivity after adjoining the two-block
  gives \(r\ge h\) when \(k=1\).  Together with \(r=e-2\) and
  \(e\le h+k\), both cases are impossible.

Consequently both inequalities (10) are proved without an unmentioned
linearity or unique-incidence assumption.

## P9--P10: lower bound and affine support

The linear combination of (10) is
\(3a+8b-c\ge23\).  Summation over the 18 one-point deletions gives
\(12A+24B-2C\ge414\), hence \(6(A+2B)-C\ge207\).  Since \(C\ge0\) and the
18-layer deletion equations give \(A+2B=2\pmod5\), the least possible integer
is 37.  Summing over all \(\binom{21}{18}=1330\) sets counts a 14-zero-sum 35
times and a 15-zero-sum 20 times, producing

\[
7Z_{14}(S)+8Z_{15}(S)\ge9842.
\]

If a nonzero functional is constant zero on \(S\), the 11-point linear
hyperplane bound is violated.  If it is a nonzero constant, only lengths
divisible by five can be zero-sums, so a 17-set has \(a=c=0\); P6 then forces
\(b=1\), the already excluded triple \((0,1,0)\).  Thus the profile constraints
\(n_0\le11\) and \(\max n_j\le20\) are justified.

## P11: projective-functional identities

The checker explicitly constructed all normalized nonzero linear functionals
on \(\mathbb F_5^4\).  It found 156 projective classes.  Every one of the 624
nonzero vectors is annihilated by exactly 31 classes.  All 193,440 unordered
pairs of linearly independent nonzero vectors were checked and have exactly
six common annihilators.  The zero vector has 156 annihilators.

These constants give every identity in (14) by double counting.  Distinct
labels justify the \(E\) identity; P5's absence of proportional pairs justifies
the \(J\) identity; \(s\ne0\) justifies the \(T\) identity; and absence of an
actual three-term progression makes the displacement vector in every
\(\operatorname{ap}\) configuration nonzero.  Equation (15) has the same
31-versus-156 split for each labelled coefficient assignment.  Nonzero scalar
rescaling of the representative functional preserves every zero condition, so
passing to projective classes loses no information.

## P12: independent reconstruction of the integer certificate

`projection_recheck.py` is a standard-library implementation written from the
displayed definitions.  It expands \(z_k\) by residue-group binomial dynamic
programming, computes \(E,J,T,\operatorname{ap}\) directly, and computes each
\(R_{\mathbf c}\) as an exact labelled coefficient-allocation count.  It does
not read a candidate feature table or executable.

The completed run recorded in `projection_recheck.json` obtained:

- all 11,931 raw profiles checked, with layer counts
  \(2020,1771,1540,1330,1140,969,816,680,560,455,364,286\);
- all 18 \(R_{\mathbf c}\) values recomputed on every profile, for 214,758 exact
  \(R\)-evaluations;
- 2,997 nonzero-scalar profile orbits, matching the auxiliary denominator;
- no profile with \(P(n)>0\); the exact maximum is zero, attained on the four
  scalar images of \((0,0,0,8,13)\);
- \(K=-978253109306\);
- \(125Y_{14}=700000000\), \(125Y_{15}=800000000\), and \(Y_{16}=0\);
- independent ASCII row encoding SHA-256
  `54905033df70ce794fc0bf80727d730b9fedb21eca8d5c090f3f45ce492e5d97`.

The final inequality direction is correct.  Since every \(\beta_j\ge0\) and
every \(W_{\mathbf c_j}(S)\ge0\),

\[
0\ge K+D(7Z_{14}+8Z_{15})+125\sum_j\beta_jW_{\mathbf c_j}(S)
\]

implies \(K+D(7Z_{14}+8Z_{15})\le0\).  With \(D=10^8\), this yields the real
upper bound 9782.53109306 and therefore the integer upper bound 9782.  It
contradicts the independently derived lower bound 9842.

## Reproducibility and input sufficiency

The proof text contains all numerical and mathematical inputs needed to
reconstruct the 11,931-row certificate and the 18 coefficient-assignment
features.  The chat attachment placeholders and the claimed pre-existing zip
archive are therefore not required for this audit.  No missing input blocks
verification of the theorem.

Artifacts produced by this review:

- `fresh_audit/projection_recheck.py`
- `fresh_audit/projection_recheck.json`

SHA-256 values at review time:

- checker: `e9398f1c679ca87e16bba33aa3c85e1f151cf2ff7ade11e87d7c12e5ab8b0eb0`
- result JSON after repository LF normalization: `904948836d94e2f5ef10bf14ca2be98b2321c03f7b5554c86a4ae3fb601530cf`
