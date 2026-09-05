# Atom-route completion and verification ledger

Overall endpoint status: **INCOMPLETE** for both A (21 positions, cutoff 13) and B (20 positions, cutoff 14). No endpoint counterexample is claimed. No searches remain running at this handoff.

The detailed mathematical normalization, recurrence, scope, and remaining patterns are in `../proofs/atom_structure.md`.

## Completed finite exclusions

| Object | Exhaustive denominator / node count | Conclusion | Independent implementation status |
|---|---|---|---|
| Five tripled elements | 5 normalized cores, separately at both cutoffs | All safe extensions stop by length 17 | Original Python only; fresh audit still required |
| Four independent tripled elements | 34 first roots; 656175 nodes | With all new multiplicities <=2, maximum length 18 at cutoff 13 | All root, level, leaf, and maximum counts identical in separately written C# |
| Three independent tripled elements plus an outside doubled element | 113 first roots; 20707001 nodes in complete accepted records | With exactly these three tripled elements, maximum length 18 at cutoff 13 | Mixed Python/C# completed tree; C# calibrated by the full four-triple comparison, but no second implementation has redone all 113 roots |
| Core (3,3,2,2), new distinct double blocks, cutoff 14 | 122 roots; 22461 nodes | Maximum length 16 | Separate NumPy/gather program reproduces every root and count |
| Core (3,3,2,2), new distinct double blocks, cutoff 13 | 122 roots; 24267 nodes | Maximum length 16 | Separate NumPy/gather program reproduces every root and count |
| Core (2,2,2,2), new distinct double blocks, cutoff 14 | 44 roots; 183444 nodes | Maximum length 16 | Separate NumPy/gather program reproduces every root and count |
| Core (2,2,2,2), new distinct double blocks, cutoff 13 | 44 roots; 185077 nodes | Maximum length 16 | Separate NumPy/gather program reproduces every root and count |

Evidence paths: `atom_five_triples.json`, `atom_four_independent_A.json`, `atom_four_fast_crosscheck.jsonl`, `atom_fast_crosscheck_summary.json`, `atom_three_double_final.json`, `atom_b_support9_blocks.jsonl`, `atom_3322_m13_blocks.jsonl`, `atom_2222_m14_blocks.jsonl`, `atom_2222_m13_blocks.jsonl`, and `atom_double_blocks_crosscheck.json`.

The double-block consequences concern **any selected copies** in a larger sequence. In particular, two copies may be selected from a tripled element. The later complete leaf certificates strengthen the endpoint bound to **at most seven support elements of multiplicity at least two**, uniformly.

## Complete leaf certificates, with no general suffix search

* All 428 length-seventeen (3,2,2,2) leaves have full coverage and maximum shortest-subsequence distance at most ten. Thus no one admits any additional position while avoiding zero sums of length <=13. This excludes their embedding in endpoint sequences but preserves the standalone seventeen-position certificate. Maximum-distance histogram: 8:141, 9:189, 10:98.
* All 10196 length-sixteen (2,2,2,2) leaves have full coverage. Safe next-value counts are zero at 2153 leaves and one at 8043 leaves. Any endpoint containing such a core would need at least four further positions, each equal to the unique safe value if it exists. The height bound <=3 rules this out. Therefore both bad endpoints have a+b<=7.
* All 15684 length-sixteen (3,3,2,2) leaves were scanned; their safe-next-value counts range from zero through six: 0:977, 1:3970, 2:3012, 3:801, 4:6316, 5:604, 6:4. Twelve leaves have coverage 623, all others 625. This histogram alone does not close the two-tripled/five-doubled case; the exact finite check below does. No general suffix tree was run.

Full per-leaf records: `atom_3222_leaf_profiles.jsonl`, `atom_2222_leaf_profiles.jsonl`, `atom_3322_leaf_profiles.jsonl`. All leaf denominators match the preserved complete source trees root by root. Separate NumPy reconstruction checks the saved distance histograms and every safe next value: `atom_3222_leaf_profiles_check.json`, `atom_2222_leaf_profiles_check.json`, `atom_3322_leaf_profiles_check.json`. Original scripts and source outputs were not altered for these callbacks.

## Completed micro-combination exclusion with explicit witnesses

For the (3,3,2,2) length-sixteen leaves, after excluding the core support, safe-list sizes have distribution 0:3380, 1:3110, 2:1894, 3:863, 4:5879, 5:554, 6:4. Only 6437 leaves can supply four distinct new values; there are exactly 8709 four-subsets. Every one has an explicit zero-sum position subsequence of length <=13 stored in `atom_3322_outside_micro.json`. The plain-integer checker `atom_3322_outside_micro_check.json` verifies all witnesses and exact coverage of the 8709 combinations, without DP or a search.

