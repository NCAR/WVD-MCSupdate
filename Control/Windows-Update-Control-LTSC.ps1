# -------------------------------------------------
# Windows Update Enable / Disable Script (LTSC)
# -------------------------------------------------

# Ensure script is running as Administrator
if (-not ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
    ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {

    Start-Process powershell `
        -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" `
        -Verb RunAs
    exit
}

Clear-Host
Write-Host "Windows Update Control (LTSC)" -ForegroundColor Cyan
Write-Host "--------------------------------`n"

Write-Host "1 - Disable Windows Updates"
Write-Host "2 - Enable Windows Updates"
Write-Host "Q - Quit`n"

$choice = Read-Host "Select an option"

$services = @(
    "wuauserv",      # Windows Update
    "UsoSvc"        # Update Orchestrator
#    "UsoSvc",        # Update Orchestrator
#    "WaaSMedicSvc"   # Windows Update Medic
)

switch ($choice.ToUpper()) {

    "1" {
        Write-Host "`nDisabling Windows Update services..." -ForegroundColor Yellow

        foreach ($svc in $services) {
            Write-Host "Stopping and disabling: $svc"
            Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
            Set-Service -Name $svc -StartupType Disabled
        }

        Write-Host "`nWindows Updates have been DISABLED." -ForegroundColor Green
        Write-Host "A reboot is recommended.`n" -ForegroundColor DarkYellow
        Pause
    }

    "2" {
        Write-Host "`nEnabling Windows Update services..." -ForegroundColor Yellow

        foreach ($svc in $services) {
            Write-Host "Enabling and starting: $svc"
            Set-Service -Name $svc -StartupType Manual
            Start-Service -Name $svc -ErrorAction SilentlyContinue
        }

        Write-Host "`nWindows Updates have been ENABLED." -ForegroundColor Green
        Write-Host "You may now check for updates in Settings.`n" -ForegroundColor DarkYellow
        Pause
    }

    "Q" {
        Write-Host "`nNo changes made. Exiting."
        exit
    }

    Default {
        Write-Host "`nInvalid selection. No changes made." -ForegroundColor Red
        Pause
    }
}
