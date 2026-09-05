param([int]$Seconds=60)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new()
$taskRoot=Split-Path -Parent $PSScriptRoot
$taskInput=Join-Path $taskRoot 'evidence\atom_2222_m13_blocks.jsonl'
$taskOriginal=Join-Path $PSScriptRoot 'atom_double_blocks.ps1'
$taskSource=Join-Path $PSScriptRoot 'seven_doubles_continue_probe.cs'
$taskRows=@(Get-Content -LiteralPath $taskInput -Encoding utf8 | ForEach-Object {$_ | ConvertFrom-Json})
$taskMeta=$taskRows[0]
$taskRoots=@($taskRows | Where-Object {$_.type -eq 'root'} | Sort-Object root)
if ($taskMeta.mode -ne '2222' -or $taskMeta.m -ne 13 -or $taskRoots.Count -ne 44 -or @($taskRoots | Where-Object {-not $_.completed_exhaustively}).Count -ne 0) {throw 'input mismatch'}
$taskOriginalHash=(Get-FileHash -LiteralPath $taskOriginal -Algorithm SHA256).Hash.ToLowerInvariant()
if($taskOriginalHash -ne $taskMeta.script_sha256){throw 'script hash mismatch'}
$taskInputHash=(Get-FileHash -LiteralPath $taskInput -Algorithm SHA256).Hash.ToLowerInvariant()
$taskProducerHash=(Get-FileHash -LiteralPath $taskSource -Algorithm SHA256).Hash.ToLowerInvariant()
Add-Type -Path $taskSource
[SevenDoublesContinueProbe]::Run((Join-Path $taskRoot 'evidence'),$Seconds,[int[]]$taskMeta.canonical_roots,[int[]]@($taskRoots | ForEach-Object {$_.nodes_by_length.'14'}),$taskInputHash,$taskOriginalHash,$taskProducerHash)
