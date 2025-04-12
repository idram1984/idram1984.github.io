# Get the current directory
$scriptPath = $PSScriptRoot
$projectRoot = $scriptPath

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute "pwsh.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$projectRoot'; poetry run python update_book.py`"" `
    -WorkingDirectory $projectRoot

# Create the scheduled task trigger (runs daily at 2 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 2AM

# Create the scheduled task settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 3

# Create the scheduled task
$taskName = "WhatsPricedInBookUpdate"
$taskDescription = "Updates the Whats Priced In Jupyter Book daily"

# Check if task already exists and remove it if it does
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Register the new task
Register-ScheduledTask -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Force

Write-Host "Scheduled task '$taskName' has been created successfully."
Write-Host "The task will run daily at 2 AM." 