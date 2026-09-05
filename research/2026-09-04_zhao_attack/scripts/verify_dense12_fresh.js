"use strict";

// Independent verifier. Reads only the three assigned inputs; does not load the
// author's enumeration code. All arithmetic is integral, modulo 5 where needed.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..");
const inputPaths = [
  "proofs/hyperplane_dense12.md",
  "evidence/atom_127_classification.json",
  "proofs/lower_bound_18_B.md",
];
const inputBytes = Object.fromEntries(inputPaths.map(p => [p, fs.readFileSync(path.join(root, p))]));
const sha256 = b => crypto.createHash("sha256").update(b).digest("hex");
const inputHashes = Object.fromEntries(inputPaths.map(p => [p, sha256(inputBytes[p])]));
const cert = JSON.parse(inputBytes[inputPaths[1]].toString("utf8"));
const mod = n => ((n % 5) + 5) % 5;
const sum = v => v.reduce((a, b) => a + b, 0);
const key = v => v.join(",");
const encode = v => v.reduce((a, b, i) => a + b * 5 ** i, 0);
const decode = (n, d) => Array.from({ length: d }, (_, i) => Math.floor(n / 5 ** i) % 5);
const vector = (v, d) => Array.isArray(v) && v.length === d && v.every(x => Number.isInteger(x) && x >= 0 && x < 5);
const sortedKeys = vs => vs.map(key).sort();
const det3 = m => mod(
  m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
  - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
  + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
);
const multiply = (m, v) => m.map(row => mod(sum(row.map((x, i) => x * v[i]))));
const histogram = values => Object.fromEntries(
  [...new Set(values)].sort((a, b) => a - b).map(v => [v, values.filter(x => x === v).length])
);

// Enumerate actual position subsets, not multiplicity coefficient tuples.
function positionSubsets(positions, dimension) {
  const count = 2 ** positions.length;
  const targets = new Uint16Array(count);
  const lengths = new Uint8Array(count);
  const minimum = Array(5 ** dimension).fill(Infinity);
  const witnesses = Array(5 ** dimension).fill(null);
  const zeroMasks = [];
  const zeroHistogram = {};
  for (let mask = 0; mask < count; ++mask) {
    if (mask > 0) {
      const lowBit = mask & -mask;
      const position = 31 - Math.clz32(lowBit);
      const previous = mask ^ lowBit;
      const previousVector = decode(targets[previous], dimension);
      targets[mask] = encode(previousVector.map((v, i) => mod(v + positions[position][i])));
      lengths[mask] = lengths[previous] + 1;
    }
    const target = targets[mask];
    const length = lengths[mask];
    if (length < minimum[target]) {
      minimum[target] = length;
      witnesses[target] = mask;
    }
    if (target === 0) {
      zeroMasks.push(mask);
      zeroHistogram[length] = (zeroHistogram[length] ?? 0) + 1;
    }
  }
  return { minimum, witnesses, zeroMasks, zeroHistogram, subsetsChecked: count };
}

const expectedBlocks = [
  [345, 455, 505], [215, 225, 565], [160, 185, 505],
  [45, 180, 305], [45, 220, 345], [45, 415, 485],
  [30, 190, 315], [30, 210, 335], [30, 420, 480],
];
const expectedHistogram = { 0: 1, 1: 6, 2: 19, 3: 36, 4: 35, 5: 19, 6: 8, 12: 1 };
const standardBasis3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
assert.equal(cert.records.length, 9);
assert.equal(cert.core_count, 9);
assert.equal(cert.single_GL_H_orbit, true);
assert.equal(cert.group, "C_5^4");
assert.equal(cert.h_equation, "first coordinate = 0");
assert.deepEqual(cert.outside_tripled_element, [1, 0, 0, 0]);
assert.deepEqual(cert.records.map(r => r.blocks_encoded), expectedBlocks);
const reference = cert.reference_support_h;
assert.equal(reference.length, 6);
assert(reference.every(v => vector(v, 3)));
assert.equal(new Set(reference.map(key)).size, 6);
assert.deepEqual(reference.slice(0, 3), standardBasis3);
assert.deepEqual(reference.slice(3).map(v => encode([0, ...v])).sort((a, b) => a - b), cert.reference_blocks_encoded);
const referenceSet = sortedKeys(reference);
const refKeyToIndex = new Map(reference.map((v, i) => [key(v), i]));

// Source basis is explicitly checked. Independently try all ordered triples of
// reference support points as images of that basis: at most 6*5*4 candidates.
function findOrbitMap(support) {
  let tried = 0;
  for (let a = 0; a < 6; ++a) for (let b = 0; b < 6; ++b) for (let c = 0; c < 6; ++c) {
    if (a === b || a === c || b === c) continue;
    ++tried;
    const matrix = [0, 1, 2].map(i => [reference[a][i], reference[b][i], reference[c][i]]);
    const determinant = det3(matrix);
    if (determinant === 0) continue;
    const images = support.map(v => multiply(matrix, v));
    if (JSON.stringify(sortedKeys(images)) === JSON.stringify(referenceSet)) {
      return { matrix, determinant, supportPermutation: images.map(v => refKeyToIndex.get(key(v))), candidatesTried: tried };
    }
  }
  throw new Error("No independent linear orbit map found");
}

