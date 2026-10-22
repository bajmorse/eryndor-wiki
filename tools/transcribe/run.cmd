@echo off
REM Convenience wrapper: runs run.ps1 without changing the system execution policy.
REM -ExecutionPolicy Bypass applies to this one powershell.exe process and
REM persists nothing. Takes the same arguments as run.ps1, e.g.
REM   tools/transcribe/run.cmd -Session session-1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
exit /b %ERRORLEVEL%
