# Zhao endpoint completion intake — 2026-09-05

This directory records the rescued B manuscript and the four first-round PRO outputs. It is an audit intake, not a declaration that the full endpoint problem has been solved.

## Current status

| target | intake status | present audit conclusion |
|---|---|---|
| B: every 20-position sequence in \(\mathbb F_5^4\) has a nonempty zero-sum of length at most 14 | rescue manuscript reports a complete proof | candidate-closed, conditional on the explicitly listed certified repository inputs; no critical hand-proof gap found in the present line audit |
| A, at least one value of multiplicity 3 | round-1 route 3 reports `PROVED` | the self-contained three-anchor proof passes the present line audit; still retained as a candidate theorem until an independent verifier checks it |
| A, squarefree | round-1 route 1 reports `INCOMPLETE` | open; the 15-block 5-regular complement-fibre branch and all larger block-count branches remain |
| A, only double and single values | round-1 route 2 reports `INCOMPLETE` | open; no complete \(b\in\{1,\ldots,6\}\) multiplicity class was excluded |
| A, two triple values | round-1 route 4 reports `INCOMPLETE` | its dedicated computation is incomplete, but this whole regime is subsumed if the stronger three-anchor proof from route 3 is certified |

The key compression is therefore:

> If the three-anchor proof survives independent review, every hypothetical A counterexample has height at most two. The only remaining multiplicity cells are \(a=0\), \(b=0,1,\ldots,6\): one squarefree cell and six double-only cells.

This is 8 of the 15 originally dispatched multiplicity cells closed by one proof, leaving 7 cells. That count must not be presented as a percentage of mathematical difficulty; the two remaining structural regimes may contain most of the difficulty.

## Verification levels

The repository uses the following levels for this intake:

1. **raw** — a thread output is preserved exactly, with its own terminal label;
2. **locally audited** — the argument has been checked line by line in this intake;
3. **replayed** — all claimed finite certificates have been regenerated in a clean environment;
4. **independently certified** — a separate verifier has checked both reductions and evidence.

The B manuscript and three-anchor proof currently reach level 2, not levels 3 or 4. The rescue bundle's smoke replay could not be rerun on this host because no GNU C++ compiler is installed. This is an environment limitation, not a mathematical failure, and it is not counted as a pass.

## What the first-round PRO runs actually accomplished

### Route 1 — squarefree

It derived useful deletion congruences, lower bounds on 14/15/16/17-zero-sum counts, structure in the 15-block case, and explicit examples showing that several tempting intermediate claims are false. It stopped at a genuine branch rather than closing the target. In particular, proving a statement only for a selected 15-block subfamily would still not settle larger block counts.

### Route 2 — double-only

It proved a one-dimensional stabilizer lemma for \(\Sigma_2(S)\) and isolated the \(b=1\) obstruction. It did not exclude any complete value of \(b\). The failure to upgrade an inclusion to the equality available in B is a method breakpoint, not an endpoint for the assigned theorem.

### Route 3 — at least one triple

It supplied a short self-contained proof. The load-bearing pieces were rechecked:

- the group-ring deletion count proving \(s_{\le 11}(\mathbb F_5^3)\le14\) and \(s_{\le15}(\mathbb F_5^4)\le18\);
- the graph proof that 15 nonzero positions in \(\mathbb F_5^3\) contain a 3-to-11-position zero-sum;
- the quotient by \(\langle a\rangle\), with all three anchor positions kept distinct;
- the split of a 14- or 15-position zero-sum into a block \(U\) of size at most 7;
- replacement of \(U\) by one external anchor, producing a nonempty zero-sum of length at most 13.

No illegal translation, fourth copy of the anchor, or collapse of equal-valued positions was found.

### Route 4 — two triples

It completed only roots whose candidate pool had size at most 40. It certified 622 roots for \(b=0\) and 1,583 roots for \(b=1\), while leaving 7,246 and 18,643 frontier roots respectively: 25,889 roots in total. The cutoff 40 was explicitly human-chosen. It is not a theorem and not a complexity barrier.

## Observed stopping pattern to reject in the next round

The PRO runs tended to stop when one of the following occurred:

1. a valid lemma or reduction was obtained, even though the frozen theorem remained open;
2. the next branch required a different method than the one already developed;
3. a convenient computation threshold was reached (notably candidate-pool size 40);
4. a relaxation remained feasible, which only falsified that relaxation as a proof method;
5. an equality used in B could not be transferred to A, so the run reported the interface instead of switching approaches;
6. the run could name a “first/minimum unclosed case,” treating localization of the obstacle as a deliverable.

Future prompts must treat all six as intermediate checkpoints. They must require method switching, exact exhaustive continuation, certificate production, and adversarial proof checking before a final answer is accepted.

## Contents

- `rescue/B_proof_A_progress.md`: rescued proof manuscript, preserved with provenance and caveats.
- `rescue/bundle/zhao_result/`: source, logs, and replay entrypoint from the rescued archive.
- `pro_round1/`: exact final responses from the four recent ChatGPT PRO tasks.
- `pro_round2_prompts.md`: four unsent second-round prompts with explicit anti-stopping terminal contracts.
- `SOURCE_SHA256SUMS.txt`: hashes of the intake files.

## Non-claims

- The full A endpoint is not proved by this intake.
- A threshold-limited enumeration is not a finite classification.
- A self-reported `PROVED` label is not independent certification.
- A missing compiler is not evidence for or against a mathematical claim.
- “No counterexample found” is never promoted to “proved.”