const records = cert.records.map(record => {
  const support = record.support_h;
  assert.equal(support.length, 6);
  assert(support.every(v => vector(v, 3)));
  assert.equal(new Set(support.map(key)).size, 6);
  assert.deepEqual(support.slice(0, 3), standardBasis3);
  assert.deepEqual(support.slice(3).map(v => encode([0, ...v])).sort((a, b) => a - b), record.blocks_encoded);
  assert.deepEqual(record.h_multiplicities, [2, 2, 2, 2, 2, 2]);
  assert.equal(record.coefficient_tuples_checked, 3 ** 6);
  const positions = support.flatMap(v => [v, v]);
  const result = positionSubsets(positions, 3);
  assert.deepEqual(result.zeroMasks, [0]);
  assert.equal(record.zero_sum_free, true);
  assert(result.minimum.every(Number.isFinite));
  const sigma = [0, 1, 2].map(i => mod(sum(positions.map(v => v[i]))));
  const sigmaIndex = encode(sigma);
  assert.notEqual(sigmaIndex, 0);
  assert.deepEqual(record.sigma_h, sigma);
  assert.deepEqual(record.negative_sigma_h, sigma.map(v => mod(-v)));
  assert.equal(result.minimum[sigmaIndex], 12);
  assert.equal(Math.max(...result.minimum.filter((_, i) => i !== sigmaIndex)), 6);
  const actualHistogram = histogram(result.minimum);
  assert.deepEqual(actualHistogram, record.distance_histogram);
  assert.deepEqual(actualHistogram, expectedHistogram);

  const rows = record.all_125_minimum_representations;
  assert.equal(rows.length, 125);
  const seen = new Set();
  for (const row of rows) {
    assert(vector(row.target_h, 3));
    const target = encode(row.target_h);
    assert(!seen.has(target));
    seen.add(target);
    assert.equal(row.coefficients.length, 6);
    assert(row.coefficients.every(x => Number.isInteger(x) && x >= 0 && x <= 2));
    assert.equal(sum(row.coefficients), row.minimum_length);
    const represented = [0, 1, 2].map(i => mod(sum(support.map((v, j) => v[i] * row.coefficients[j]))));
    assert.deepEqual(represented, row.target_h);
    assert.equal(row.minimum_length, result.minimum[target]);
  }
  assert.equal(seen.size, 125);

  const supplied = record.matrix_h_to_reference;
  assert.equal(supplied.length, 3);
  assert(supplied.every(v => vector(v, 3)));
  const suppliedDeterminant = det3(supplied);
  assert.notEqual(suppliedDeterminant, 0);
  assert.equal(record.matrix_h_determinant, suppliedDeterminant);
  assert.deepEqual(sortedKeys(support.map(v => multiply(supplied, v))), referenceSet);
  const expectedExtension = [
    [1, 0, 0, 0],
    ...supplied.map(row => [0, ...row]),
  ];
  assert.deepEqual(record.matrix_c5_4_to_reference, expectedExtension);
  assert.deepEqual(multiply(expectedExtension, [1, 0, 0, 0]), [1, 0, 0, 0]);
  const independentOrbitMap = findOrbitMap(support);
  return {
    blocksEncoded: record.blocks_encoded,
    support,
    multiplicities: [2, 2, 2, 2, 2, 2],
    positionSubsetsChecked: result.subsetsChecked,
    nonemptyZeroSumCount: result.zeroMasks.length - 1,
    sigma,
    histogram: actualHistogram,
    distanceAtSigma: result.minimum[sigmaIndex],
    maximumDistanceAwayFromSigma: 6,
    all125SuppliedWitnessesAndMinimaVerified: true,
    distanceIndexConvention: "i = h[0] + 5*h[1] + 25*h[2]",
    minimumDistances: result.minimum,
    minimizingPositionMasks: result.witnesses,
    positionOrder: "two consecutive positions per listed support value",
    suppliedOrbitMapVerified: true,
    suppliedOrbitDeterminant: suppliedDeterminant,
    independentOrbitMap,
  };
});
assert.equal(new Set(records.map(r => sortedKeys(r.support).join(";")).values()).size, 9);
const referenceRecord = records.find(r => JSON.stringify(r.blocksEncoded) === JSON.stringify(cert.reference_blocks_encoded));
assert(referenceRecord);
assert.deepEqual(referenceRecord.support, reference);

