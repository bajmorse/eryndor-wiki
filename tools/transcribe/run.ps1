<#
.SYNOPSIS
  Transcribe one session's Craig recordings in Docker (CPU only).
.EXAMPLE
  .\tools\transcribe\run.ps1 -Session session-1
  .\tools\transcribe\run.ps1 -Session session-1 -Model large-v3-turbo
  .\tools\transcribe\run.ps1 -Session session-1 -MergeOnly   # rebuild transcript.md from existing tracks
#>
param(
  [Parameter(Mandatory)] [string] $Session,
  [string] $Model = "large-v3",
  [switch] $MergeOnly,
  [switch] $NoBuild
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$in   = Join-Path $repo "recordings\$Session"
$out  = Join-Path $in "transcript"
if (-not (Test-Path $in)) { throw "No recordings at $in" }
New-Item -ItemType Directory -Force $out | Out-Null

# Probe the daemon with EAP relaxed: in PS 5.1 a native command writing to
# stderr becomes a terminating error while EAP is Stop, which would mask the
# useful message below.
$eap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
docker version --format "{{.Server.Version}}" 2>&1 | Out-Null
$dockerUp = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = $eap
if (-not $dockerUp) {
  throw "Can't reach the Docker daemon. Start Docker Desktop, wait for it to report 'Engine running', then re-run."
}

if (-not $NoBuild) {
  docker build -t eryndor-transcribe $PSScriptRoot
  if ($LASTEXITCODE -ne 0) { throw "docker build failed" }
}

$extra = @()
if ($MergeOnly) { $extra += "--merge-only" }

# No stderr redirect: PS 5.1 turns native stderr into terminating errors under
# ErrorActionPreference=Stop. Progress goes to stdout, which is what we log.
docker run --rm `
  -e MODEL=$Model `
  -v "${in}:/in:ro" `
  -v "${out}:/out" `
  -v eryndor-whisper-cache:/cache `
  eryndor-transcribe --input /in --output /out @extra | Tee-Object -FilePath (Join-Path $out "run.log") -Append
if ($LASTEXITCODE -ne 0) {
  throw "Transcription exited with code $LASTEXITCODE. See $out\run.log. Finished tracks are kept; re-run to resume."
}

Write-Host "`nTranscript: $out\transcript.md"