This proves the standalone finite-pattern theorem (3^2,2^5,1^4) of length twenty always has a <=13 zero sum. It eliminates B's (a,b,c)=(2,5,4) and A's (2,5,5). Under the separate a<=3 dependency, it gives a>=2 implies a+b<=6. No other unlisted suffix class is claimed exhausted.

## Completed finite objects which are not endpoint exclusions

* All zero-sum-free extensions of e1^3 e2^3 e3^3 in H through length twelve: level counts 1,58,738,891. The 891 twelve-position cores have unique distance-12 point, no distance-11 point, at most one distance-10 point, at most five points of distance >=9, and at most two of distance >=10. Full lists/profiles: `atom_three_hyperplane.json`. This is original Python evidence; the root agent's separate outside quotient proofs carry any endpoint application.
* All eleven-position H cores: 738 raw extensions, 131 S3 orbits. Full distance tables in `atom_h11_core_profiles.json`; the earlier input `atom_h11_cores.json` was preserved unchanged. Minimum coverage 100; maximum unreachable 25; maxima of distance >=8,9,10,11,12 are 33,29,27,26,25, counting infinity. The later preprocessor adds these profiles without changing its raw or canonical core lists.
* One-tripled/seven-doubled candidate (core 3,2,2,2): 106 roots, 121866 nodes, 428 length-seventeen terminal branches. Full tree `atom_3222_m13_blocks.jsonl`; all roots and terminal counts independently reproduced in `atom_3222_crosscheck.json`. One explicit survivor is separately certified through every bounded coefficient tuple in `atom_3222_length17_certificate.json`. Its minimum zero-sum length is 15, and Z15=6. It has only 17 positions and is not an endpoint counterexample.
* One length-eighteen leaf of the four-independent-triples computation was independently checked through every nonempty position subset: `atom_four_longest18_graycheck.json`. This check validates that leaf, not the full search tree.

## Incomplete bounded search

`atom_h11_probe.jsonl`: fixed e4 outside a normalized eleven-position H core, all other outside elements distinct, cutoff 13. Of 131 core representatives, 13 are complete. Core id `38,108` was interrupted by the 45-second global deadline after 21504 nodes. The other 117 cores were not attempted in this probe. Total nodes 13116309; longest observed length 17. This is not a full H=11 exclusion. No H=9 or H=10 outside search was run by this route.

Earlier 332 checkpoints are superseded by the full `atom_three_double_final.json`; their truncations must not be counted as unfinished final branches. Conversely, the H11 probe has no superseding full record and must remain incomplete.

The existing (3,2,2,2) tree's 107656 length-fifteen nodes were additionally scanned for safe single values outside the core support, with every root matched to the original tree: `atom_3222_len15_scan.jsonl`. All profiles and safe lists were independently rebuilt in NumPy, and the exact denominator was recomputed: `atom_3222_len15_scan_check.json` (10.13 seconds). The scan itself is complete, but it does not close any suffix class. The largest outside-safe list has size 127 at nine nodes; the other lists have size at most twenty. Their exact five-subset denominator is 2336039691, so no five-subset enumeration was started. This is the current quantified breakpoint for the (a,b,c)=(1,6,5) length-twenty pattern. The original block tree and all earlier certificates remain preserved.

## Explicit mathematical dependencies

* The line/plane reductions use the published Zhao-Hong Lemma 2.3 constants read from the original publication. The thesis link was not successfully retrieved; it is not silently treated as an independently inspected source.
* The five-triple exclusion supplies the capacity bound used for four independent triples.
* The 332 exclusion is conditional on exactly three tripled elements. Its proof does not itself require the rank-three four-triple exclusion, but using it as part of an a<=3 classification does.
* Excluding four tripled elements of rank three is the root agent's separate proof. This route did not silently claim to prove it.
* The H=12 outside exclusions are the root agent's separate quotient arguments, applied to the 891-core distance assertions. They are a separate audit dependency.
* No result here is asserted for arbitrary p>=5 or as an exact value of K(C_5^4).

## Exact unresolved scope

With the separate four-triple exclusion accepted, remaining (a,b,c) patterns have a=0,b<=7; a=1,b<=6; a=2,b<=4; or a=3,b<=1, with c=N-3a-2b. None of the first three families has been exhausted. For a=3, all doubled elements lie in the triple span H; after a separately verified H=12 exclusion, the remaining intersections are H=9 (no doubles, no further H singles), H=10 (no doubles, one H single), or H=11 (either no doubles and two H singles, or one double and no further H singles). All outside terms are distinct.

The resulting support lower bounds are A>=13 and B>=12, conditional on the stated separate proof dependencies. These are reductions, not solutions of the endpoint claims.
