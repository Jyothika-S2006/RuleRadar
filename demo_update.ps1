$ErrorActionPreference = 'Stop'

$livePagePath = Join-Path $PSScriptRoot 'demo_site\live.html'
$updatedPagePath = Join-Path $PSScriptRoot 'demo_site\v2.html'

Copy-Item -LiteralPath $updatedPagePath -Destination $livePagePath -Force
