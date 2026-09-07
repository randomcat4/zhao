            positional += 1
    return {"admissible_cases_checked": checked,
            "multi_replacement_cases_excluded": rejected_multiple_replacement,
            "per_k": summaries, "independent_positional_cases": positional}


def check_prime_thresholds_and_counts() -> dict:
    prime_cases = 0
    for p in primes_up_to(1009):
        if p < 7:
            continue
        rho, h = (p+1)//2, p-4
        assert rho > min(4, h)
        assert (3*rho) % p != 0
        assert ((p-1)//2) != 1
        if p >= 29:
            assert 3*p*rho > 4*256
        if p >= 131:
            assert 3*p > 4+16+64 and rho > 64
        if p >= 149:
            assert rho-30 > 12
            assert 5*(p-59) > 3*p-2
            assert 3*p-135 > 2*p-2
        assert 8+3*h < 3*p
        assert 4+(h+1) < 3*p
        assert 3*p > 6 and rho > 2
        assert (2*rho) % p == 1
        prime_cases += 1
    assert 3*7-2 > 3*(7-4)+6
    return {"prime_cases": prime_cases, "cover_tree_nodes": 84,
            "outside_vertex_degree_cap": 64, "tau4_edge_cap": 256,
            "two_sided_link_witness_vertex_cap": 12,
            "two_sided_link_degree_sum_cap": 30,
            "pair_graph_unmatched_vertex_cap": 133,
            "same_value_cover_p7_outside_positions_at_least": 4}


def check_cross_pair_fibres() -> dict:
    checked = 0
    for p in [7, 11, 13, 17, 19, 23, 29, 31]:
        for qA in range(p):
            for qB in range(p):
                if qA == qB:
                    continue
                for v in range(p):
                    a = (qB - 2*(qA-v)) % p
                    b = (qA - 2*(qB-v)) % p
                    assert (a-b) % p == (-3*(qA-qB)) % p
                    assert a or b
                    checked += 1
    assert (1 - 2*(0-1)) % 3 == 0
    assert (0 - 2*(1-1)) % 3 == 0
    return {"distinct_sum_fibre_cases": checked,
            "characteristic_three_exception_confirmed": True}


def check_threefold_cover_interfaces() -> dict:
    arithmetic = algebraic = 0
    for p in primes_up_to(503):
        if p < 7:
            continue
        rho, s, h = (p+1)//2, (p-1)//2, p-4
        assert (-1-rho) % p != 0
        assert s >= 3 and s < p
        m = ((3-rho)*pow(3, -1, p)) % p
        assert m != 0
        if m <= h:
            assert 3 < rho
        if p >= 11:
            assert s > 3
        arithmetic += 1
    p = 7
    rho, s, h, delta = 4, 3, 3, 1
    m = ((3+delta-rho)*pow(3, -1, p)) % p
    assert m == 0
    md = ((rho-2)*pow(3, -1, p)) % p
    assert md == 3 <= h
    assert (3*s) % p != rho
    for p in [7, 11, 13, 17, 19]:
        for x in range(p):
            for y in range(p):
                if x == y:
                    continue
                for c in range(p):
                    if c in (x, y):
                        continue
                    u = (y+c-x) % p
                    assert u not in (y, c)
                    if p == 7 and (2*c-3*y+x) % p == 0:
                        d = (2*y-x) % p
                        assert d not in (x, y, c, u)
                    algebraic += 1
    return {"prime_arithmetic_cases": arithmetic,
            "label_distinctness_cases": algebraic,
            "p7_exception": {"delta": delta, "effective_m_u": m,
                              "forced_m_d": md, "degree_of_d_mod7": 2,
                              "required_degree_mod7": 4}}


def check_deletion_sign_independently() -> dict:
    checked = 0
    for p in [7, 11, 13, 17]:
        n = 3*p
        B = {0, 1, 2, 3}
        BC = set(range(n)) - B
        for i in range(n):
            contribution = sum((-1)**len(U) for U in (B, BC) if i not in U)
            assert contribution == 1-2*int(i in B)
            checked += 1
        assert (-(-1)*pow(2, -1, p)) % p == (p+1)//2
    return {"single_block_complement_position_checks": checked,
            "degree_residue_is_positive_half": True}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    report = {
        "status": "EXACT_FINITE_INTERFACES_PASS; UNIVERSAL_PROOFS_ARE_IN_NOTE",
        "not_claimed": ["A_p proved", "h <= p-5", "theta=-1 excluded",
                        "enumeration of all sequences", "formal kernel certification"],
        "input_round3_note_sha256": digest(ROOT/'inputs'/'round3_research_note.md'),
        "note_sha256": digest(ROOT/'research_note.md'),
        "checker_sha256": digest(Path(__file__)),
        "marked_lifts": check_marked_lifts(),
        "p7_positive_certificate": check_p7_positive_certificate(),
        "simultaneous_replacement": check_simultaneous_replacement_bound(),
        "cover_thresholds": check_prime_thresholds_and_counts(),
        "cross_pair_fibres": check_cross_pair_fibres(),
        "threefold_cover_interfaces": check_threefold_cover_interfaces(),
        "sign_check": check_deletion_sign_independently(),
    }
    output = ROOT/'verification_report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(report['status'])
    print('admissible replacement cases:', report['simultaneous_replacement']['admissible_cases_checked'])
    print('positional core cases:', report['simultaneous_replacement']['independent_positional_cases'])
    print('distinct-sum fibre checks:', report['cross_pair_fibres']['distinct_sum_fibre_cases'])
    print('report:', output)


if __name__ == '__main__':
    main()
