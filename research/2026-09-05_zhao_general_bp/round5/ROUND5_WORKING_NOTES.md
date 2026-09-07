# Round 5 working notes: near-squarefree complements in the `{3p,4p-4}` branch

Date: 2026-09-07

**Status: WORKING PROOF NOTES — NOT YET INDEPENDENTLY AUDITED.**

This file archives the useful structural reductions obtained after Round 4. It is deliberately **not** an update to `THREAD_STATUS.md`, and it must not be cited as closing general `B_p` or the whole two-length branch until independently checked.

## 0. Fixed branch and notation

Let `p>=7` be prime, `G=F_p^4`, `|S|=5p-5`, and assume there is no nonempty zero sum of length at most `3p-1`. In this file we additionally remain inside the conditional two-length branch

```text
all nonempty zero sums have length in {3p,4p-4},
Z_{4p-4}(S)>0.
```

Fix an `L=4p-4` atom `T` and its complement `R=S\T`, so `|R|=p-1`. The previously archived inputs are used only in the forms already proved in Rounds 3–4:

- `h(S)<=p-2`;
- every `2,...,p-1` positional subsum of `R` avoids `supp(S)`;
- equal sums of subsets of `R` have equal cardinality;
- there is a linear length functional `ell_R:<R>->F_p`, equal to `1` on every external position value;
- `lambda_T(g)=2 nu_T(g)+1` on external values;
- the `(p-3)`-deletion design congruence holds for `L`-atom complements;
- at least one `L`-atom complement has rank at least `3`.

Throughout this note, complements are chosen with **maximum support**, and among those with **maximum rank** whenever an exchange argument needs that refinement.

## 1. Exact two-value fibre congruence

For `B subseteq R`, write

```text
b=|B|,
t=sigma(B),
M_B=sum_{i in B} nu_T(g_i).
```

Let

```text
a_B = #{A subseteq T : |A|=b, sigma(A)=t},
c_B = #{A subseteq T : |A|=b+p-4, sigma(A)=t}.
```

Inside the two-length branch, the actual `T`-fibre over `t` can occur only in those two lengths. The first two fibre moments give the congruences

```text
a_B == (-1)^b (1-b-M_B)       (mod p),
c_B == (-1)^(b+1) (1+b+M_B)   (mod p).
```

For two distinct external values `g,h` this specializes to

```text
a_{g,h} == -(1+m_g+m_h) (mod p),
```

where `m_x=nu_T(x)`. The number of *nontrivial* internal two-position representations of `g+h`, after removing the `m_g m_h` representations using one internal `g` and one internal `h`, is therefore

```text
a_{g,h}-m_g m_h == -(m_g+1)(m_h+1) (mod p).
```

Hence, for a squarefree external complement (`r_g=r_h=1`), the external multiplicity bound gives `m_g,m_h<=p-3`, so every pair of distinct external values has at least one nontrivial `T`-internal two-position representation of the same sum.

## 2. Cross-atom lambda-difference lemma and its scope

Let `R,R'` be two `L`-atom complements, with atoms `T,T'`. On the span of positions that remain external on both sides,

```text
Delta = (lambda_T-lambda_T')/2
```

satisfies

```text
Delta(x)=nu_{R'}(x)-nu_R(x)
```

for every value `x` for which the comparison is legitimate. If **all values whose multiplicities change remain represented in the common external part**, then, writing

```text
d_x=nu_{R'}(x)-nu_R(x),
```

fixed total sum gives `sum_x d_x x=0`, and applying `Delta` yields

```text
sum_x d_x^2 = 0 (mod p).
```

### Important scope correction

This square-sum identity **cannot** be applied blindly to a squarefree exchange

```text
E + {g,h}  <->  E + {a,b}
```

when `g,h` disappear completely on the right and `a,b` were absent on the left. In that situation the changed values are not all common external values, so the formal `1+1+1+1=4` contradiction is invalid.

The identity is reliable for exchanges in which the changed value classes survive in the common external part, and is especially useful for coloop / binary-cocircuit / repeated-value exchanges.

## 3. Maximum-support reduction to two near-squarefree types

The following reduction is the main reusable output of this working round.

Choose `R` with maximum support and rank at least `3` (using the Round-4 rank-expansion result if necessary). Then the intended proof shows:

```text
external multiplicity type of R is either

    1^(p-1)

or

    2 * 1^(p-3).
```

Equivalently, every external value occurs at most twice and at most one value occurs twice.

### 3.1 No value can occur three or more times

Suppose `g` occurs `r_g>=3` times externally. A one-variable deconvolution of the actual-sum fibre along the value `g` gives a two-position internal representation

```text
a+b=2g
```

using no internal `g`. Replace two external copies of `g` by the internal positions `a,b`. Because `r_g-2>=1`, `g` remains external. Maximum support forces `a,b` to lie in existing external value classes. The changed classes therefore remain visible on both sides, so the square-sum lemma applies and yields

```text
1^2+1^2+(-2)^2 = 6 == 0 (mod p),
```

impossible for `p>=7`.

### 3.2 Two distinct double values are impossible

Assume distinct `g,h` both occur twice externally. Remove one copy of each, keeping `g,h` in the common external part. The two-value fibre congruence shows that the number of nontrivial internal representations `a+b=g+h` is nonzero modulo `p`, because

```text
m_g,m_h <= p-5.
```

If such a representation uses only old external value classes, maximum support and the common-position condition make the square-sum lemma applicable; the possible change vectors give square sums `4` or `6`, both nonzero modulo `p`.

If every internal representation were the trivial internal `g+h` representation, then

```text
m_g m_h == -(1+m_g+m_h) (mod p),
```

