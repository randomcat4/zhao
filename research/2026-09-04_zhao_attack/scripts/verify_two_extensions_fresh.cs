using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Numerics;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Diagnostics;

// Independent verifier. No producer assembly, source module, solver, or distance
// state is imported. Core distances enumerate every bounded coefficient tuple.
// Dynamic extension states use scalar minimum distances, not exact-length bits.
public static class VerifyTwoExtensionsFresh
{
    const int Q = 625, Inf = 99, Cutoff = 13;
    static readonly int[] Basis = { 1, 5, 25, 125 };
    static readonly int[] BaseSequence = { 1,1,1,5,5,5,25,25,125,125 };
    static int[][] Coordinates, Plus;
    static int[] Negative;
    static string Root;
    static long CoefficientTuples, CoreTuples, PairTests, SameColorTests;
    static long Nodes, DynamicRejects, StaticEdgeRejects, BlockDomainTests;
    static readonly SortedDictionary<int,long> CandidateHistogram = new();
    static readonly SortedDictionary<int,long> ColorHistogram = new();
    static readonly SortedDictionary<int,long> HyperplaneMaxHistogram = new();
    static readonly SortedDictionary<int,long> H12CountHistogram = new();
    static readonly SortedDictionary<int,long> TotalLevels = new();
    static readonly SortedDictionary<int,long> TotalLeaves = new();
    static readonly SortedDictionary<string,long> TotalPrunes = new();
    static readonly JsonSerializerOptions Pretty = new() { WriteIndented = true };

