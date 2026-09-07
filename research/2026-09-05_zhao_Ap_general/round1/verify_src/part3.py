                (0,0,19,1),(0,0,1,19),(0,1,1,19),(0,0,1,2),
                (0,1,3,0),(0,10,11,0)]
    entries = []
    for c in patterns:
        full = (21 - sum(c),) + c
        background = max(range(5), key=lambda i: full[i])
        r = 21 - full[background]
        param7 = None
        for p in (5, 7, 11, 101):
            parameterized = list(full) + [0] * (p - 5)
            parameterized[background] = 5 * p - 4 - r
            require(sum(parameterized) == 5 * p - 4, 'parameterized coefficient type length')
            require(5 * p - 4 - max(parameterized) == r, 'fixed exceptional degree')
            if p == 5:
                require(tuple(parameterized) == full, 'p5 specialization')
            if p == 7:
                param7 = parameterized
        entries.append({'c1_c2_c3_c4': c, 'background_coefficient': background,
                        'number_of_exceptional_positions': r,
                        'parameterized_p7_type': param7})
    return {'p5_patterns': entries,
            'exception_counts': [x['number_of_exceptional_positions'] for x in entries],
            'claim': 'This rewrites coefficient types, not the final Farkas inequality for general p.'}


def exact_type_count(values: list[int], c: tuple[int, ...], p: int) -> int:
    """Literal positional coefficient assignments, for small interface tests."""
    remaining = list(c)
    def visit(i: int, total: int) -> int:
        if i == len(values):
            return int(total % p == 0)
        result = 0
        for coefficient, count in enumerate(remaining):
            if count:
                remaining[coefficient] -= 1
                result += visit(i + 1, (total + coefficient * values[i]) % p)
                remaining[coefficient] += 1
        return result
    return visit(0, 0)


def exception_profile_count(values: list[int], c: tuple[int, ...], p: int) -> int:
    """Equation (9.2), using exact integer multinomial factors."""
    profile = Counter(values)
    b = max(range(p), key=lambda i: c[i])
    exceptional = [i for i in range(p) if i != b and c[i]]
    limits = tuple(c[i] for i in exceptional)
    target = -b * sum(values) % p
    dp = {(tuple(0 for _ in limits), 0): 1}
    for j in range(p):
        m = profile[j]
        new = defaultdict(int)
        for (used, weight), count in dp.items():
            for allocation in itertools.product(*(range(limit - u + 1)
                                                   for limit, u in zip(limits, used))):
                if sum(allocation) > m:
                    continue
                multiplicity = math.factorial(m) // math.factorial(m - sum(allocation))
                divisor = math.prod(math.factorial(a) for a in allocation)
                require(multiplicity % divisor == 0, 'integer profile multinomial')
                multiplicity //= divisor
                used2 = tuple(u + a for u, a in zip(used, allocation))
                weight2 = (weight + sum((d - b) * j * a
                                        for d, a in zip(exceptional, allocation))) % p
                new[(used2, weight2)] += count * multiplicity
        dp = dict(new)
    return dp.get((limits, target), 0)


def check_profile_rewrite() -> dict:
    cases = 0
    for p in (5, 7):
        patterns = [(3, 1, 2, 0, 0), (0, 0, 1, 4, 1),
                    (1, 1, 0, 0, 4), (0, 0, 0, 5, 1)]
        profiles = [[0, 1, 1, 2, 3, 4], [1] * 6, [0] * 6, [0, 2, 2, 3, 4, 4]]
        for base in patterns:
            c = tuple(base) + (0,) * (p - 5)
            for values in profiles:
                require(exact_type_count(values, c, p) == exception_profile_count(values, c, p),
                        'background/exception integer identity')
                cases += 1
    return {'cases': cases, 'claim': 'Literal positional assignments equal the conditional factorial-polynomial formula.'}


def check_complete_core() -> dict:
    scalar_tests = 0
    for p in primes_up_to(101):
        h = p - 3
        residues = set(range(h + 1)) | {(j + 2) % p for j in range(h + 1)}
        require(residues == set(range(p)), 'p-3 anchors plus a block of sum 2a cover the line')
        require(h + 2 == p - 1, 'complete core positional budget')
        scalar_tests += 1
    explicit_tests = 0
    for p in (5, 7):
        a = (1, 0, 0, 0)
        core = [a] * (p - 3) + [(0, 1, 0, 0), (2, p - 1, 0, 0)]
        sums = {(0, 0, 0, 0)}
        for x in core:
            sums |= {add_vector(t, x, p) for t in list(sums)}
        require(all((j, 0, 0, 0) in sums for j in range(p)), 'off-line complete core')
        explicit_tests += 1
    return {'scalar_tests': scalar_tests, 'off_line_positional_examples': explicit_tests,
            'p7_height4_remaining_anchor_free_zero_lengths': [21, 22, 23],
            'claim': 'A core need only represent the line; its individual positions need not lie on it.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('verification_report.json'))
    args = parser.parse_args()
    result = {
        'research_status': 'A_p_NOT_SOLVED',
        'full_A_p_proof': False,
        'verified_A_p_counterexample_family': False,
        'finite_interfaces_passed': True,
        'deletion_parametrization': check_deletion(),
        'marked_quotient_moments': check_marked_moments(),
        'projective_double_counting': check_projection(),
        'anchor_polynomial': check_anchor_polynomial(),
        'p7_structural_check': check_p7(),
        'coefficient_type_rewrite': check_certificate_degrees(),
        'background_exception_identity': check_profile_rewrite(),
        'complete_core': check_complete_core(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('FINITE_INTERFACE_CHECKS_PASS')
    print('ALL_PRIME_p_MINUS_2_ANCHOR_PROOF: see research_note.md')
    print('A_p_NOT_SOLVED; NO_A_p_COUNTEREXAMPLE_FAMILY')
    print(args.output)


if __name__ == '__main__':
    main()
