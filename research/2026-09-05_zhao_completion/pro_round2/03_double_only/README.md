# PRO round 2 — double-only six-type closure

This directory preserves the second-round result for the frozen multiplicity cells

\[
|S|=21,\qquad h(S)\le 2,\qquad 1\le b\le 6,
\]

where exactly \(b\) actual values occur twice and all other actual values occur once. Subsequences are positional. The reported and independently rechecked conclusion is:

> Every such sequence over \(\mathbb F_5^4\) has a nonempty zero-sum subsequence of length at most 13.

The proof is a hand proof. It does not use an exhaustive classification of all sequences, the rescued B proof, the earlier stabilizer lemma, or an assumption that equal-valued positions can be merged. Its auxiliary programs check finite arithmetic, complement, deletion-sign, and positional-incidence interfaces only.

## Verification record

- Submitted terminal status: `PROVED_AND_AUDITED`.
- Separate second-pass audit: `PASS`.
- All supplied Python programs use only the standard library and replay with exit status 0.
- The independent checker does not import either submitted checker.
- This is not a Lean/Coq kernel certificate and is not represented as external institutional sign-off.

The repository-wide A endpoint remains open because the 21-element squarefree cell is not closed. The archived three-anchor proof is also kept under its own stated verification boundary.

## Contents

- `proof/proof_zh.md` — self-contained proof and boundary audit.
- `proof/RED_TEAM.md` — adversarial checks of the submitted proof.
- `proof/audit_arithmetic.py`, `proof/verify_positions.py` — two submitted finite-interface checkers.
- `proof/*.json`, `proof/*.log`, `proof/SHA256SUMS.txt` — submitted outputs and manifest.
- `independent_verification/independent_verification.md` — separate line audit and re-derivation.
- `independent_verification/independent_check.py` — checker written independently of the submitted checkers.
- `independent_verification/*.json`, `independent_verification/*.log`, `independent_verification/SHA256SUMS.txt` — independent output and manifest.
- `repo_check.py` — repository-mode replay of the independently written finite-interface logic against the committed `proof/` directory.

## Original package hashes

The two original response ZIPs were used for the recorded independent replay. Their decompressed contents are committed below; the binary ZIPs are not duplicated in this PR.

```text
99451451102aa38ff1959fe375510ae4deed4558886d8ca3edc3ba4b8de5fad3  zhao_double_only_proved_and_audited.zip
fcb457febef3959237afbd2eee70115aecf1f4b122a6535e926ebef53dc6dfbf  zhao_independent_verification.zip
```

## Reproduction

From this directory:

```bash
(
  cd proof
  sha256sum -c SHA256SUMS.txt
  python3 -I audit_arithmetic.py
  python3 -I verify_positions.py
)

(
  cd independent_verification
  sha256sum -c SHA256SUMS.txt
)

python3 -I repo_check.py proof --json /tmp/zhao-repository-check.json
```

Expected status lines:

```text
ARITHMETIC_AUDIT_OK
POSITIONAL_AUDIT_OK
REPOSITORY_FINITE_INTERFACE_CHECK_PASS
```

The finite checker explicitly records that it is not a global enumeration of sequences in \(\mathbb F_5^4\); the universal graph, quotient, and capacity arguments are checked in the two Markdown reports.