    static void Require(bool condition, string message)
    { if (!condition) throw new InvalidOperationException(message); }
    static void Inc<K>(SortedDictionary<K,long> map, K key, long amount = 1) where K : notnull
    { map.TryGetValue(key, out long old); map[key] = old + amount; }
    static string PathAt(string relative)
    {
        string path = Path.GetFullPath(Path.Combine(Root, relative));
        Require(path.StartsWith(Root + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase), "Path outside approved run: " + relative);
        return path;
    }
    static string Sha(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
    static JsonElement ReadJson(string relative) => JsonDocument.Parse(File.ReadAllText(PathAt(relative), Encoding.UTF8)).RootElement.Clone();
    static List<JsonElement> ReadLines(string relative) => File.ReadLines(PathAt(relative), Encoding.UTF8)
        .Where(x => !String.IsNullOrWhiteSpace(x)).Select(x => JsonDocument.Parse(x).RootElement.Clone()).ToList();
    static int I(JsonElement x, string name) => x.GetProperty(name).GetInt32();
    static long L(JsonElement x, string name) => x.GetProperty(name).GetInt64();
    static bool B(JsonElement x, string name) => x.GetProperty(name).GetBoolean();
    static string S(JsonElement x, string name) => x.GetProperty(name).GetString();
    static int[] Ints(JsonElement x) => x.EnumerateArray().Select(y => y.GetInt32()).ToArray();
    static BigInteger[] Bigs(JsonElement x) => x.EnumerateArray().Select(y => BigInteger.Parse(y.GetRawText(), System.Globalization.CultureInfo.InvariantCulture)).ToArray();
    static string Key(int r, int s) => r + "," + s;
    static string Key(JsonElement x) { int[] a = Ints(x.GetProperty("blocks")); Require(a.Length == 2, "Not two blocks"); return Key(a[0], a[1]); }
    static void EqualInts(IEnumerable<int> actual, JsonElement expected, string name)
    { Require(actual.SequenceEqual(Ints(expected)), name + " integer sequence mismatch"); }
    static void EqualMap<K>(SortedDictionary<K,long> actual, JsonElement expected, string name) where K : notnull
    {
        var wanted = expected.EnumerateObject().ToDictionary(x => x.Name, x => x.Value.GetInt64());
        Require(actual.Count == wanted.Count, name + " map size mismatch");
        foreach (var pair in actual) Require(wanted.TryGetValue(pair.Key.ToString(), out long n) && n == pair.Value, name + " mismatch at " + pair.Key);
    }
    static long Choose(int n, int k)
    {
        if (n < k) return 0;
        BigInteger a = 1;
        for (int j = 1; j <= k; j++) a = a * (n - j + 1) / j;
        return checked((long)a);
    }
    static int Encode(int[] v) => v[0] + 5*v[1] + 25*v[2] + 125*v[3];
    static void BuildGroup()
    {
        Coordinates = new int[Q][];
        Plus = new int[Q][];
        Negative = new int[Q];
        for (int g = 0; g < Q; g++) Coordinates[g] = new[] { g%5, (g/5)%5, (g/25)%5, g/125 };
        for (int g = 0; g < Q; g++)
        {
            Negative[g] = Encode(Coordinates[g].Select(x => (5-x)%5).ToArray());
            Plus[g] = new int[Q];
            for (int h = 0; h < Q; h++)
            {
                int value = 0, place = 1;
                for (int k = 0; k < 4; k++, place *= 5) value += ((Coordinates[g][k] + Coordinates[h][k])%5)*place;
                Plus[g][h] = value;
            }
            Require(Plus[g][Negative[g]] == 0, "Group inverse mismatch");
        }
    }
    sealed class Distances
    {
        public byte[] D;
        public int ShortestNonemptyZero;
        public long Tuples;
    }
    // This retains all count vectors, including collisions. It is not a
    // recurrence on distances, Boolean reachability, or a producer state.
    static Distances EnumerateCounts(int[] values, int[] capacities)
    {
        var sums = new List<int> { 0 };
        var lengths = new List<int> { 0 };
        for (int p = 0; p < values.Length; p++)
        {
            var nextSums = new List<int>(sums.Count * (capacities[p] + 1));
            var nextLengths = new List<int>(nextSums.Capacity);
            for (int j = 0; j < sums.Count; j++)
            {
                int sum = sums[j];
                for (int k = 0; k <= capacities[p]; k++)
                {
                    nextSums.Add(sum); nextLengths.Add(lengths[j] + k);
                    sum = Plus[sum][values[p]];
                }
            }
            sums = nextSums; lengths = nextLengths;
        }
        byte[] distance = Enumerable.Repeat((byte)Inf, Q).ToArray();
        int nz = Inf;
        for (int j = 0; j < sums.Count; j++)
        {
            if (lengths[j] < distance[sums[j]]) distance[sums[j]] = (byte)lengths[j];
            if (sums[j] == 0 && lengths[j] > 0) nz = Math.Min(nz, lengths[j]);
        }
        long denominator = capacities.Aggregate(1L, (a,b) => a*(b+1));
        Require(sums.Count == denominator && distance[0] == 0, "Coefficient domain mismatch");
        CoefficientTuples += denominator;
        return new Distances { D = distance, ShortestNonemptyZero = nz, Tuples = denominator };
    }
    static Distances BuildCore(params int[] blocks)
    {
        int[] values = Basis.Concat(blocks).ToArray();
        Require(values.Distinct().Count() == values.Length && !values.Contains(0), "Invalid repeated core support");
        var result = EnumerateCounts(values, new[] {3,3,2,2}.Concat(blocks.Select(_ => 2)).ToArray());
        Require(result.ShortestNonemptyZero > Cutoff, "Unsafe generated core " + String.Join(",", blocks));
        if (blocks.Length == 2) { Require(result.Tuples == 1296, "Core coefficient count"); CoreTuples += result.Tuples; }
        return result;
    }
    static int Canonical(int g)
    {
        int[] v = Coordinates[g];
        int answer = g;
        for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++)
            answer = Math.Min(answer, Encode(new[] {v[a],v[1-a],v[2+b],v[3-b]}));
        return answer;
    }
    static List<int> DoubleCandidates(byte[] distance, int[] support, int start)
    {
        var used = new HashSet<int>(support);
        var result = new List<int>();
        for (int g = start; g < Q; g++)
        {
            BlockDomainTests++;
            if (used.Contains(g)) continue;
            if (distance[Negative[g]] + 1 > Cutoff && distance[Negative[Plus[g][g]]] + 2 > Cutoff) result.Add(g);
        }
        return result;
    }
    static int[] SingletonCandidates(byte[] distance, int[] support)
    {
        var used = new HashSet<int>(support);
        var result = new List<int>();
        for (int g = 0; g < Q; g++) if (distance[Negative[g]] + 1 > Cutoff && !used.Contains(g)) result.Add(g);
        return result.ToArray();
    }
    static bool[][] RebuildGraph(byte[] distance, int[] candidates, JsonElement record)
    {
        int n = candidates.Length;
        var graph = Enumerable.Range(0,n).Select(_ => new bool[n]).ToArray();
        var masks = Enumerable.Repeat(BigInteger.Zero, n).ToArray();
        for (int i = 0; i < n; i++) for (int j = i+1; j < n; j++)
        {
            PairTests++;
            if (distance[Negative[Plus[candidates[i]][candidates[j]]]] + 2 <= Cutoff) continue;
            graph[i][j] = graph[j][i] = true;
            masks[i] |= BigInteger.One << j;
            masks[j] |= BigInteger.One << i;
        }
        Require(masks.SequenceEqual(Bigs(record.GetProperty("adjacency_bitmasks"))), "Graph mismatch " + Key(record));
        Require(L(record,"pair_checks") == Choose(n,2), "Pair denominator mismatch");
        return graph;
    }
    // List passes rather than producer bitmask intersections.
    static List<BigInteger> GreedyClasses(bool[][] graph, IEnumerable<int> order)
    {
        var remaining = order.ToList();
        var classes = new List<BigInteger>();
        while (remaining.Count > 0)
        {
            var chosen = new List<int>();
            var next = new List<int>();
            BigInteger mask = BigInteger.Zero;
            foreach (int i in remaining)
            {
                if (chosen.Any(j => graph[i][j])) next.Add(i);
                else { chosen.Add(i); mask |= BigInteger.One << i; }
            }
            Require(chosen.Count > 0, "Empty greedy color class");
            classes.Add(mask); remaining = next;
        }
        return classes;
    }
    static List<BigInteger> Dsatur(bool[][] graph)
    {
        int n = graph.Length;
        int[] degree = graph.Select(row => row.Count(x => x)).ToArray();
        int[] saturation = new int[n], assigned = Enumerable.Repeat(-1,n).ToArray();
        bool[,] forbidden = new bool[n,n];
        var classes = new List<BigInteger>();
        for (int step = 0; step < n; step++)
        {
            int choice = -1;
            for (int i = 0; i < n; i++) if (assigned[i] < 0 &&
                (choice < 0 || saturation[i] > saturation[choice] ||
                 (saturation[i] == saturation[choice] && degree[i] > degree[choice]))) choice = i;
            int color = 0;
            while (forbidden[choice,color]) color++;
            if (color == classes.Count) classes.Add(BigInteger.Zero);
            classes[color] |= BigInteger.One << choice; assigned[choice] = color;
            for (int j = 0; j < n; j++) if (graph[choice][j] && assigned[j] < 0 && !forbidden[j,color])
            { forbidden[j,color] = true; saturation[j]++; }
        }
        return classes;
    }
    static int VerifyColorings(bool[][] graph, byte[] distance, int[] candidates, JsonElement row)
    {
        int n = candidates.Length;
        string method = "ascending_index_independent_classes";
        var colors = GreedyClasses(graph, Enumerable.Range(0,n));
        var attempts = new SortedDictionary<string,long>(); attempts[method] = colors.Count;
        if (colors.Count > 5)
        {
            var next = GreedyClasses(graph, Enumerable.Range(0,n).OrderByDescending(i => graph[i].Count(x => x)).ThenBy(i => i));
            attempts["descending_degree_independent_classes"] = next.Count;
            if (next.Count < colors.Count) { colors = next; method = "descending_degree_independent_classes"; }
        }
        if (colors.Count > 5)
        {
            var next = Dsatur(graph); attempts["dsatur_greedy"] = next.Count;
            if (next.Count < colors.Count) { colors = next; method = "dsatur_greedy"; }
        }
        EqualMap(attempts,row.GetProperty("attempted_color_counts"),"Attempted color counts");
        Require(S(row,"coloring_method") == method, "Coloring method mismatch");
        var provided = Bigs(row.GetProperty("proper_color_classes"));
        Require(colors.SequenceEqual(provided), "Color class replay mismatch " + Key(row));
        BigInteger all = (BigInteger.One << n)-1, union = BigInteger.Zero;
        foreach (BigInteger mask in provided)
        {
            Require(mask > 0 && (mask & ~all) == 0 && (mask & union) == 0, "Invalid or overlapping color class");
            union |= mask;
            for (int i = 0; i < n; i++) if ((mask & (BigInteger.One << i)) != 0)
                for (int j = i+1; j < n; j++) if ((mask & (BigInteger.One << j)) != 0)
                {
                    SameColorTests++;
                    Require(distance[Negative[Plus[candidates[i]][candidates[j]]]] + 2 <= Cutoff, "Monochromatic compatible pair");
                }
        }
        Require(union == all && I(row,"number_of_colors") == colors.Count, "Color vertex coverage mismatch");
        Require(B(row,"no_six_new_singletons_certified_by_this_coloring") == (colors.Count <= 5), "Color classification mismatch");
        Require(B(row,"graph_completed"), "Incomplete source graph");
        return colors.Count;
    }
    sealed class SearchResult
    {
        public long nodes { get; set; }
        public SortedDictionary<int,long> nodes_by_added { get; } = new();
        public SortedDictionary<int,long> leaves_by_added { get; } = new();
        public SortedDictionary<string,long> prune_counts { get; } = new();
        public string tree_trace_sha256 { get; set; }
        public long static_pair_rejections { get; set; }
    }
    static SearchResult Search(byte[] initial, int[] candidates, bool[][] graph)
    {
        var result = new SearchResult();
        var chosen = new List<int>();
        int width = (candidates.Length + 7)/8;
        Require(candidates.Length <= 256, "Trace index encoding overflow");
        using var hash = IncrementalHash.CreateHash(HashAlgorithmName.SHA256);
        void Marker(char c) { hash.AppendData(new[] { (byte)c }); }
        void Visit(byte[] current, List<int> available)
        {
            result.nodes++; int depth = chosen.Count;
            Inc(result.nodes_by_added,depth);
            var trace = new byte[1+width+depth]; trace[0] = (byte)depth;
            foreach (int i in available) trace[1+i/8] |= (byte)(1 << (i%8));
            for (int i = 0; i < depth; i++) trace[1+width+i] = (byte)chosen[i];
            hash.AppendData(trace);
            int need = 6-depth;
            if (need == 0)
            {
                Marker('W');
                throw new InvalidOperationException("SAFE SIX-SINGLETON WITNESS: " + String.Join(",", chosen.Select(i => candidates[i])));
            }
            if (available.Count < need)
            { Inc(result.prune_counts,"candidate_count"); Inc(result.leaves_by_added,depth); Marker('N'); return; }
            if (GreedyClasses(graph,available).Count < need)
            { Inc(result.prune_counts,"proper_coloring"); Inc(result.leaves_by_added,depth); Marker('C'); return; }
            bool child = false;
            for (int p = 0; p < available.Count; p++)
            {
                if (available.Count-p < need) { Inc(result.prune_counts,"remaining_candidate_count"); Marker('R'); break; }
                int i = available[p], g = candidates[i];
                Require(current[Negative[g]] + 1 > Cutoff, "Unsafe DFS chosen vertex");
                // Separate source and target arrays prevent reusing the new position.
                byte[] updated = (byte[])current.Clone();
                for (int h = 0; h < Q; h++)
                {
                    int destination = Plus[h][g], length = current[h]+1;
                    if (length < updated[destination]) updated[destination] = (byte)length;
                }
                var following = new List<int>();
                for (int q = p+1; q < available.Count; q++)
                {
                    int j = available[q];
                    if (!graph[i][j]) { result.static_pair_rejections++; continue; }
                    if (updated[Negative[candidates[j]]] + 1 > Cutoff) following.Add(j);
                    else Inc(result.prune_counts,"dynamic_short_zero");
                }
                chosen.Add(i); child = true; Visit(updated,following); chosen.RemoveAt(chosen.Count-1);
            }
            if (!child) Inc(result.leaves_by_added,depth);
        }
        Visit(initial,Enumerable.Range(0,candidates.Length).ToList());
        result.tree_trace_sha256 = Convert.ToHexString(hash.GetHashAndReset()).ToLowerInvariant();
        return result;
    }
    static void CompareSearch(SearchResult result, JsonElement record)
    {
        string key = Key(record);
        Require(B(record,"completed_exhaustively") && B(record,"decision_complete") && !B(record,"time_limit_reached"), "Incomplete DFS record " + key);
        Require(record.GetProperty("witness_added_values").ValueKind == JsonValueKind.Null, "Producer witness " + key);
        Require(L(record,"nodes") == result.nodes, "DFS node count " + key);
        EqualMap(result.nodes_by_added,record.GetProperty("nodes_by_added"),"DFS levels " + key);
        EqualMap(result.leaves_by_added,record.GetProperty("leaves_by_added"),"DFS leaves " + key);
        EqualMap(result.prune_counts,record.GetProperty("prune_counts"),"DFS pruning " + key);
        Require(S(record,"tree_trace_sha256") == result.tree_trace_sha256, "DFS full trace " + key);
        Nodes += result.nodes;
        StaticEdgeRejects += result.static_pair_rejections;
        foreach (var pair in result.nodes_by_added) Inc(TotalLevels,pair.Key,pair.Value);
        foreach (var pair in result.leaves_by_added) Inc(TotalLeaves,pair.Key,pair.Value);
        foreach (var pair in result.prune_counts) Inc(TotalPrunes,pair.Key,pair.Value);
        if (result.prune_counts.TryGetValue("dynamic_short_zero",out long n)) DynamicRejects += n;
    }
    static Dictionary<string,JsonElement> UniqueRows(IEnumerable<JsonElement> rows, string type)
    {
        var result = new Dictionary<string,JsonElement>();
        foreach (var row in rows.Where(x => S(x,"type") == type)) Require(result.TryAdd(Key(row),row), "Duplicate record " + Key(row));
        return result;
    }
    static object BindSnapshot(string source, string snapshot, string expectedSnapshotHash)
    {
        Require(Sha(PathAt(snapshot)) == expectedSnapshotHash, "Dependency snapshot hash " + snapshot);
        string[] actual = File.ReadAllLines(PathAt(source),Encoding.UTF8), reference = File.ReadAllLines(PathAt(snapshot),Encoding.UTF8);
        Require(actual.Length == reference.Length, "Dependency line count changed " + source);
        var differences = new List<int>();
        for (int i = 0; i < actual.Length; i++) if (actual[i] != reference[i]) differences.Add(i+1);
        Require(differences.All(i => i == 3), "Dependency mathematics changed " + source);
        return new { source, snapshot, current_sha256 = Sha(PathAt(source)), audited_snapshot_sha256 = expectedSnapshotHash, changed_lines = differences };
    }
    static void CheckReportedHashes(JsonElement report)
    {
        foreach (var entry in report.GetProperty("input_sha256").EnumerateObject())
            Require(Sha(PathAt(entry.Name.Replace('\\','/'))) == entry.Value.GetString(), "Recorded input hash mismatch: " + entry.Name);
    }
    static object BindH12(int r, int s, int functional, JsonElement h12, Dictionary<string,JsonElement> profiles)
    {
        int[] sequence = BaseSequence.Concat(new[] {r,r,s,s}).ToArray();
        bool Inside(int g) => Coordinates[g].Zip(Coordinates[functional], (x,y) => x*y).Sum()%5 == 0;
        int[] inside = sequence.Where(Inside).ToArray(), outside = sequence.Where(g => !Inside(g)).ToArray();
        Require(inside.Length == 12 && outside.Length == 2 && outside[0] == outside[1], "H12 actual positions");
        EqualInts(inside,h12.GetProperty("inside_sequence"),"H12 inside positions");
        Require(I(h12,"outside_double_value") == outside[0], "H12 outside double");
        EqualInts(new[] {3,3,2,2,2},h12.GetProperty("inside_multiplicity_profile"),"H12 multiplicities");
        Require(Inside(1) && Inside(5), "A triple outside H12");
        int[] doubles = new[] {25,125,r,s}.Where(Inside).ToArray();
        Require(doubles.Length == 3, "H12 doubles");
        int basisDouble = doubles.First(g => Coordinates[g][2] != 0 || Coordinates[g][3] != 0);
        int[] map = Enumerable.Repeat(-1,Q).ToArray();
        for (int a = 0; a < 5; a++) for (int b = 0; b < 5; b++) for (int c = 0; c < 5; c++)
        {
            int g = a+5*b;
            for (int k = 0; k < c; k++) g = Plus[g][basisDouble];
            Require(map[g] == -1, "H12 basis not independent");
            map[g] = 25*a + 5*b + c; // Explicit external-certificate big-endian code.
        }
        Require(Enumerable.Range(0,Q).All(g => (map[g] >= 0) == Inside(g)), "H12 basis does not cover hyperplane");
        int[] extras = doubles.Where(g => g != basisDouble).Select(g => map[g]).OrderBy(g => g).ToArray();
        Require(profiles.TryGetValue(Key(extras[0],extras[1]), out JsonElement certified), "H12 missing from certified 75-pair domain");
        var local = EnumerateCounts(new[] {1,5,basisDouble}.Concat(doubles.Where(g => g != basisDouble)).ToArray(), new[] {3,3,2,2,2});
        Require(local.Tuples == 432 && local.ShortestNonemptyZero == Inf, "H12 is not zero-sum-free");
        int[] mappedDistances = new int[125];
        for (int g = 0; g < Q; g++) if (Inside(g)) mappedDistances[map[g]] = local.D[g];
        EqualInts(mappedDistances,certified.GetProperty("distances_by_target_code"),"H12 certified distances");
        foreach (var condition in certified.GetProperty("conditions").EnumerateObject()) Require(condition.Value.GetBoolean(), "H12 certified condition failure");
        int total = 0; foreach (int g in inside) total = Plus[total][g];
        Require(mappedDistances.All(x => x < Inf) && mappedDistances[map[total]] == 12, "H12 coverage/total");
        Require(Enumerable.Range(0,125).All(g => g == map[total] || mappedDistances[g] <= 10), "H12 unique exception");
        Require(mappedDistances.Count(x => x >= 10) <= 3 && mappedDistances.Count(x => x >= 9) <= 5, "H12 exception sizes");
        return new { blocks = new[] {r,s}, functional, basis_values = new[] {1,5,basisDouble}, outside_double = outside[0], certified_pair = extras, distances = mappedDistances };
    }
    public static void Run(string runDirectory)
    {
        Root = Path.GetFullPath(runDirectory).TrimEnd(Path.DirectorySeparatorChar,Path.AltDirectorySeparatorChar);
        Require(String.Equals(Root.Replace('\\','/'),"C:/game/gameproject/showa100/math/2026-09-04_zhao_attack",StringComparison.OrdinalIgnoreCase),"Unexpected working directory");
        string summaryPath = PathAt("evidence/verify_two_extensions_fresh.json");
        File.WriteAllText(summaryPath,JsonSerializer.Serialize(new { status = "INCOMPLETE_RUNNING", scope = "a=2,b=4 local endpoint class only" },Pretty),Encoding.UTF8);
        var watch = Stopwatch.StartNew();
        try
        {
            string[] inputFiles = {
                "proofs/two_triples_four_doubles.md", "evidence/finite_two_triples_probe.json", "evidence/finite_two_triples_probe_cores.jsonl",
                "evidence/finite_two_triples_residual.json", "evidence/finite_two_triples_residual_hyperplanes.jsonl", "evidence/finite_two_triples_residual_cores.jsonl",
                "evidence/atom_3322_m13_blocks.jsonl", "scripts/finite_two_triples_probe.py", "scripts/finite_two_triples_residual.py",
                "scripts/verify_finite_cores_fresh.py", "scripts/verify_finite_double_blocks.py", "scripts/atom_double_blocks.ps1",
                "proofs/hyperplane_core_A_support8.md", "proofs/verify_support8_fresh.md", "evidence/verify_support8_fresh.json",
                "proofs/one_triple_six_doubles.md", "proofs/verify_single_extensions_fresh.md", "evidence/verify_single_extensions_audited_snapshot.md",
                "proofs/certified_reduction.md", "proofs/verify_combined_scope_fresh.md", "evidence/verify_combined_certified_reduction_final_snapshot.md"
            };
            var hashes = inputFiles.ToDictionary(x => x,x => Sha(PathAt(x)));
            File.Copy(PathAt("proofs/two_triples_four_doubles.md"),PathAt("evidence/verify_two_extensions_audited_snapshot.md"),true);
            JsonElement probe = ReadJson("evidence/finite_two_triples_probe.json"), residual = ReadJson("evidence/finite_two_triples_residual.json");
            CheckReportedHashes(probe); CheckReportedHashes(residual);
            Require(hashes["evidence/finite_two_triples_probe_cores.jsonl"] == S(probe,"certificate_sha256"),"Probe certificate hash");
            Require(hashes["evidence/finite_two_triples_residual_hyperplanes.jsonl"] == S(residual,"hyperplane_profiles_sha256"),"Hyperplane certificate hash");
            Require(hashes["evidence/finite_two_triples_residual_cores.jsonl"] == S(residual,"direct_core_records_sha256"),"Direct certificate hash");
            var probeLines = ReadLines("evidence/finite_two_triples_probe_cores.jsonl");
            var coreRows = probeLines.Where(x => S(x,"type") == "core_result").ToList();
            Require(coreRows.Count == 8461 && UniqueRows(coreRows,"core_result").Count == 8461,"Probe record denominator");
            var hyperLines = ReadLines("evidence/finite_two_triples_residual_hyperplanes.jsonl");
            var hyperRows = UniqueRows(hyperLines,"hyperplane_profile");
            var directLines = ReadLines("evidence/finite_two_triples_residual_cores.jsonl");
            var directRows = UniqueRows(directLines,"direct_core_result");
            var directSummaryRows = residual.GetProperty("direct_root_results").EnumerateArray().ToDictionary(Key,x => x);
            Require(hyperRows.Count == 1022 && directRows.Count == 958 && directSummaryRows.Count == 958,"Residual denominators");
            var originalTree = ReadLines("evidence/atom_3322_m13_blocks.jsonl");
            var originalRoots = originalTree.Where(x => S(x,"type") == "root").ToDictionary(x => I(x,"root"), x => x);
            Require(originalRoots.Count == 122,"Original tree root denominator");
            JsonElement support8 = ReadJson("evidence/verify_support8_fresh.json");
            CheckReportedHashes(support8);
            Require(I(support8,"zero_free_cores") == 75,"H12 external finite scope");
            var supportProfiles = support8.GetProperty("rows").EnumerateArray().ToDictionary(x => Key(I(x,"u"),I(x,"v")), x => x);
            Require(supportProfiles.Count == 75,"Duplicate external H12 profiles");
            foreach (string proof in new[] {"proofs/verify_support8_fresh.md","proofs/verify_single_extensions_fresh.md","proofs/verify_combined_scope_fresh.md"})
                Require(File.ReadAllText(PathAt(proof),Encoding.UTF8).Contains("STATUS: CORRECT"),"Dependency not certified " + proof);
            var bindings = new[] {
                BindSnapshot("proofs/certified_reduction.md","evidence/verify_combined_certified_reduction_final_snapshot.md","83c2666de5277dc60ed1e41ab59bd517b58b54efcf34e04a5777a8f12d66fdb1"),
                BindSnapshot("proofs/one_triple_six_doubles.md","evidence/verify_single_extensions_audited_snapshot.md","de499581b70dad27fc915420f0627b71ba006e2fc83678773d7668f4efc910c3")
            };
            BuildGroup();
            var baseState = BuildCore();
            var initial = DoubleCandidates(baseState.D,Basis,0);
            EqualInts(initial,originalTree[0].GetProperty("initial_safe_candidates"),"Initial full safe double pool");
            Require(initial.Count == 371,"Initial double candidate count");
            int[] roots = initial.Select(Canonical).Distinct().OrderBy(x => x).ToArray();
            Require(roots.Length == 122 && roots.All(initial.Contains),"Canonical first-root coverage");
            EqualInts(roots,originalTree[0].GetProperty("canonical_roots"),"Original root set");
            EqualInts(roots,probe.GetProperty("canonical_roots"),"Probe root set");
            EqualInts(roots,probeLines[0].GetProperty("canonical_roots"),"Probe metadata roots");
            int[] functionals = Enumerable.Range(1,Q-1).Where(g => Coordinates[g].First(x => x != 0) == 1).ToArray();
            Require(functionals.Length == 156,"Hyperplane projective denominator");
            var hyperMasks = new HashSet<BigInteger>();
            var insideTable = new bool[156][];
            for (int j = 0; j < functionals.Length; j++)
            {
                EqualInts(Coordinates[functionals[j]],hyperLines[0].GetProperty("hyperplane_functionals")[j],"Hyperplane normal ordering");
                insideTable[j] = new bool[Q]; BigInteger mask = BigInteger.Zero;
                for (int g = 0; g < Q; g++)
                {
                    insideTable[j][g] = Coordinates[g].Zip(Coordinates[functionals[j]],(a,b) => a*b).Sum()%5 == 0;
                    if (insideTable[j][g]) mask |= BigInteger.One << g;
                }
                Require(insideTable[j].Count(x => x) == 125 && hyperMasks.Add(mask),"Duplicate or wrong-sized hyperplane");
            }
            var rootsEvidence = new List<object>(); var h12Bindings = new List<object>();
            var residualKeys = new List<int[]>(); var h12Keys = new List<int[]>(); var directKeys = new List<int[]>();
            var generatedByRoot = new SortedDictionary<int,long>(); var directByRoot = new SortedDictionary<int,long>();
            int coreIndex = 0, colored = 0, length16 = 0, residualIndex = 0, directIndex = 0;
            long denominator6 = 0, denominator7 = 0, directDenominator6 = 0, directDenominator7 = 0;
            var coreNonemptyZeroHistogram = new SortedDictionary<int,long>();
            using (var coresOut = new StreamWriter(PathAt("evidence/verify_two_extensions_cores.jsonl"),false,new UTF8Encoding(false)))
            using (var searchesOut = new StreamWriter(PathAt("evidence/verify_two_extensions_searches.jsonl"),false,new UTF8Encoding(false)))
            {
                foreach (int r in roots)
                {
                    var state12 = BuildCore(r);
                    var seconds = DoubleCandidates(state12.D,Basis.Concat(new[] {r}).ToArray(),r+1);
                    var lengths = new SortedDictionary<int,long>(); Inc(lengths,12);
                    var leaves = new SortedDictionary<int,long>();
                    if (seconds.Count == 0) Inc(leaves,12);
                    foreach (int s in seconds)
                    {
                        string key = Key(r,s); var state14 = BuildCore(r,s); var row = coreRows[coreIndex];
                        Require(Key(row) == key && I(row,"core_index") == coreIndex && I(row,"root") == r,"Complete ordered length14 coverage " + key);
                        Inc(lengths,14); Inc(generatedByRoot,r); Inc(coreNonemptyZeroHistogram,state14.ShortestNonemptyZero);
                        var support = Basis.Concat(new[] {r,s}).ToArray();
                        int[] candidates = SingletonCandidates(state14.D,support);
                        EqualInts(candidates,row.GetProperty("outside_safe_values"),"Full 625-domain singleton pool " + key);
                        Require(I(row,"candidate_count") == candidates.Length,"Candidate count field");
                        long six = Choose(candidates.Length,6), seven = Choose(candidates.Length,7);
                        Require(L(row,"six_subset_count") == six && L(row,"seven_subset_count") == seven,"Core subset denominator");
                        denominator6 += six; denominator7 += seven; Inc(CandidateHistogram,candidates.Length);
                        bool[][] graph = RebuildGraph(state14.D,candidates,row);
                        int colorCount = VerifyColorings(graph,state14.D,candidates,row); Inc(ColorHistogram,colorCount);
                        string classification;
                        if (colorCount <= 5) { colored++; classification = "PROPER_COLORING_AT_MOST_FIVE"; Require(!hyperRows.ContainsKey(key) && !directRows.ContainsKey(key),"Class overlap"); }
                        else
                        {
                            residualKeys.Add(new[] {r,s});
                            Require(hyperRows.TryGetValue(key,out JsonElement hrow),"Missing hyperplane classification " + key);
                            Require(I(hrow,"residual_index") == residualIndex++ && I(hrow,"root") == r && I(hrow,"candidate_count") == candidates.Length,"Hyperplane record identity");
                            int[] sequence = BaseSequence.Concat(new[] {r,r,s,s}).ToArray();
                            int[] counts = insideTable.Select(inside => sequence.Count(g => inside[g])).ToArray();
                            EqualInts(counts,hrow.GetProperty("all_156_item_counts"),"All 156 weighted hyperplane intersections " + key);
                            Require(counts.Max() <= 12 && I(hrow,"maximum_items_in_hyperplane") == counts.Max(),"Hyperplane maximum");
                            int[] hindices = Enumerable.Range(0,156).Where(j => counts[j] == 12).ToArray();
                            Inc(HyperplaneMaxHistogram,counts.Max()); Inc(H12CountHistogram,hindices.Length);
                            Require(hrow.GetProperty("h12_hyperplanes").GetArrayLength() == hindices.Length,"H12 listing cardinality");
                            for (int j = 0; j < hindices.Length; j++)
                            {
                                int functional = functionals[hindices[j]]; JsonElement h = hrow.GetProperty("h12_hyperplanes")[j];
                                Require(I(h,"functional_encoded") == functional,"H12 functional code");
                                EqualInts(Coordinates[functional],h.GetProperty("functional_coordinates"),"H12 functional coordinates");
                                h12Bindings.Add(BindH12(r,s,functional,h,supportProfiles));
                            }
                            if (hindices.Length > 0)
                            {
                                h12Keys.Add(new[] {r,s}); classification = "H12_BOUND_TO_EXTERNAL_CORRECT_LEMMA";
                                Require(!directRows.ContainsKey(key) && S(hrow,"classification") == "H12_PENDING_EXTERNAL_LEMMA","H12 classification overlap");
                            }
                            else
                            {
                                directKeys.Add(new[] {r,s}); classification = "EXHAUSTIVE_SIX_SINGLETON_SEARCH";
                                Require(S(hrow,"classification") == "DIRECT_EXACT_EXTENSION_SEARCH" && directRows.TryGetValue(key,out _),"Direct classification");
                                JsonElement drow = directRows[key];
                                Require(I(drow,"direct_index") == directIndex++ && I(drow,"root") == r && I(drow,"candidate_count") == candidates.Length && L(drow,"six_subset_count") == six,"Direct identity");
                                SearchResult result = Search(state14.D,candidates,graph);
                                CompareSearch(result,drow);
                                JsonElement srow = directSummaryRows[key];
                                Require(result.nodes == L(srow,"nodes") && result.tree_trace_sha256 == S(srow,"tree_trace_sha256"),"Summary DFS binding");
                                EqualMap(result.nodes_by_added,srow.GetProperty("nodes_by_added"),"Summary DFS levels");
                                EqualMap(result.leaves_by_added,srow.GetProperty("leaves_by_added"),"Summary DFS leaves");
                                EqualMap(result.prune_counts,srow.GetProperty("prune_counts"),"Summary DFS pruning");
                                searchesOut.WriteLine(JsonSerializer.Serialize(new { blocks = new[] {r,s}, candidates, result, status = "COMPLETE_NO_SAFE_SIX_EXTENSION" }));
                                Inc(directByRoot,r); directDenominator6 += six; directDenominator7 += seven;
                            }
                        }
                        // Rebuild every next double-block node as well, so the
                        // length14 set is bound to the original full 3322 tree.
                        var thirds = DoubleCandidates(state14.D,support,s+1);
                        if (thirds.Count == 0) Inc(leaves,14);
                        foreach (int t in thirds)
                        {
                            var state16 = BuildCore(r,s,t); Inc(lengths,16); Inc(leaves,16); length16++;
                            Require(DoubleCandidates(state16.D,support.Concat(new[] {t}).ToArray(),t+1).Count == 0,"Unexpected length18 core");
                        }
                        coresOut.WriteLine(JsonSerializer.Serialize(new { core_index = coreIndex, blocks = new[] {r,s}, minimum_distances = state14.D.Select(x => (int)x).ToArray(), minimum_nonempty_zero = state14.ShortestNonemptyZero, bounded_coefficient_tuples = state14.Tuples, outside_safe_values = candidates, proper_color_count = colorCount, classification, safe_next_double_blocks = thirds }));
                        coreIndex++;
                    }
                    JsonElement original = originalRoots[r];
                    EqualMap(lengths,original.GetProperty("nodes_by_length"),"Original full tree levels root " + r);
                    EqualMap(leaves,original.GetProperty("leaves_by_length"),"Original full tree leaves root " + r);
                    Require(B(original,"completed_exhaustively") && L(original,"nodes") == lengths.Values.Sum() && I(original,"terminal_count") == 0,"Original full root completion");
                    Require(I(original,"max_reached_length") == lengths.Keys.Max(),"Original max depth");
                    rootsEvidence.Add(new { root = r, nodes_by_length = lengths, leaves_by_length = leaves });
                    if (rootsEvidence.Count%20 == 0) Console.WriteLine("Independent replay: roots=" + rootsEvidence.Count + " cores14=" + coreIndex + " residual_nodes=" + Nodes);
                }
            }
            Require(coreIndex == 8461 && length16 == 15684 && roots.Length+coreIndex+length16 == 24267,"Full tree denominator");
            Require(colored == 7439 && residualKeys.Count == 1022 && h12Keys.Count == 64 && directKeys.Count == 958,"Disjoint partition denominator");
            Require(Nodes == 356118 && Nodes == L(residual,"direct_nodes"),"Complete DFS node denominator");
            EqualMap(generatedByRoot,probe.GetProperty("generated_cores_by_root"),"Per-root length14 counts");
            EqualMap(generatedByRoot,probe.GetProperty("graph_completed_by_root"),"Per-root graph counts");
            EqualMap(directByRoot,residual.GetProperty("direct_completed_by_original_root"),"Per-root direct completions");
            EqualMap(CandidateHistogram,probe.GetProperty("outside_candidate_count_distribution"),"Candidate distribution");
            EqualMap(ColorHistogram,probe.GetProperty("best_color_count_distribution"),"Color count distribution");
            EqualMap(HyperplaneMaxHistogram,residual.GetProperty("maximum_hyperplane_item_distribution"),"Hyperplane maximum distribution");
            EqualMap(H12CountHistogram,residual.GetProperty("h12_hyperplanes_per_core_distribution"),"H12 count distribution");
            void EqualKeys(List<int[]> keys, JsonElement expected, string label)
            {
                Require(expected.GetArrayLength() == keys.Count,label + " denominator");
                for (int j = 0; j < keys.Count; j++) EqualInts(keys[j],expected[j],label + " ordered keys");
            }
            EqualKeys(residualKeys,probe.GetProperty("unresolved_core_keys"),"All coloring residuals");
            EqualKeys(h12Keys,residual.GetProperty("h12_core_keys"),"All H12 cores");
            EqualKeys(directKeys,residual.GetProperty("direct_expected_core_keys"),"All direct-search cores");
            Require(denominator6 == L(probe,"six_subset_denominator") && denominator7 == L(probe,"seven_subset_denominator"),"Global static combination denominators");
            Require(directDenominator6 == L(residual,"direct_six_subset_denominator") && directDenominator7 == L(residual,"direct_seven_subset_denominator"),"Direct static combination denominators");
            Require(PairTests == L(probe,"total_pair_checks") && PairTests == 14520820,"Pair checks denominator");
            Require(!B(probe,"time_limit_reached") && !B(residual,"time_limit_reached") && I(probe,"unprocessed_cores") == 0 && residual.GetProperty("unprocessed_core_keys").GetArrayLength() == 0 && residual.GetProperty("uncompleted_direct_core_keys").GetArrayLength() == 0,"Source incomplete status");
            foreach (var pair in hashes) Require(Sha(PathAt(pair.Key)) == pair.Value,"Input changed during independent replay: " + pair.Key);
            File.WriteAllText(PathAt("evidence/verify_two_extensions_h12_bindings.json"),JsonSerializer.Serialize(new { status = "ALL_64_BOUND_TO_CERTIFIED_75_TYPE_DOMAIN", rows = h12Bindings, external_report_sha256 = hashes["proofs/verify_support8_fresh.md"], external_evidence_sha256 = hashes["evidence/verify_support8_fresh.json"] },Pretty),new UTF8Encoding(false));
            var output = new {
                status = "INDEPENDENT_COMPLETE_FINITE_REPLAY_PASSED",
                scope = "a=2,b=4 A21/B20 endpoint class only; H12 abstract lemma and prior a,b bounds are explicit external certified dependencies",
                method = "Full bounded-coefficient core enumeration; full-domain scalar minimum distances; array/list graphs and DFS; no producer imports",
                group_size = Q, cutoff = Cutoff, initial_safe_double_candidates = initial.Count,
                canonical_roots = roots, length12_nodes = roots.Length, length14_nodes = coreIndex, length16_nodes = length16,
                full_original_tree_nodes = roots.Length+coreIndex+length16, no_length18_nodes = true,
                core_coefficient_tuples = CoreTuples, all_coefficient_tuples_including_roots_and_length16 = CoefficientTuples,
                block_candidate_domain_tests = BlockDomainTests, full_core_target_distances = coreIndex*Q,
                full_core_singleton_domain_tests = coreIndex*Q, pair_tests = PairTests, same_color_distance_tests = SameColorTests,
                colored_cores = colored, residual_cores = residualKeys.Count, all_hyperplane_counts_checked = residualKeys.Count*156,
                h12_cores = h12Keys.Count, h12_distance_bindings_checked = h12Bindings.Count*125,
                direct_search_cores = directKeys.Count, direct_nodes = Nodes, direct_levels = TotalLevels, direct_leaves = TotalLeaves,
                direct_prunes = TotalPrunes, static_pair_rejections = StaticEdgeRejects, dynamic_short_zero_rejections = DynamicRejects,
                all_958_trace_sha256_match = true, safe_six_singleton_extensions = 0,
                six_subset_denominator = denominator6, seven_subset_denominator = denominator7,
                direct_six_subset_denominator = directDenominator6, direct_seven_subset_denominator = directDenominator7,
                candidate_histogram = CandidateHistogram, color_histogram = ColorHistogram,
                hyperplane_max_histogram = HyperplaneMaxHistogram, h12_count_histogram = H12CountHistogram,
                core_minimum_nonempty_zero_histogram = coreNonemptyZeroHistogram,
                original_full_root_records = rootsEvidence, external_snapshot_bindings = bindings,
                dependency_report_hashes = new { support8 = hashes["proofs/verify_support8_fresh.md"], single_extensions = hashes["proofs/verify_single_extensions_fresh.md"], combined_scope = hashes["proofs/verify_combined_scope_fresh.md"] },
                input_sha256 = hashes, verifier_sha256 = Sha(PathAt("scripts/verify_two_extensions_fresh.cs")),
                evidence_sha256 = new { cores = Sha(PathAt("evidence/verify_two_extensions_cores.jsonl")), searches = Sha(PathAt("evidence/verify_two_extensions_searches.jsonl")), h12_bindings = Sha(PathAt("evidence/verify_two_extensions_h12_bindings.json")), audited_snapshot = Sha(PathAt("evidence/verify_two_extensions_audited_snapshot.md")) },
                dotnet_version = Environment.Version.ToString(), elapsed_seconds = watch.Elapsed.TotalSeconds,
                input_files_unchanged_during_run = true, lean_status = "NOT_LEAN_FORMALIZED"
            };
            File.WriteAllText(summaryPath,JsonSerializer.Serialize(output,Pretty),new UTF8Encoding(false));
            Console.WriteLine(JsonSerializer.Serialize(new { status = output.status, length14_nodes = coreIndex, colored, h12 = h12Keys.Count, direct = directKeys.Count, nodes = Nodes, elapsed_seconds = watch.Elapsed.TotalSeconds }));
        }
        catch (Exception exception)
        {
            File.WriteAllText(summaryPath,JsonSerializer.Serialize(new { status = "INCOMPLETE_OR_CRITICAL_GAP", error = exception.ToString(), elapsed_seconds = watch.Elapsed.TotalSeconds },Pretty),new UTF8Encoding(false));
            throw;
        }
    }
}
