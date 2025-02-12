# Get the desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Create the shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$desktopPath\Update Blog.lnk")
$Shortcut.TargetPath = "C:\Program Files\PowerShell\7\pwsh.exe"
$Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$desktopPath\RunBlogUpdate.ps1`""
$Shortcut.WorkingDirectory = $desktopPath
$Shortcut.IconLocation = "C:\Program Files\PowerShell\7\pwsh.exe,0"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!"
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 