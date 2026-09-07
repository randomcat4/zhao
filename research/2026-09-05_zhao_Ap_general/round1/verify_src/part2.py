        if not any(total):
            result[mask.bit_count()] += 1
    return result


def count_ap(sequence: list[tuple[int, ...]], p: int) -> int:
    return sum(all((sequence[j][r] + sequence[k][r] - 2 * sequence[i][r]) % p == 0
                   for r in range(len(sequence[0])))
               for i in range(len(sequence))
               for j, k in itertools.combinations([x for x in range(len(sequence)) if x != i], 2))


def dependent_pair(x: tuple[int, ...], y: tuple[int, ...], p: int) -> bool:
    return any(all((a * u - v) % p == 0 for u, v in zip(x, y)) for a in range(1, p))


def check_projection() -> dict:
    results = []
    # Deliberately includes repeated values, collinear pairs, and actual APs.
    sequence = [(1, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0),
                (0, 1, 0, 0), (1, 1, 0, 0), (3, 0, 0, 0), (0, 0, 1, 0)]
    n = len(sequence)
    for p in (5, 7):
        reps = projective_reps(p)
        v, h, ell = p**3 + p**2 + p + 1, p**2 + p + 1, p + 1
        require(len(reps) == v and len(set(reps)) == v, 'projective denominator')
        require(sum(lam[0] == 0 for lam in reps) == h, 'annihilator of nonzero vector')
        require(sum(lam[0] == lam[1] == 0 for lam in reps) == ell, 'annihilator of independent pair')
        actual_z = zero_counts(sequence, p)
        eq = sum(x == y for x, y in itertools.combinations(sequence, 2))
        col = sum(dependent_pair(x, y, p) for x, y in itertools.combinations(sequence, 2))
        actual_ap = count_ap(sequence, p)
        total = tuple(sum(x[r] for x in sequence) % p for r in range(4))
        require(any(total), 'test total must be nonzero')
        sums_z = [0] * (n + 1)
        sums_E = sums_J = sums_ap = sums_T = 0
        # A small complete coefficient pattern: one coefficient 1, one 2, rest 0.
        actual_W = sum(not any((sequence[i][r] + 2 * sequence[j][r]) % p for r in range(4))
                       for i in range(n) for j in range(n) if i != j)
        sums_R = 0
        for lam in reps:
            values = [dot(lam, x, p) for x in sequence]
            profile = Counter(values)
            z = count_projected_zeros(values, p)
            sums_z = [a + b for a, b in zip(sums_z, z)]
            sums_E += sum(choose(c, 2) for c in profile.values())
            sums_J += choose(profile[0], 2)
            sums_T += sum(values) % p == 0
            sums_ap += sum((values[j] + values[k] - 2 * values[i]) % p == 0
                           for i in range(n)
                           for j, k in itertools.combinations([x for x in range(n) if x != i], 2))
            sums_R += sum((values[i] + 2 * values[j]) % p == 0
                          for i in range(n) for j in range(n) if i != j)
        require(sums_z == [h * choose(n, k) + p**3 * actual_z[k] for k in range(n + 1)], 'z projection')
        require(sums_E == h * choose(n, 2) + p**3 * eq, 'equal-pair correction')
        require(sums_J == ell * choose(n, 2) + p**2 * col, 'collinearity correction')
        require(sums_ap == h * n * choose(n - 1, 2) + p**3 * actual_ap, 'AP correction')
        require(sums_T == h, 'total-sum indicator')
        require(sums_R == h * n * (n - 1) + p**3 * actual_W, 'weighted-type projection')
        results.append({'p': p, 'projective_points': v, 'one_vector_annihilators': h,
                        'two_independent_vector_annihilators': ell,
                        'equal_position_pairs': eq, 'collinear_position_pairs': col,
                        'actual_AP_configurations': actual_ap})
    return {'cases': results, 'claim': 'Counts include all positional multiplicity correction terms.'}