// Exhaust all 165 multiplicity vectors. Each property is position-permutation
// invariant; multinomial weights independently check coverage of all 4^8 words.
function factorial(n) { let answer = 1; for (let i = 2; i <= n; ++i) answer *= i; return answer; }
let coveredWords = 0;
const c5Checks = [];
for (let n1 = 0; n1 <= 8; ++n1) for (let n2 = 0; n2 <= 8 - n1; ++n2) for (let n3 = 0; n3 <= 8 - n1 - n2; ++n3) {
  const counts = [n1, n2, n3, 8 - n1 - n2 - n3];
  const word = counts.flatMap((n, i) => Array(n).fill(i + 1));
  const wordWeight = factorial(8) / counts.reduce((a, b) => a * factorial(b), 1);
  coveredWords += wordWeight;
  if (Math.max(...counts) >= 6) {
    c5Checks.push({ counts, wordWeight, outcome: "multiplicity_at_least_six" });
    continue;
  }
  const zero = [];
  for (let mask = 1; mask < 256; ++mask) {
    let length = 0;
    let total = 0;
    for (let j = 0; j < 8; ++j) if ((mask & (1 << j)) !== 0) { ++length; total += word[j]; }
    if (mod(total) === 0) zero.push({ mask, length });
  }
  let pair = null;
  for (let i = 0; i < zero.length && pair === null; ++i) for (let j = i + 1; j < zero.length; ++j) {
    if ((zero[i].mask & zero[j].mask) === 0 && zero[i].length + zero[j].length <= 7) {
      pair = [zero[i], zero[j]];
      break;
    }
  }
  assert(pair !== null, `C5 lemma failed at ${counts}`);
  c5Checks.push({ counts, wordWeight, outcome: "two_disjoint_zero_sums_total_at_most_seven", pair });
}
assert.equal(c5Checks.length, 165);
assert.equal(coveredWords, 4 ** 8);

const lowerPositions = [
  ...Array.from({ length: 4 }, () => [1, 0, 0, 0]),
  ...Array.from({ length: 4 }, () => [0, 1, 0, 0]),
  ...Array.from({ length: 4 }, () => [0, 0, 1, 0]),
  ...Array.from({ length: 4 }, () => [0, 0, 0, 1]),
  [3, 1, 1, 1], [3, 1, 1, 1],
];
const lower = positionSubsets(lowerPositions, 4);
assert.deepEqual(lower.zeroHistogram, { 0: 1, 15: 76 });
const lowerClasses = {};
for (const mask of lower.zeroMasks) {
  const k = ((mask >> 16) & 1) + ((mask >> 17) & 1);
  const coefficients = [0, 1, 2, 3].map(i => {
    let count = 0;
    for (let j = 0; j < 4; ++j) if ((mask & (1 << (i * 4 + j))) !== 0) ++count;
    return count;
  });
  if (lowerClasses[k] === undefined) lowerClasses[k] = { coefficients, positionSubsetCount: 0, length: k + sum(coefficients) };
  assert.deepEqual(lowerClasses[k].coefficients, coefficients);
  ++lowerClasses[k].positionSubsetCount;
}
assert.deepEqual(lowerClasses, {
  0: { coefficients: [0, 0, 0, 0], positionSubsetCount: 1, length: 0 },
  1: { coefficients: [2, 4, 4, 4], positionSubsetCount: 12, length: 15 },
  2: { coefficients: [4, 3, 3, 3], positionSubsetCount: 64, length: 15 },
});

for (const p of inputPaths) assert.equal(sha256(fs.readFileSync(path.join(root, p))), inputHashes[p], `${p} changed while checking`);
const output = {
  status: "CORRECT_FOR_ASSIGNED_LOCAL_CLAIMS",
  inputsSha256: inputHashes,
  verifierSha256: sha256(fs.readFileSync(__filename)),
  arithmetic: "exact integer arithmetic; group operations reduced modulo 5",
  scope: "assigned nine cores only; no completeness claim about other zero-sum-free cores and no complete A21/B20 claim",
  uncheckedInputFields: ["source_sha256", "script_sha256", "global_coefficient_tuples_checked", "safe_all_a", "safe_outside_core_a", "safe_all_b", "safe_outside_core_b", "exceptional_values_encoded"],
  cores: records,
  c5Lemma: {
    multiplicityVectorsChecked: c5Checks.length,
    orderedWordsCovered: coveredWords,
    multiplicityAtLeastSixCases: c5Checks.filter(c => c.outcome === "multiplicity_at_least_six").length,
    disjointPairCases: c5Checks.filter(c => c.outcome !== "multiplicity_at_least_six").length,
    witnesses: c5Checks,
  },
  lowerBound18: {
    positions: lowerPositions,
    positionSubsetsChecked: lower.subsetsChecked,
    zeroSumLengthHistogramIncludingEmpty: lower.zeroHistogram,
    zeroSumClasses: lowerClasses,
    allNonemptyZeroSumPositionMasks: lower.zeroMasks.filter(mask => mask !== 0),
  },
};
const outputPath = path.join(root, "evidence/verify_dense12_fresh.json");
fs.writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n");
console.log(JSON.stringify({
  status: output.status,
  inputHashes,
  coresVerified: records.length,
  corePositionSubsetsChecked: sum(records.map(r => r.positionSubsetsChecked)),
  minimumRepresentationRowsVerified: records.length * 125,
  commonHistogram: expectedHistogram,
  c5MultiplicityVectorsChecked: c5Checks.length,
  c5OrderedWordsCovered: coveredWords,
  lowerBound18ZeroSums: lower.zeroHistogram,
  output: outputPath,
}, null, 2));
