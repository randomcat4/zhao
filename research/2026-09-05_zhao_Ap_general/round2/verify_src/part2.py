        histogram_count = regular_count = 0
        for ms in product(range(h+1), repeat=p):
            histogram_count += 1
            if not any(ms):
                continue
            for b in range(p):
                regular = all(ms[(b-x) % p] - int(2*x % p == b) == r
                              for x in range(p) if ms[x])
                if not regular:
                    continue
                regular_count += 1
                seen: set[int] = set()
                bipartite = half = 0
                for x in range(p):
                    if not ms[x] or x in seen:
                        continue
                    y = (b-x) % p
                    seen.update([x, y])
                    if x == y:
                        assert ms[x] == r+1
                        half += 1
                    else:
                        assert ms[x] == ms[y] == r
                        bipartite += 1
                assert half <= 1
                assert sum(ms) == 2*r*bipartite+(r+1)*half
                assert sum(ms) != 3*p-1
        results.append({'p': p, 'all_histograms': histogram_count,
                        'regular_nonempty_histogram_target_pairs': regular_count})
    return {'results': results, 'target_total_solutions': 0,
            'scope': 'Involution-component interface only; not C_p^4 sequence enumeration.'}


def line_key(x: tuple[int, ...], p: int) -> tuple[int, ...]:
    lead = next(v for v in x if v)
    inv = pow(lead, -1, p)
    return tuple(v*inv % p for v in x)


def check_correction_bounds() -> dict:
    rng = random.Random(26090503)
    samples = 0
    rational_expansions = 0
    for p in [5, 7, 11]:
        for _ in range(15):
            n = 5*p-4
            xs: list[tuple[int, ...]] = []
            while len(xs) < n:
                if xs and rng.randrange(3) == 0:
                    x = rng.choice(xs)
                else:
                    x = tuple(rng.randrange(p) for _ in range(4))
                if any(x):
                    xs.append(x)
            mult = Counter(xs)
            h = max(mult.values())
            line_mult = Counter(line_key(x, p) for x in xs)
            b = max(line_mult.values())
            eq = sum(comb(m, 2) for m in mult.values())
            col = sum(comb(m, 2) for m in line_mult.values())
            ap = 0
            for center in range(n):
                ends = [i for i in range(n) if i != center]
                for i, j in combinations(ends, 2):
                    if all((xs[i][k]+xs[j][k]-2*xs[center][k]) % p == 0 for k in range(4)):
                        ap += 1
            inv2 = pow(2, -1, p)
            midpoint_sum = sum(mult[tuple((xs[i][k]+xs[j][k])*inv2 % p for k in range(4))]
                               for i, j in combinations(range(n), 2))
            c = comb(n, 2)
            assert ap+2*eq == midpoint_sum <= h*c
            assert 0 <= eq <= col
            assert 2*col <= (b-1)*n
            for _ in range(10):
                alpha, beta, gamma = [Fraction(rng.randrange(-15, 16), rng.randrange(1, 6))
                                       for _ in range(3)]
                rho = max(Fraction(0), -beta/(2*p))
                v = beta/p+2*rho
                tau = max(Fraction(0), -gamma, -(alpha+v)/2)
                u, w = alpha+v+2*tau, gamma+tau
                assert min(u, v, w, tau, rho) >= 0
                lhs = alpha*eq+(beta/p)*col+gamma*ap
                rhs = (u*eq+v*(col-eq)+w*ap+tau*(h*c-2*eq-ap)
                       +rho*((b-1)*n-2*col)-tau*h*c-rho*(b-1)*n)
                assert lhs == rhs
                assert lhs >= -tau*h*c-rho*(b-1)*n
                rational_expansions += 1
            samples += 1
    return {'positional_samples': samples,
            'literal_center_endpoint_AP_checks': samples,
            'rational_cone_expansion_checks': rational_expansions,
            'float_arithmetic_used': False,
            'scope': 'Only new correction identities/inequalities; projection identities are inherited.'}


def check_line_cap_interface() -> dict:
    results = []
    for p in [5, 7, 11]:
        count = zero_free = rigid = complete = 0
        for xs in combinations_with_replacement(range(1, p), p-2):
            count += 1
            reachable = {0}
            bad = False
            for x in xs:
                if (-x) % p in reachable:
                    bad = True
                reachable |= {(s+x) % p for s in reachable.copy()}
            if bad:
                continue
            zero_free += 1
            if len(set(xs)) == 1:
                rigid += 1
            else:
                assert len(reachable) == p
                complete += 1
        results.append({'p': p, 'all_line_multisets': count,
                        'zero_sum_free': zero_free, 'constant': rigid,
                        'nonconstant_complete_subset_sum': complete})
    return {'results': results,
            'scope': 'The prime-independent growth proof, not these cases, gives the line cap.'}


def check_symbolic_file() -> dict:
    data = json.loads((ROOT/'symbolic_interfaces.json').read_text(encoding='utf-8'))
    for key in ['deletion', 'local_moments']:
        m, inv = data[key]['matrix'], data[key]['inverse']
        n = len(m)
        assert [[sum(m[i][k]*inv[k][j] for k in range(n)) for j in range(n)]
                for i in range(n)] == [[int(i == j) for j in range(n)] for i in range(n)]
    gs = data['g_coefficients_ascending']
    assert gs == [4, 0, -5, 0, 1]
    assert all(sum(c*x**i for i, c in enumerate(gs)) == 0 for x in [1, -1, 2, -2])
    return {'integer_inverse_checks': 2, 'polynomial_root_checks_over_Z': 4,
            'full_A_p_certificate_claimed': False}


def main() -> None:
    ps = primes_through(997)
    report = {
        'status': 'ALL_EXACT_FINITE_INTERFACE_CHECKS_PASS',
        'universal_claim_proved_in_note': 'Any A_p counterexample has h(S) <= p-4 (p >= 5).',
        'not_claimed': ['a complete A_p proof', 'a counterexample family',
                        'a full all-p profile Farkas certificate',
                        'exhaustive testing of sequences over F_p^4'],
        'symbolic_file': check_symbolic_file(),
        'parameter_interfaces': check_parameter_interfaces(ps),
        'positional_complements': check_positional_complement_formulas(),
        'intersecting_triple_interface': check_empty_intersection_witnesses(),
        'fixed_sum_link_interface': check_link_involution(),
        'correction_bounds': check_correction_bounds(),
        'line_cap_interface': check_line_cap_interface(),
    }
    input_path = ROOT/'inputs'/'round1_research_note.md'
    report['inherited_input_sha256'] = hashlib.sha256(input_path.read_bytes()).hexdigest()
    out = ROOT/'verification_report.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
