param(
    [Parameter(Mandatory = $true)][string]$TvHost
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$py = Join-Path $repo 'tools/venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $py)) { throw 'Project Python environment is missing' }
$env:TV_HOST = $TvHost
& $py -I (Join-Path $PSScriptRoot 'configure-home.py') --restore
if ($LASTEXITCODE -ne 0) { throw 'Original HOME restoration or verification failed; see backup/mitv-mosr4-home/home-restore.json' }
