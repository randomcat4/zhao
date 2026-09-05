#!/usr/bin/env python3
"""Re-run the finite A exclusions. No third-party Python packages or network needed.

Requires Python 3.10+ and GNU g++ with C++17 support. The C++ sources use
GNU libstdc++ bitset scanning extensions. B is proved in proof_progress.md;
these finite computations are NOT premises of the new B closure.
"""
from __future__ import annotations
import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=['smoke', 'complete'], default='smoke')
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    compiler = shutil.which(args.compiler)
    if compiler is None:
        raise SystemExit(f'Compiler not found: {args.compiler}')
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    output = ROOT / f'rerun_{args.suite}.txt'
    compiled: set[str] = set()

    def run(name: str, *arguments: object) -> str:
        if name not in compiled:
            subprocess.run([compiler, '-O3', '-std=c++17', str(ROOT/'source'/f'{name}.cpp'),
                            '-o', str(build/name)], check=True)
            compiled.add(name)
        cmd = [str(build/name), *(str(x) for x in arguments)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        text = result.stdout
        with output.open('a', encoding='utf-8') as f:
            f.write('$ ' + ' '.join(cmd) + '\n' + text)
            if result.stderr:
                f.write(result.stderr)
        print(text.strip(), flush=True)
        if re.search(r'\bFOUND(?:_A)?\b|MISMATCH|DISAGREEMENT|overflow', text + result.stderr):
            raise RuntimeError('A reported counterexample or internal disagreement requires review.')
        return text

    output.write_text('', encoding='utf-8')
    t = run('verify_class7')
    assert 'normalized_sevens=3472' in t and 'max_extension_capacity=4' in t
    assert 'max_same_coset_extensions=0' in t
    t = run('oracle_check')
    assert 'H_core_types=45' in t and 'exact_length_queries=12150000' in t and 'mismatches=0' in t
    if args.suite == 'smoke':
        print('SMOKE PASS. This is an interface check, not a replay of all finite trees.')
        return

    t = run('h9_class6_complete', 1, 124)
    assert 'cores=2948970' in t and 'A_endpoints=0' in t
    for m, count in [(5, 4653100), (4, 310124), (3, 7626)]:
        t = run('h9_class_attack', 1, 124, m)
        assert f'cores={count}' in t and 'A_endpoints=0' in t
    t = run('core_clique', 'a2b3')
    assert 'safe_cores=371' in t and 'endpoints=0' in t
    t = run('core_clique_dynamic', 'a2b2_rank4')
    assert 'safe_cores=1' in t and 'endpoints=0' in t
    t = run('scan_H10')
    core_values = [int(line.split()[0]) for line in t.splitlines() if line.strip()]
    assert len(core_values) == len(set(core_values)) == 44
    for g in core_values:
        t = run('H10_class7_scan', g)
        assert 'normalized_sevens=0' in t
    # Descending M is part of the proof: larger maximum classes are excluded first.
    for m in [6, 5, 4, 3]:
        for g in core_values:
            t = run('H10_class_attack', 1, 124, m, g)
            assert f'H10_g={g}' in t and 'A_endpoints=0' in t and 'COMPLETE' in t
    print('COMPLETE PASS for the stated A subfamilies. This does not prove all of A.')


if __name__ == '__main__':
    main()