hence `(m_g+1)(m_h+1)==0 (mod p)`, impossible for `m_g,m_h<=p-5`.

This leaves at most one double external value.

**Audit note:** the above reduction is a working proof and should be checked line-by-line for the exact common-external-position hypothesis before being promoted to the authoritative status file.

## 4. Unique-double-value reflection structure

Assume

```text
R = g^2 A,
|A|=p-3,
```

where `A` is squarefree and `g notin A`. Put

```text
a = nu_S(g)-1.
```

The fixed `2g` fibre decomposes under the reflection

```text
rho(x)=2g-x.
```

Maximum support and the cross-atom square-sum restriction force the non-central reflection structure to have only constantly many components:

- at most a small number of old-new components, whose old endpoints must be coloops of the value matroid of `A`;
- at most one old-old reflection pair.

A useful target congruence for the fixed `2g` core is

```text
C(a+1,2)
 + sum_{y in Y} (n_y-1)n_{2g-y}
 + epsilon (n_u-1)(n_v-1)
 == 0 (mod p),
```

where `Y` is the set of old endpoints of old-new reflection components and `epsilon in {0,1}` records the possible unique old-old pair.

The previous working derivation claimed that, in rank `3` and `p>=11`, this can be pushed to a contradiction by showing all low-weight lambda-difference kernels coincide and then reducing to a uniform midpoint / uniform-translation model. That sub-proof is **not promoted here as audited**; preserve it only as a candidate route.

## 5. Squarefree rank-three small-cocircuit route

Assume `R` is squarefree, rank `3`, and contains a coloop or a binary cocircuit. Then all but at most two or three external values lie on an affine line inside `ell_R=1`.

The candidate counting route is:

1. Use `lambda_T(g)=2nu_T(g)+1` to show the internal multiplicity function cannot vary too much along that affine line without exceeding the rank-three zero-sum-free capacity.
2. If the internal multiplicity is positive and constant on almost the entire line, construct a `p`-term zero sum from two copies of an almost-complete affine line.
3. Hence the line contributes no internal copies.
4. The `(p-3)`-link condition then forces every external two-sum on the line to have at least `p-1` internal two-position representations.
5. Summing over all target sums gives a lower bound of order `p(p-1)`, while the number of internal pairs in the relevant affine hyperplane gives a smaller upper bound.

This is a promising closed subcase, but it still needs independent verification before being treated as a theorem.

## 6. Correct global carrier for squarefree all-new exchanges

For squarefree exchanges where both replacement values are genuinely new, the local square-sum lemma does not apply. The correct global object is the exchange graph on all `L`-atom complements: connect two complements when they share `p-3` positions.

For a connected component `F` of this graph, let `X` be the union of all positions occurring in blocks of `F`. Then every `(p-3)`-subset `E of X` has block degree

```text
d_F(E) == 0 (mod p).
```

Indeed, if `E` lies in one block of `F`, every global complement containing `E` is adjacent to that block and hence remains in the same connected component; if `E` lies in none, the degree is zero.

A Boolean-polynomial argument then gives the useful ground-set lower bound

```text
|X| >= 2p-2.
```

The borderline case `|X|=2p-3` would force all `p` subblocks of a `p`-set to be complements of the same fixed sum, hence all `p` positions equal, contradicting the short-zero-sum hypothesis.

This exchange-component design is the appropriate carrier for future additive-energy / collision counting in the squarefree rank-3-no-small-cocircuit and rank-4 cases.

## 7. Label-sensitive `(p-3)`-link constraint for two-sums

A key next-step constraint, highlighted by the independent audit, should be treated positionally, not merely by value support:

> For each external two-position subset `{i,j} subset R`, the core `E=R\{i,j}` has size `p-3`. The number of `L`-atom complements containing `E` is divisible by `p`.

Since the original complement `R` is one such block, the fixed sum `g_i+g_j` must admit enough positional two-position completions to make the total number of complement blocks a positive multiple of `p`.

This must be applied with exact positional multiplicities. It is stronger than the statement “there exists another representation of the same two-sum”, and it is the preferred input for the next energy/capacity round.

## 8. Retracted / forbidden deductions

The following deductions were explored and must **not** be reused:

1. **False single-family covering claim.** From a `(p-3)`-deletion congruence one cannot conclude that every `(b-1)`-subset is covered by the long-representation family attached to one fixed `B`. A surviving `3p` complement may correspond to a proper subset `C subsetneq B`.

2. Therefore the proposed exponential bounds

```text
Z_{3p} >= p 2^(p-3)+1,
Z_{4p-4} >= p 2^(p-3)
```

are **retracted**. The archived universal bound that remains available is `Z_{3p}>=8p+1`.

3. **False unrestricted square-sum exchange.** Do not apply `sum d_x^2=0` when changed value classes disappear on one side of the exchange and appear only on the other.

## 9. Remaining targets

After retaining only reductions that survive the caveats above, the intended near-squarefree targets are:

```text
(A) squarefree rank 3 with no coloop or binary cocircuit;
(B) squarefree rank 4;
(C) unique-double-value rank 4;
(D) p=7 exceptional small-prime configurations.
```

The desired next method is a label-sensitive additive-energy / capacity double count over **all external two-position sums**, using:

- `(p-3)`-link divisibility;
- fixed complement sum;
- `ell_R=1`;
- `lambda_T(g)=2nu_T(g)+1`;
- maximum-support / maximum-rank exchange restrictions;
- the exchange-component design above.

A proof eliminating these cases would close only the conditional `{3p,4p-4}` branch. It must not be described as proving all of general `B_p` unless all lower non-pure lengths have separately been eliminated.
