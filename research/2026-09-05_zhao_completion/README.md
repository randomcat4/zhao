# Zhao endpoint completion intake — 2026-09-05

This directory records the rescued B manuscript, the four first-round PRO outputs, the second-round prompts, and the completed second-round double-only proof with a separate verification package. It is an audit archive, not a declaration that the full endpoint problem has been solved.

## Current status

| target | intake status | present audit conclusion |
|---|---|---|
| B: every 20-position sequence in \(\mathbb F_5^4\) has a nonempty zero-sum of length at most 14 | rescue manuscript reports a complete proof | candidate-closed, conditional on the explicitly listed certified repository inputs; no critical hand-proof gap found in the present line audit |
| A, at least one value of multiplicity 3 | round-1 route 3 reports `PROVED` | the self-contained three-anchor proof passes the present line audit; still retained as a candidate theorem until a genuinely separate verifier checks it |
| A, squarefree | round-1 route 1 reports `INCOMPLETE` | open; the 15-block 5-regular complement-fibre branch and all larger block-count branches remain |
| A, only double and single values, \(1\le b\le6\) | round-2 prompt 3 reports `PROVED_AND_AUDITED` | a new two-anchor hand proof closes all six frozen cells; a separate second-pass report and independently written finite-interface checker found no gap and replay successfully |
| A, two triple values | round-1 route 4 reports `INCOMPLETE` | its dedicated computation is incomplete, but this whole regime is subsumed if the stronger three-anchor proof from route 3 is certified |

The double-only theorem does not depend on the rescued B proof, the earlier stabilizer lemma, or an exhaustive sequence classification. It uses positional group-ring congruences, a two-anchor quotient argument, and a complete five-branch incidence analysis for the 15-position case.

Consequently, from the point of view of multiplicity cells:

> the cells \(a=0,\ b=1,\ldots,6\) are closed by the new two-anchor proof; if the archived three-anchor proof also survives genuinely separate review, the only remaining A cell is the 21-element squarefree case \((a,b)=(0,0)\).

The full A endpoint is still open in this archive because the squarefree cell is not closed.

## Verification levels

The repository uses the following levels for this intake:

1. **raw** — a thread output is preserved exactly, with its own terminal label;
2. **locally audited** — the argument has been checked line by line in this intake;
3. **replayed** — all claimed finite certificates have been regenerated in a clean environment;
4. **independently certified** — a genuinely separate verifier has checked both reductions and evidence.

The B manuscript and three-anchor proof currently reach level 2, not levels 3 or 4. The rescue bundle's smoke replay could not be rerun on the original host because no GNU C++ compiler was installed; this was recorded as not replayed, not as a pass.

The double-only package reaches level 3 and includes a second-pass re-derivation plus a checker written independently of the submitted checkers. Because the two passes were produced within the same research exchange, the archive records this accurately as a separate verification package rather than external institutional or proof-assistant certification.

## What the first-round PRO runs actually accomplished

### Route 1 — squarefree

It derived useful deletion congruences, lower bounds on 14/15/16/17-zero-sum counts, structure in the 15-block case, and explicit examples showing that several tempting intermediate claims are false. It stopped at a genuine branch rather than closing the target. In particular, proving a statement only for a selected 15-block subfamily would still not settle larger block counts.

### Route 2 — double-only

It proved a one-dimensional stabilizer lemma for \(\Sigma_2(S)\) and isolated the \(b=1\) obstruction. It did not exclude any complete value of \(b\). The failure to upgrade an inclusion to the equality available in B was a method breakpoint, not an endpoint for the assigned theorem.

### Route 3 — at least one triple

It supplied a short self-contained proof. The load-bearing pieces were rechecked:

- the group-ring deletion count proving \(s_{\le 11}(\mathbb F_5^3)\le14\) and \(s_{\le15}(\mathbb F_5^4)\le18\);
- the graph proof that 15 nonzero positions in \(\mathbb F_5^3\) contain a 3-to-11-position zero-sum;
- the quotient by \(\langle a\rangle\), with all three anchor positions kept distinct;
- the split of a 14- or 15-position zero-sum into a block \(U\) of size at most 7;
- replacement of \(U\) by one external anchor, producing a nonempty zero-sum of length at most 13.

No illegal translation, fourth copy of the anchor, or collapse of equal-valued positions was found in that line audit.

### Route 4 — two triples

It completed only roots whose candidate pool had size at most 40. It certified 622 roots for \(b=0\) and 1,583 roots for \(b=1\), while leaving 7,246 and 18,643 frontier roots respectively: 25,889 roots in total. The cutoff 40 was explicitly human-chosen. It is not a theorem and not a complexity barrier.

## Round 2 — double-only six-type closure

The second-round result is archived under `pro_round2/03_double_only/`. Its proof begins with any doubled value \(a\), reserves the two positional copies, eliminates every other point on \(\langle a\rangle\), and obtains a 14- or 15-position zero-sum outside the anchors from an 18-position height-two lemma. The quotient by \(\langle a\rangle\) then yields:

- a complete contradiction in the 14-position branch from a star-shaped pair graph and a group-ring congruence;
- a complete 15-position analysis indexed by the pair count \(e=0,1,2,3,4\), using positional triple degrees, deletion congruences, codegree at most two, and intersecting-family counts.

The proof is uniform in \(b\), so the denominator is exactly six multiplicity cells and all six are closed. The scripts do not enumerate all sequences; they verify the finite arithmetic, signs, complement lengths, and positional incidences used by the hand proof.

## Observed stopping pattern to reject in future rounds

The first-round PRO runs tended to stop when one of the following occurred:

1. a valid lemma or reduction was obtained, even though the frozen theorem remained open;
2. the next branch required a different method than the one already developed;
3. a convenient computation threshold was reached, notably candidate-pool size 40;
4. a relaxation remained feasible, which only falsified that relaxation as a proof method;
5. an equality used in B could not be transferred to A, so the run reported the interface instead of switching approaches;
6. the run could name a “first/minimum unclosed case,” treating localization of the obstacle as a deliverable.

Future work must continue to treat all six as intermediate checkpoints, not terminal states.

## Contents

- `rescue/B_proof_A_progress.md`: rescued proof manuscript, preserved with provenance and caveats.
- `rescue/bundle/zhao_result/`: source, logs, and replay entrypoint from the rescued archive.
- `pro_round1/`: exact final responses from the four first-round PRO tasks.
- `pro_round2_prompts.md`: four second-round prompts with explicit anti-stopping terminal contracts.
- `pro_round2/03_double_only/`: the two-anchor proof, decompressed submitted package contents, recorded ZIP hashes, separate verification report, independent checker, outputs, and manifests.
- `SOURCE_SHA256SUMS.txt`: hashes of the intake files.

## Non-claims

- The full A endpoint is not proved by this intake; the squarefree 21-element cell remains open.
- The archived three-anchor proof has not been promoted to external independent certification.
- A threshold-limited enumeration is not a finite classification.
- A self-reported terminal label is not accepted without examining its proof and evidence.
- A missing compiler is not evidence for or against a mathematical claim.
- “No counterexample found” is never promoted to “proved.”
