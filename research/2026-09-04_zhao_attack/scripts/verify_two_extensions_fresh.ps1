$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$taskRunDirectory = 'C:/game/gameproject/showa100/math/2026-09-04_zhao_attack'
Add-Type -Path (Join-Path $taskRunDirectory 'scripts/verify_two_extensions_fresh.cs')
[VerifyTwoExtensionsFresh]::Run($taskRunDirectory)
