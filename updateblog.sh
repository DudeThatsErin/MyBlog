#!/bin/bash

# Set error handling
set -e

# Set variables for Obsidian to Hugo copy
SOURCE_PATH="$HOME/Obsidian/MyVault/Blogs"  # Update this path to match your Obsidian vault location
DESTINATION_PATH="$PWD/content/posts"
MYREPO="git@github.com:DudeThatsErin/MyBlog.git"

# Change to the script's directory
cd "$(dirname "$0")"

# Check for required commands
for cmd in git hugo python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed or not in PATH."
        exit 1
    fi
done

# Step 1: Check if Git is initialized, and initialize if necessary
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git remote add origin $MYREPO
else
    echo "Git repository already initialized."
    if ! git remote | grep -q "^origin$"; then
        echo "Adding remote origin..."
        git remote add origin $MYREPO
    fi
fi

# Step 2: Sync posts from Obsidian to Hugo content folder
echo "Syncing posts from Obsidian..."

if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Source path does not exist: $SOURCE_PATH"
    exit 1
fi

if [ ! -d "$DESTINATION_PATH" ]; then
    echo "Error: Destination path does not exist: $DESTINATION_PATH"
    exit 1
fi

# Use rsync for directory synchronization
rsync -av --delete "$SOURCE_PATH/" "$DESTINATION_PATH/"

# Step 3: Process Markdown files with Python script
echo "Processing image links in Markdown files..."
if [ ! -f "images.py" ]; then
    echo "Error: Python script images.py not found."
    exit 1
fi

# Execute the Python script
python3 images.py

# Step 4: Build the Hugo site
echo "Building the Hugo site..."
hugo

# Step 5: Add changes to Git
echo "Staging changes for Git..."
if [ -n "$(git status --porcelain)" ]; then
    git add .
else
    echo "No changes to stage."
fi

# Step 6: Commit changes with a dynamic message
COMMIT_MESSAGE="New Blog Post on $(date '+%Y-%m-%d %H:%M:%S')"
if [ -n "$(git diff --cached --name-only)" ]; then
    echo "Committing changes..."
    git commit -m "$COMMIT_MESSAGE"
else
    echo "No changes to commit."
fi

# Step 7: Push all changes to the main branch
echo "Deploying to GitHub Master..."
git push origin master || {
    echo "Failed to push to Master branch."
    exit 1
}

# Step 8: Push the public folder to the hostinger branch
echo "Deploying to GitHub Hostinger..."

# Check if the temporary branch exists and delete it
if git show-ref --verify --quiet refs/heads/hostinger-deploy; then
    git branch -D hostinger-deploy
fi

# Perform subtree split
git subtree split --prefix public -b hostinger-deploy || {
    echo "Subtree split failed."
    exit 1
}

# Push to hostinger branch with force
if ! git push origin hostinger-deploy:hostinger --force; then
    echo "Failed to push to hostinger branch."
    git branch -D hostinger-deploy
    exit 1
fi

echo "Deployment completed successfully!" 