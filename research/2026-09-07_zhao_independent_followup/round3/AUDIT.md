# Zhao general-prime endpoints: third independent audit

This note tests the first nonlinear constraints omitted by the second-round relaxations. It is not an endpoint proof and the explicit models are not counterexamples.

## 1. Two notions of order

- **Link/moment order `t`**: data `d(E)` are known for position sets `|E|<=t`; the level-one Gram matrix uses links through size two, and the level-two matrix uses links through size four.
- **Exchange radius `r`**: two equal-sum blocks differ by deleting and inserting `r` positions. A one-exchange forces equality of the exchanged labels; a two-exchange forces equality of the two pair sums.

These orders are not the same. For a `(p-1)`-block, a two-exchange is exposed by a link of size `p-3`.

## 2. A_7: the supplied degree/codegree table fails at pair order

In the length-22 layer, use zero-based positions `2,7,19` (one-based `3,8,20`). Their degrees and codegrees are

```
d_2=d_7=d_19=554,
d_{2,7}=0,
d_{2,19}=d_{7,19}=554.
```

For any genuine block family,

```
sum_B (1_{2 in B}+1_{7 in B}-1_{19 in B})^2 >= 0.
```

The supplied marginals give

```
554+554+554+2*0-2*554-2*554 = -554.
```

Equivalently, the principal Gram matrix

```
554 * [[1,0,1],[0,1,1],[1,1,1]]
```

has determinant `-554^3=-170031464`. Thus the table is not the degree/codegree table of any family, even before imposing common group labels or zero sums.

The same contradiction can be read without PSD: every block containing position 19 would have to contain both 2 and 7, yet the codegree of 2 and 7 is zero.

## 3. The all-prime A multihypergraph passes PSD but fails one-exchange fixed-sum gluing

The symmetric all-prime construction is an actual positive multihypergraph, so every positional Gram matrix and every Möbius nonnegativity inequality holds at every order. However all multiplicities in all four layers are positive for every prime `p>=7`; hence the support contains every block of the relevant size.

Take two positions `u,v` and a common `(k-1)`-set `E`. Both `E+u` and `E+v` are declared zero-sum blocks. Their difference forces `g_u=g_v`. Thus all position labels are equal. Since `k=3p+j`, `1<=j<=4<p`, zero block sum gives `j g=0`, hence `g=0`, contradicting the no-singleton-zero condition.

So this concrete model first fails the **one-exchange common-label condition**, not PSD. Pure simplicity is only seen when the full atomic complement weight is recovered; the smallest complement size is `p-4` (three when `p=7`).

## 4. B: the old complete incidence model is killed by one-exchange, and the new maximal-support result confirms this

For the old model consisting of all `(p-1)`-subsets of a fixed `X` of size `2p-2`, every positional Gram/Möbius condition holds because it is a genuine simple family. If all blocks have the same group sum, then for arbitrary `u,v in X` choose `E subset X\{u,v}` of size `p-2`. The two blocks `E+u,E+v` force `g_u=g_v`. Hence all `2p-2` positions of `X` have one value.

This violates `h(S)<=p-2`. Under the additional maximal-support theorem supplied for this audit, it also gives maximum complement support one, neither squarefree nor a unique-double profile. Thus the new theorem kills this old model, but does not add a new obstruction beyond one-exchange closure.

## 5. A simple all-order local Möbius model around a maximal B complement

Let `R` have `k=p-1` positions. For `0<=r<=p-1`, define exact-distance multiplicities

```
w_0=1, w_1=0,
w_r=r-1              for odd r>=3,
w_r=p-r+1            for even r>=2.
```

Equivalently,

```
w_r = (-1)^(r+1)(r-1) mod p
```

with the least nonnegative representative.

Take an outside set `O` of `4p-4` positions. For every `J subset R`, `|J|=r`, choose `w_r` distinct `r`-subsets of `O` and form blocks

```
(R\J) union A.
```

This is a simple `(p-1)`-uniform family. For `I subset R`, `|I|=r`, the number of blocks containing `R\I` is

```
d_r = sum_{q=0}^r binom(r,q) w_q.
```

Hence `d_0=d_1=1` and `d_r=0 mod p` for every `r>=2`, by the two binomial identities for `(1-1)^r` and its derivative. All exact Möbius counts are the nonnegative `w_r`, so all local Gram matrices are PSD.