def check_anchor_polynomial() -> dict:
    reflection_tests = 0
    compression_tests = 0
    primes = primes_up_to(101)
    for p in primes:
        for d in (3, 4):
            possibilities = [(t, m) for t in range(5) for m in range(p)
                             if d * (p - 1) + 2 == 2 * (p - 1) * t + m]
            require(possibilities == ([] if d == 3 else [(2, 2)]), 'reflection arithmetic')
            if d == 4:
                require(2 * p <= 4 * p - 5, 'reflection short zero length')
            reflection_tests += 1
        for q in (1, 2):
            g0 = math.prod(-j * j for j in range(1, q + 1)) % p
            require(g0 != 0, 'anchor polynomial constant')
            for c in list(range(1, q + 1)) + [-j for j in range(1, q + 1)]:
                require(math.prod(c * c - j * j for j in range(1, q + 1)) % p == 0,
                        'anchor polynomial roots')
            for n in range(3 * p - 1, 4 * p - 4):
                if n <= 3 * p + 2 * q - 2:
                    continue
                if n % 2 == 0:
                    require(n > 3 * (p - 1) + 2 * q, 'even certificate degree')
                    require(g0 * (1 + (-1)**n) % p != 0, 'even contradiction')
                else:
                    require(n > 3 * (p - 1) + 2 * q + 1, 'odd certificate degree')
                    require(((-1)**n) * n * g0 % p != 0, 'odd contradiction')
                compression_tests += 1
        require(all(2 * e % p != 0 for e in range(1, p - 1)), 'final p-2-anchor star contradiction')
    return {'primes': primes, 'reflection_tests': reflection_tests,
            'scalar_compression_tests': compression_tests,
            'claim': 'Finite arithmetic checks of the universal polynomial argument; the combinatorial proof is in the note.'}


def partitions_by_height(n: int, maximum: int) -> tuple[list[int], list[list[int]]]:
    types = []
    def recurse(h: int, left: int, counts: list[int]) -> None:
        if h == 1:
            types.append([left] + counts)
            return
        for count in range(left // h + 1):
            recurse(h - 1, left - h * count, [count] + counts)
    recurse(maximum, n, [])
    histogram = [0] * maximum
    for counts in types:
        height = max(i + 1 for i, count in enumerate(counts) if count)
        histogram[height - 1] += 1
        require(sum((i + 1) * count for i, count in enumerate(counts)) == n, 'partition weight')
    # Independent generating-function count.
    dp = [1] + [0] * n
    for h in range(1, maximum + 1):
        for j in range(h, n + 1):
            dp[j] += dp[j - h]
    require(dp[n] == len(types), 'partition denominator')
    return histogram, types


def check_p7() -> dict:
    histogram, types = partitions_by_height(31, 5)
    require(histogram == [1, 15, 80, 225, 427], 'p7 multiplicity histogram')
    p = 7
    points = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0),
              (1, 0, 0, 1), (1, 1, 1, 1)]
    caps = [5, 5, 5, 5, 3]
    zeros = []
    positional_counts = Counter()
    vectors_checked = 0
    for counts in itertools.product(*(range(m + 1) for m in caps)):
        vectors_checked += 1
        if not any(counts):
            continue
        if all(sum(counts[i] * points[i][r] for i in range(5)) % p == 0 for r in range(4)):
            zeros.append(list(counts))
            positional_counts[sum(counts)] += math.prod(choose(caps[i], counts[i]) for i in range(5))
    require(zeros == [[4, 5, 5, 5, 2]], 'local witness zero-count vector')
    require(dict(positional_counts) == {21: 15}, 'local witness positional count')
    return {'formal_length_31_types_before_p_minus_2_anchor': len(types),
            'exact_maximum_multiplicity_1_to_5': histogram,
            'height_5_types_eliminated_by_uniform_proof': 427,
            'formal_types_remaining_after_uniform_proof': 321,
            'remaining_height_4_types': 225,
            'warning': 'Formal multiplicity partitions are not realizable counterexamples and do not classify vector assignments.',
            'local_witness': {'p': p, 'points': points, 'multiplicities': caps, 'length': sum(caps),
                              'count_vectors_checked_including_empty': vectors_checked,
                              'nonempty_zero_count_vectors': zeros,
                              'positional_zero_counts_by_length': dict(positional_counts),
                              'is_A7_counterexample': False,
                              'reason': 'Length 23, not the required 31; this is only a local-structure witness.'}}


def check_certificate_degrees() -> dict:
    patterns = [(0,0,20,1),(0,0,1,20),(0,0,18,3),(0,1,19,1),
                (0,0,6,15),(0,0,1,3),(0,0,2,19),(0,1,18,1),
                (0,0,2,18),(0,0,18,2),(0,1,2,18),(0,0,4,17),
