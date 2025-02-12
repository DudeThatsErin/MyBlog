# PowerShell Script for Windows

# Set error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Set variables for Obsidian to Hugo copy
$sourcePath = "E:\Obs\MyVault\Blogs"  # Update this path to match your Obsidian vault location
$destinationPath = Join-Path $PSScriptRoot "content\posts"
$attachments_base = "E:\Obs\MyVault\90-Attachments\Blogs"  # Path to attachments
$staticImagesPath = Join-Path $PSScriptRoot "static\images"
$staticFilesPath = Join-Path $PSScriptRoot "static\files"
$myrepo = "git@github.com:DudeThatsErin/MyBlog.git"

# Change to the script's directory
Set-Location $PSScriptRoot

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check for required commands
$requiredCommands = @('git', 'hugo')
foreach ($cmd in $requiredCommands) {
    if (-not (Test-Command $cmd)) {
        Write-Error "$cmd is not installed or not in PATH."
        exit 1
    }
}

# Check for Python command (python or python3)
if (Test-Command 'python') {
    $pythonCommand = 'python'
} elseif (Test-Command 'python3') {
    $pythonCommand = 'python3'
} else {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# Step 1: Check if Git is initialized, and initialize if necessary
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..."
    git init
    git remote add origin $myrepo
} else {
    Write-Host "Git repository already initialized."
    $remotes = git remote
    if (-not ($remotes -contains 'origin')) {
        Write-Host "Adding remote origin..."
        git remote add origin $myrepo
    }
}

# Step 2: Ensure static directories exist
Write-Host "Creating static directories if they don't exist..."
New-Item -ItemType Directory -Force -Path $staticImagesPath | Out-Null
New-Item -ItemType Directory -Force -Path $staticFilesPath | Out-Null

# Step 3: Sync posts from Obsidian to Hugo content folder
Write-Host "Syncing posts from Obsidian..."

if (-not (Test-Path $sourcePath)) {
    Write-Error "Source path does not exist: $sourcePath"
    exit 1
}

if (-not (Test-Path $destinationPath)) {
    Write-Error "Destination path does not exist: $destinationPath"
    exit 1
}

# Use Robocopy to mirror the directories
$robocopyOptions = @('/MIR', '/Z', '/W:5', '/R:3', '/NFL', '/NDL')
$robocopyResult = robocopy $sourcePath $destinationPath @robocopyOptions

if ($LASTEXITCODE -ge 8) {
    Write-Error "Robocopy failed with exit code $LASTEXITCODE"
    exit 1
}

# Step 4: Process Markdown files with Python script
Write-Host "Processing image links in Markdown files..."
if (-not (Test-Path "images.py")) {
    Write-Error "Python script images.py not found."
    exit 1
}

# Execute the Python script
try {
    $env:ATTACHMENTS_BASE = $attachments_base
    & $pythonCommand images.py
    Remove-Item env:ATTACHMENTS_BASE
} catch {
    Write-Error "Failed to process image links: $_"
    exit 1
}

# Step 5: Build the Hugo site
Write-Host "Building the Hugo site..."
try {
    hugo
} catch {
    Write-Error "Hugo build failed: $_"
    exit 1
}

# Step 6: Add changes to Git
Write-Host "Staging changes for Git..."
$hasChanges = (git status --porcelain) -ne $null
if (-not $hasChanges) {
    Write-Host "No changes to stage."
} else {
    git add .
}

# Step 7: Commit changes with a dynamic message
$commitMessage = "New Blog Post on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$hasStagedChanges = (git diff --cached --name-only) -ne $null
if (-not $hasStagedChanges) {
    Write-Host "No changes to commit."
} else {
    Write-Host "Committing changes..."
    git commit -m "$commitMessage"
}

# Step 8: Push all changes to the main branch
Write-Host "Deploying to GitHub Master..."
try {
    git push origin master
} catch {
    Write-Error "Failed to push to Master branch: $_"
    exit 1
}

# Step 9: Push the public folder to the hostinger branch
Write-Host "Deploying to GitHub Hostinger..."

# Check if the temporary branch exists and delete it
$branchExists = git branch --list "hostinger-deploy"
if ($branchExists) {
    git branch -D hostinger-deploy
}

# Perform subtree split
try {
    git subtree split --prefix public -b hostinger-deploy
} catch {
    Write-Error "Subtree split failed: $_"
    exit 1
}

# Push to hostinger branch with force
try {
    git push origin hostinger-deploy:hostinger --force
} catch {
    Write-Error "Failed to push to hostinger branch: $_"
    git branch -D hostinger-deploy
    exit 1
}

Write-Host "Deployment completed successfully!" -ForegroundColor Green