At the first high link, indexed by missing pairs, `d_2=p` and all off-diagonal intersections are one. The Gram matrix is

```
(p-1) I + J,
```

with positive eigenvalues. Thus Gram/PSD and even all-order local Möbius consistency do not eliminate either the squarefree or unique-double maximal-support profile.

The first label-sensitive condition is `r=2`: every pair `J subset R` must have `p-1` additional outside pair replacements of exactly the same group sum. In original link language this is the `|E|=p-3` condition.

## 6. The maximal-support theorem does not kill the local fibre models

Two common-label examples survive all previously derived local length-functional constraints:

- **Squarefree:** `R={(1,t,t^2,t^3): t in F_p^*}`.
- **Unique double:** two copies of `(1,0,0,0)` together with `p-3` distinct points `(1,t,t^2,t^3)`.

Every nonempty subset of either sequence has first coordinate equal to its cardinality in `{1,...,p-1}`, hence is nonzero. Equal subset sums have equal lengths. Taking `ell=lambda` equal to the first coordinate and `Q=3 ell^2` gives the same zeroth/first/second fibre jets as in the second audit. Therefore the maximal-support classification alone does not remove those local relaxations.

## 7. The squarefree moment-curve model first meets a genuine obstruction at the pair-completion link

The moment curve is Sidon for unordered pairs. If

```
g_a+g_b=g_c+g_d,
```

then the second and third coordinates give equal sums and equal sums of squares, hence equal products; therefore `{a,b}={c,d}`.

For each of the `binom(p-1,2)` distinct pair sums, the `p-3` link congruence and the presence of `R` force at least `p` pair representations in the full sequence. A position pair has only one sum, so

```
p * binom(p-1,2) <= binom(5p-5,2).
```

This is equivalent to

```
p^2-27p+30 <= 0.
```

It fails for every prime `p>=29`. Thus the squarefree moment-curve local model has no global two-length extension for `p>=29`; the certificate uses only the pair-completion link and total pair capacity.

For `p=7,11,13,17,19,23`, this count does not decide feasibility.

## 8. A p=7 common-label pair-completion model, and its exact first failures

Let

```
R={(1,t,t^2,t^3): t=1,...,6} subset F_7^4,
sigma(R)=(6,0,0,0),
h=(2,0,0,0).
```

Take the 30-position sequence

```
S = R union (R+h) union 3 copies of (R-h).
```

Then `sigma(S)=sigma(R)`, the height is three, and `R` is squarefree. In the complete six-subset fibre of sum `sigma(S)`, every link `R\{i,j}` has degree exactly seven. Thus the common-label two-exchange/pair-completion condition is genuinely realizable at `p=7`.

It is not a B_7 model. The complete fixed-sum fibre has 1441 blocks, which is `6 mod 7`, not zero. More directly, choose any three base points and the `R-h` copies of the complementary three points. Their sum is

```
sigma(R)-3h = 7 sigma(R)=0.
```

For the pinned indexing in the JSON, positions `1,2,3,16,17,18` form an explicit six-position zero sum. Hence pair completion does not imply the two-length spectrum; the next missing condition is global compatibility of all fixed-sum fibres with the no-short-zero-sum condition and with deletion congruences away from the chosen block.

## 9. Final order assessment

| model | Gram/Möbius status | first detected failure |
|---|---|---|
| A_7 supplied degree/codegree table | fails | pair-link / degree-2 Gram |
| all-prime A multihypergraph | passes at every positional order | one-exchange common-label gluing; simplicity only at atomic complement order `p-4` |
| old B complete-subset design | passes at every positional order | one-exchange common-sum closure |
| B maximal-support local Möbius model | passes at every local order | first nontrivial label test is two-exchange, i.e. a `p-3` link |
| B squarefree moment curve | local jets pass | pair-capacity contradiction at that link for `p>=29`; undecided by this test for `p<=23` |
| B_7 translate model | pair completion passes | global fibre count and an explicit six-position zero sum |

There is therefore no short universal PSD certificate for the remaining B branch. The needed new theorem must control the global overlap of the pair-completion fibres (and then the higher replacement fibres) under the no-short-zero-sum condition. For A, the particular p=7 pair table is already dead, but the all-prime positive multimeasure shows that positional PSD alone cannot close the `x_0=0` chamber; common-label exchange or full atomic Boolean realization must be used.
