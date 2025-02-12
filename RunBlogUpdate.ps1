# Set the blog directory path
$blogPath = "F:\repos\CURRENTBLOG\erinblog-1"

# Change to the blog directory
Set-Location -Path $blogPath

# Run the update script
& "$blogPath\updateblog.ps1"

# Keep the window open if there are any errors
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 