param([string]$OutputFile = '')
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$auditDirectory = Split-Path -Parent $PSScriptRoot
if (-not $OutputFile) {
    $OutputFile = Join-Path $auditDirectory 'evidence/verify_single_extensions_fresh.json'
}
$auditSource = Join-Path $PSScriptRoot 'verify_single_extensions_fresh.cs'
Add-Type -Path $auditSource
[SingleExtensionsFreshAudit]::Run($auditDirectory, [System.IO.Path]::GetFullPath($OutputFile))
