# Zhao round two: double-only six-type theorem

This package contains a self-contained hand proof that every 21-position
sequence over F_5^4 of height at most two with at least one doubled value has
a nonempty zero-sum subsequence of length at most 13. In particular it covers
all six requested multiplicity types b=1,...,6.

The mathematical proof is in `proof_zh.md`. No exhaustive sequence search,
external computer classification, B theorem, or stabilizer lemma is used.
`RED_TEAM.md` records the explicit audit of the proof.

## Auxiliary arithmetic audits

Python 3.10 or later; standard library only.

```sh
sha256sum -c SHA256SUMS.txt
python3 audit_arithmetic.py
python3 verify_positions.py
```

The expected first lines are:

```text
ARITHMETIC_AUDIT_OK
POSITIONAL_AUDIT_OK
```

The scripts are not a global sequence enumerator. `verify_positions.py` neither
imports the first script nor reads its results. The supplied `.log` files are
complete actual outputs, with normal process exit status 0.

## Source provenance

The user supplied `zhao_B_proof_A_progress(2).md` and
`zhao_research_result(2).zip`, and the archive at
https://github.com/randomcat4/zhao/pull/1 . The read-only archive snapshot
examined for provenance was commit
`4e969914dec4a3150723b464d9d30fc3cf9433d6`.

The archived three-anchor argument suggested the quotient-and-replacement
route. Every lemma used in this new two-anchor proof is proved afresh in
`proof_zh.md`; no archived status label is used as a theorem. In particular,
this package does not redistribute or certify the archive's unrelated
computational classifications.

This is a hand proof and an in-response audit, not a claim of third-party
sign-off or formal proof-assistant verification.
