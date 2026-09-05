# Independent verification package

Run from a directory containing the submitted proof package:

```bash
python3 independent_check.py /path/to/zhao_double_only_proved_and_audited.zip --json independent_check.json
sha256sum -c SHA256SUMS.txt
```

Expected first line:

```text
INDEPENDENT_FINITE_INTERFACE_CHECK_PASS
```

The mathematical audit is in `independent_verification.md`.  The checker is deliberately limited to finite interfaces and package integrity; the universal graph and quotient arguments are checked in the report.
