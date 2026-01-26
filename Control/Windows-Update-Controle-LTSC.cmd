@echo off
REM ------------------------------------------
REM Windows Update Control Launcher (LTSC)
REM ------------------------------------------

SET SCRIPT_NAME=Windows-Update-Control-LTSC.ps1
SET SCRIPT_PATH=%~dp0%SCRIPT_NAME%

IF NOT EXIST "%SCRIPT_PATH%" (
    echo ERROR: PowerShell script not found.
    echo %SCRIPT_PATH%
    pause
    exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"

exit /b 0
