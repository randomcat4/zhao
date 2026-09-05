param([double]$Seconds=30)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new()
$starRoot=Split-Path -Parent $PSScriptRoot
Add-Type -Path (Join-Path $PSScriptRoot 'continue_atom16_star_addendum_d3_fixed.cs')
[ContinueAtom16StarAddendumD3Fixed]::Run($starRoot,$Seconds)
