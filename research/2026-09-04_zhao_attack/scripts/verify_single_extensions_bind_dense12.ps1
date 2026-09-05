$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$auditDirectory = Split-Path -Parent $PSScriptRoot
function Read-AuditJson([string]$relative) {
    return Get-Content -LiteralPath (Join-Path $auditDirectory $relative) -Encoding UTF8 -Raw | ConvertFrom-Json
}
function Get-AuditHash([string]$relative) {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $auditDirectory $relative)).Hash.ToLowerInvariant()
}
function Assert-Audit([bool]$condition, [string]$message) {
    if (-not $condition) { throw $message }
}
function Core-Key($blocks) { return ($blocks -join ',') }

$mainAudit = Read-AuditJson 'evidence/verify_single_extensions_fresh.json'
$denseAudit = Read-AuditJson 'evidence/verify_dense12_fresh.json'
$classification = Read-AuditJson 'evidence/atom_127_classification.json'
$denseReport = Get-Content -LiteralPath (Join-Path $auditDirectory 'proofs/verify_dense12_fresh.md') -Encoding UTF8 -Raw
Assert-Audit ($mainAudit.status -eq 'CORRECT_FOR_COMPLETE_CORE_COVERAGE_AND_107647_SMALL_CORES') 'Main full-domain audit not complete.'
Assert-Audit ($denseAudit.status -eq 'CORRECT_FOR_ASSIGNED_LOCAL_CLAIMS') 'Dense12 audit not certified.'
Assert-Audit ($denseReport -match '(?m)^STATUS: CORRECT\r?$') 'Dense12 mathematical report missing CORRECT verdict.'
foreach ($property in $mainAudit.input_sha256.PSObject.Properties) {
    Assert-Audit ((Get-AuditHash $property.Name) -eq $property.Value) ('Changed main evidence: ' + $property.Name)
}
Assert-Audit ((Get-AuditHash 'scripts/verify_single_extensions_fresh.cs') -eq $mainAudit.verifier_sha256) 'Changed main verifier.'
Assert-Audit ((Get-AuditHash 'scripts/verify_single_extensions_fresh.ps1') -eq $mainAudit.runner_sha256) 'Changed main runner.'
# Bind only the two dense12 inputs used by this local theorem. The separate
# eighteen-term lower-bound construction in that report is not a dependency.
Assert-Audit ((Get-AuditHash 'evidence/atom_127_classification.json') -eq $denseAudit.inputsSha256.'evidence/atom_127_classification.json') 'Changed classification input.'
$auditedSnapshot = 'evidence/dense12_audited_snapshot.md'
Assert-Audit ((Get-AuditHash $auditedSnapshot) -eq $denseAudit.inputsSha256.'proofs/hyperplane_dense12.md') 'Dense12 audited snapshot does not match the original audit hash.'
$snapshotLines = [System.IO.File]::ReadAllLines((Join-Path $auditDirectory $auditedSnapshot), [System.Text.Encoding]::UTF8)
$currentLines = [System.IO.File]::ReadAllLines((Join-Path $auditDirectory 'proofs/hyperplane_dense12.md'), [System.Text.Encoding]::UTF8)
Assert-Audit ($snapshotLines.Length -eq $currentLines.Length) 'Changed dense12 mathematical line count.'
$changedLines = @()
for ($index = 0; $index -lt $snapshotLines.Length; $index++) {
    if ($snapshotLines[$index] -cne $currentLines[$index]) { $changedLines += $index + 1 }
}
Assert-Audit ($changedLines.Count -eq 1 -and $changedLines[0] -eq 3) 'Dense12 changes extend beyond the status sentence.'
Assert-Audit ($snapshotLines[2] -ceq '状态：候选完整证明，提交新上下文验缝。此命题是严格的局部类结论，不是完整端点 A/B。') 'Unexpected original status sentence.'
Assert-Audit ($currentLines[2] -ceq '状态：新上下文审计 CORRECT，见 verify_dense12_fresh.md。此命题是严格的局部类结论，不是完整端点 A/B。') 'Unexpected current status sentence.'
Assert-Audit ((Get-AuditHash 'scripts/verify_dense12_fresh.js') -eq $denseAudit.verifierSha256) 'Changed dense12 verifier.'
Assert-Audit ($mainAudit.exceptional_cores.Count -eq 9 -and $classification.records.Count -eq 9 -and $denseAudit.cores.Count -eq 9) 'Nine-core denominator mismatch.'
$mainKeys = @($mainAudit.exceptional_cores | ForEach-Object { Core-Key $_.blocks } | Sort-Object)
$classificationKeys = @($classification.records | ForEach-Object { Core-Key $_.blocks_encoded } | Sort-Object)
$denseKeys = @($denseAudit.cores | ForEach-Object { Core-Key $_.blocksEncoded } | Sort-Object)
Assert-Audit (($mainKeys | Select-Object -Unique).Count -eq 9) 'Duplicated exceptional core.'
Assert-Audit (($mainKeys -join ';') -eq ($classificationKeys -join ';')) 'Classification does not match the computed exceptional set.'
Assert-Audit (($mainKeys -join ';') -eq ($denseKeys -join ';')) 'Dense12 audit does not match the computed exceptional set.'

