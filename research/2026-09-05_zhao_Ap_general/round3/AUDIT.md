# Boundary audit

This is an internal mathematical and computational audit, not independent third-party sign-off.

1. **No inherited height reproof.** The premise h(S) <= p-4 is read from the prior record. The new line-occupancy result is not misreported as h(S) <= p-5.
2. **Core capacity.** The largest core has p positions. The selected short quotient block has at most 2p-2 positions, so their disjoint union has at most L=3p-2. In the one-hole case, all copies of the actual missing-direction value a must be inside the core.
3. **Core quantifier.** The lemma says the core complement is zero-sum free. It says the core is impossible only when its size is at most p-1. A core of size p is not silently ruled out.
4. **All zero sums versus one zero sum.** The degree-six compression applies to all actual zero sums in R before the deletion system is formed. The later 3p-block discussion is explicitly conditional; theta=-1 is not excluded.
5. **Replacement.** A replacement uses all of an added c-copy package only when the new zero sum has more than h anchor positions. The inequalities c<=h+1 and |U|<=c justify the positional mapping and length bound. Trimming preserves the increased height.
6. **General r.** The normal form is stated for a maximum-height counterexample, or as a conditional boundary-height induction interface, and only for p>=2r-1. Its r-3-dimensional kernel is not a completed induction.
7. **Signs.** For an even 4-position small block in a 3p-position zero sum, one deletion contributes 1-2*1_{i in block}. Therefore the final degree is +1/2 mod p. The triple case from the prior round has the opposite sign.
8. **Four-uniform kernel lemma.** The family must contain all k-position subsets with the specified actual sum. The proof uses closure under swapping equal-valued positions. The prime cutoff 131 excludes only the specified three-position double-hit core.
9. **Counterfamily.** The full constant-sum four-block family, not just a chosen subfamily, is checked by the nine-type encoding. Its total is nonzero and its private degrees are 1; it is not an A_p counterexample.
10. **Squarefree projection.** Squarefree alone only removes D_eq. The constructed relaxation witness removes all three corrections and is affine-full, but only guarantees no zero sum up to p-2. It does not satisfy the full A_p counterexample conditions.
11. **Computation.** The standard-library checker was run twice. The JSON reports were byte-identical. It verifies finite interfaces and explicit constructions, not universal vector-sequence enumeration.
12. **Final status.** Neither A_p nor h(S)<=p-5 is claimed. No full parameterized Farkas inequality has been obtained.
