# Zhao general-prime endpoints: second independent audit models

This note records explicit relaxation models used to test whether the currently derived deletion/link/fibre equations are already contradictory. They are **not** group-sequence counterexamples and do not prove either endpoint.

## A: all-prime order-3 link multihypergraph

Let `p>=7`, `|Omega|=4p`, and distinguish `o in Omega`. For `j=1,2,3,4`, put `k_j=3p+j`. In family `H_j`, give every `k_j`-set containing `o` multiplicity `u_j` and every `k_j`-set avoiding `o` multiplicity `v_j`, using the least nonnegative representatives modulo `p` of

```
u = (-3, 9, -9, 3)
v = ( 1, 3,  -5, 2).
```

For `E subset Omega`, let `d_j(E)` be the number of blocks containing `E`, counted with multiplicity. Lucas reduction gives, for `|E|<=3`, the following residues:

| E type | `(d_1,d_2,d_3,d_4) mod p` |
|---|---|
| empty | `(-4,-6,-4,-1)` |
| one point, not `o` | `(1,3,3,1)` |
| one point, `o` | `(-3,-9,-9,-3)` |
| two points, not containing `o` | `(0,3,6,3)` |
| two points, containing `o` | `(0,9,18,9)` |
| three points, not containing `o` | `(0,0,-5,-5)` |
| three points, containing `o` | `(0,0,-9,-9)` |

Hence

```
-d_1(E)+d_2(E)-d_3(E)+d_4(E) = 1  if E is empty,
                                           0  if 1<=|E|<=3            (mod p).
```

The construction also obeys all exact nonnegative link recurrences because it is an actual multihypergraph. Its deliberate failures are: repeated blocks are allowed, and no block is required to have group sum zero under one common label map.

## A: p=7 two-link integer model

The accompanying JSON additionally contains a 28-position model with lengths 22,23,24,25 and counts

```
(703,701,703,706).
```

It supplies nonnegative integral vertex degrees and pair codegrees, below their elementary capacities, together with 28 distinct nonzero labels in `F_7^4`. It satisfies the scalar, one-position, two-position, and vector link equations. It does not supply a 0/1 decomposition into actual zero-sum subsets or higher-link compatibility.

## B: exact incidence designs without fixed-sum gluing

Let `N=5p-5`.

* For complements of `3p` atoms, fix `C` of size `p-4` and take every `(2p-5)`-set containing `C`. If `|E|<=p-3` and `q=|E\C|`, its degree is

  `binom(4p-1-q,p-1-q) = 1 (mod p)`.

* For complements of `L=4p-4` atoms, fix `X` of size `2p-2` and take every `(p-1)`-subset of `X`. For `E subset X`, `|E|=e<=p-3`, its degree is

  `binom(2p-2-e,p-1-e) = 0 (mod p)`;

  it is zero when `E` is not contained in `X`.

Both are simple 0/1 set families. They show the high-order deletion-design congruences are not contradictory by themselves.

The second family cannot be globally labelled with one common block sum while retaining `h<=p-2`: its one-exchange graph is complete on `X`; exchanging `u` and `v` between two blocks forces `g_u=g_v`, hence all `2p-2` positions in `X` have the same value.

## B: formal local fibre jet

Use outside points

`g_t=(1,t,t^2,t^3)`, `t in F_p^*`,

and let `ell` be the first coordinate, `lambda=ell`, `Q=3 ell^2`. A nonempty outside subset of size `b` has first coordinate `b`, so it is zero-sum-free and equal sums have equal lengths. For its sum, assign the least nonnegative residues

```
A_b                 = (-1)^b   (1-b),
A_(b+p-4)           = (-1)^(b+1)(1+b)       (mod p).
```

The signed counts are `c_0=1-b`, `c_1=1+b`, and satisfy the zeroth, first, and second derivative identities

```
c_0+c_1 = 2,
b c_0+(b-4)c_1 = -4-2b,
b(b-1)c_0+(b-4)(b-5)c_1 = 20+10b-6b^2.
```

This is a nonnegative local jet model, not the coefficient table of a product `prod(1-uX^{g_i})` for an actual atom.

## Exact missing semantic condition

The common omitted condition is simultaneous Boolean factorization under one position labelling:

```
A^T_r(z) = #{A subset T: |A|=r and sum(A)=z},
Sum_{r,z} (-1)^r A^T_r(z) u^r X^z = prod_{i in T}(1-uX^{g_i}),
```

with all atom/complement blocks drawn from the same globally labelled sequence and every complement block having the same group sum. The existing scalar/link equations and first two fibre moments are projections (jets) of this condition; the displayed models satisfy those projections while deliberately failing the factorization/gluing.
