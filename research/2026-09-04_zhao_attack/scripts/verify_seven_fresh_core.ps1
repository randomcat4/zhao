$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$verificationRoot = Split-Path -Parent $PSScriptRoot
Add-Type -Path (Join-Path $PSScriptRoot 'verify_seven_fresh_core.cs')
[VerifySevenFreshCore]::Run($verificationRoot)
