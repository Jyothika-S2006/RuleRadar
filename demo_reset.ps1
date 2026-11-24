$ErrorActionPreference = 'Stop'

$databasePath = Join-Path $PSScriptRoot 'ruleradar.db'
$livePagePath = Join-Path $PSScriptRoot 'demo_site\live.html'
$initialPagePath = Join-Path $PSScriptRoot 'demo_site\v1.html'

if (Test-Path -LiteralPath $databasePath) {
    Remove-Item -LiteralPath $databasePath -Force
}

Copy-Item -LiteralPath $initialPagePath -Destination $livePagePath -Force