$bindings = @()
foreach ($entry in $mainAudit.exceptional_cores) {
    $key = Core-Key $entry.blocks
    $record = $classification.records | Where-Object { (Core-Key $_.blocks_encoded) -eq $key }
    $verified = $denseAudit.cores | Where-Object { (Core-Key $_.blocksEncoded) -eq $key }
    $expectedSupport = @(@(5, 25, 125) + @($entry.blocks) | Sort-Object)
    $suppliedSupport = @($record.support_h | ForEach-Object { 5 * $_[0] + 25 * $_[1] + 125 * $_[2] } | Sort-Object)
    $verifiedSupport = @($verified.support | ForEach-Object { 5 * $_[0] + 25 * $_[1] + 125 * $_[2] } | Sort-Object)
    Assert-Audit (($expectedSupport -join ',') -eq ($suppliedSupport -join ',')) ('Classification support mismatch: ' + $key)
    Assert-Audit (($expectedSupport -join ',') -eq ($verifiedSupport -join ',')) ('Verified support mismatch: ' + $key)
    Assert-Audit (@($record.h_multiplicities | Where-Object { $_ -ne 2 }).Count -eq 0 -and $record.h_multiplicities.Count -eq 6) 'Classification multiplicities are not six doubles.'
    Assert-Audit (@($verified.multiplicities | Where-Object { $_ -ne 2 }).Count -eq 0 -and $verified.multiplicities.Count -eq 6) 'Verified multiplicities are not six doubles.'
    Assert-Audit ($verified.positionSubsetsChecked -eq 4096 -and $verified.nonemptyZeroSumCount -eq 0) 'Dense12 zero-sum-free certificate failure.'
    Assert-Audit ($verified.distanceAtSigma -eq 12 -and $verified.maximumDistanceAwayFromSigma -eq 6) 'Dense12 covering certificate failure.'
    Assert-Audit ($verified.all125SuppliedWitnessesAndMinimaVerified -eq $true -and $verified.minimumDistances.Count -eq 125) 'Dense12 target denominator failure.'
    Assert-Audit (@($entry.blocks | Where-Object { $_ % 5 -ne 0 }).Count -eq 0) 'Exceptional block not in first-coordinate-zero hyperplane.'
    $bindings += [ordered]@{
        source_index = $entry.source_index
        blocks = $entry.blocks
        independently_computed_outside_candidate_count = $entry.candidate_count
        support_encoded_in_G = $expectedSupport
        multiplicities_in_H = $verified.multiplicities
        dense12_input_and_audit_exactly_matched = $true
    }
}

$boundPaths = @(
    'proofs/one_triple_six_doubles.md',
    'evidence/verify_single_extensions_audited_snapshot.md',
    'evidence/verify_single_extensions_fresh.json',
    'proofs/verify_dense12_fresh.md',
    'evidence/verify_dense12_fresh.json',
    'proofs/hyperplane_dense12.md',
    'evidence/dense12_audited_snapshot.md',
    'evidence/atom_127_classification.json',
    'proofs/certified_reduction.md'
)
$hashes = [ordered]@{}
foreach ($relative in $boundPaths) { $hashes[$relative] = Get-AuditHash $relative }
$binding = [ordered]@{
    status = 'COMPLETE_LOCAL_DEPENDENCY_BINDING'
    frozen_local_claim = 'An A21 or B20 bad sequence cannot have exactly one tripled value, six doubled values, and all other values distinct singletons.'
    audited_proof_snapshot = 'evidence/verify_single_extensions_audited_snapshot.md'
    complete_core_count = $mainAudit.length15_cores
    small_cores_independently_excluded = $mainAudit.all_small_cores
    exceptional_cores_excluded_by_bound_fresh_dense12_audit = $bindings
    dense12_original_audited_input = $auditedSnapshot
    dense12_current_text_change = [ordered]@{ changed_lines = $changedLines; old_status = $snapshotLines[2]; new_status = $currentLines[2]; mathematical_body_unchanged = $true }
    old_corollary_conditions = @('h <= 3', 'a <= 3', 'a+b <= 7', 'a >= 2 implies a+b <= 6', 'a=3 implies b <= 1')
    old_corollary_dependency = 'proofs/certified_reduction.md; accepted existing certified results, not re-proved by this audit'
    updated_a1_condition = 'b <= 5'
    A_minimum_support_by_a_0_1_2_3 = @(14, 14, 13, 14)
    B_minimum_support_by_a_0_1_2_3 = @(13, 13, 12, 13)
    input_sha256 = $hashes
    binder_sha256 = Get-AuditHash 'scripts/verify_single_extensions_bind_dense12.ps1'
}
$bindingPath = Join-Path $auditDirectory 'evidence/verify_single_extensions_fresh_binding.json'
$binding | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $bindingPath -Encoding UTF8
[ordered]@{ status = $binding.status; matched_cores = $bindings.Count; output = $bindingPath } | ConvertTo-Json -Compress
