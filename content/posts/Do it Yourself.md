---
title: Create your own blog from Markdown!
date: 2025-02-10
author: Erin
description: A comprehensive guide on creating a blog using Hugo, Python, and Obsidian with automatic deployment
tags:
  - tutorial
  - hugo
  - python
  - obsidian
  - markdown
categories:
  - tech
draft: false
toc: true
---
# Create your own blog from Markdown!

Want to create a blog that seamlessly integrates with Obsidian and automatically deploys your content? In this tutorial, I'll show you how I built my blog using Hugo, Python, and Obsidian, complete with automatic deployment and special features like Dataview table conversion.

I am hosting this on [Hostinger](https://www.hostinger.com/cart?product=hosting%3Ahostinger_premium&period=48&referral_type=cart_link&REFERRALCODE=2HCANGELIPNL&referral_id=0194ef35-616c-70e9-afcf-90b7e3f6463b) to host my blog and portfolio online and I highly recommend it for the price and convenience. I utilize their Git Deployments to automatically pull the necessary files from my private repo so I can publish them on this website seamlessly and make quick edits from anywhere.


<div class="cardlink">
<style>

        .cardlink {
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            background: var(--background);
            transition: transform 0.2s;
            display: block;
        }
        .cardlink:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .cardlink a {
            text-decoration: none;
            color: inherit;
        }
        .cardlink-content {
            display: flex;
            gap: 1rem;
            align-items: flex-start;
        }
        .cardlink-text {
            flex: 1;
        }
        .cardlink-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: var(--accent);
            margin: 0 0 0.5rem 0;
        }
        .cardlink-description {
            font-size: 0.9rem;
            color: var(--color);
            margin: 0;
            opacity: 0.8;
        }
        .cardlink-host {
            font-size: 0.8rem;
            color: var(--color);
            opacity: 0.6;
            margin-top: 0.5rem;
        }
        .cardlink-image {
            width: 160px;
            height: 120px;
            object-fit: cover;
            border-radius: 4px;
            margin: 0;
        }
        @media (max-width: 600px) {
            .cardlink-content {
                flex-direction: column;
            }
            .cardlink-image {
                width: 100%;
                height: 160px;
                margin-top: 1rem;
            }
        }
    
</style>
<a href="https://support.hostinger.com/en/articles/1583302-how-to-deploy-a-git-repository" target="_blank" rel="noopener noreferrer">
<div class="cardlink-content">
<div class="cardlink-text">
<h3 class="cardlink-title">How to Deploy a Git Repository | Hostinger Help Center</h3>
<p class="cardlink-description">Deploying and managing git repositories using Hostinger’s hPanel</p>
<div class="cardlink-host">support.hostinger.com</div>
</div>
<img class="cardlink-image" src="https://downloads.intercomcdn.com/i/o/288430/865baa10d93939db2c24769a/a0572934395627b730f28e221c3901a2.jpg" alt="How to Deploy a Git Repository | Hostinger Help Center">
</div>
</a>
</div>

You can use this to pull from the `hostinger-deploy` branch that gets created. That is the branch you will want to push to whatever web hosting you use to display your site online similar to this one.

### Works with several Obsidian Plugins
I have set up the `files.py` file to work with several plugins...
- Dataview
- Card Link
- Handwritten Notes - it displays PDFs inline via the browser's PDF viewer.
- Obsidian Canvas - Can display an embedded canvas on the page.
- Obsidian Kanban - Can display an embedded Kanban on the page.

## Prerequisites

You'll need:
- [Hugo](https://gohugo.io/installation/) installed on your system
- [Python](https://www.python.org/downloads/) 3.8 or higher
- [Git](https://git-scm.com/downloads)
- [Obsidian](https://obsidian.md/) for writing markdown
- Basic knowledge of markdown and command line

## Step 1: Setting Up Hugo

1. First, create a new Hugo site:
   ```bash
   hugo new site yourblog
   cd yourblog
   ```

2. Install the Terminal theme (or any theme you prefer):
   ```bash
   git submodule add https://github.com/panr/hugo-theme-terminal.git themes/terminal
   ```

3. Create a `hugo.toml` configuration file:
   ```toml
   baseURL = "https://yourdomain.com/blog"
   languageCode = "en-us"
   title = "Your Blog Title"
   theme = "terminal"

   # Update paginate to use the new syntax
   pagination.pagerSize = 5

   [markup]
     [markup.goldmark]
       [markup.goldmark.renderer]
         unsafe = true  # Allow HTML in markdown
     [markup.highlight]
       codeFences = true
       guessSyntax = true
       lineNos = true
       style = "monokai"

   [params]
     # Terminal theme specific settings
     contentTypeName = "posts"
     themeColor = "teal"
     showMenuItems = 2
     fullWidthTheme = false
     centerTheme = true
     autoCover = true
     showLastUpdated = true
     showReadMore = true
     readMore = "Read post"

   [frontmatter]
     lastmod = ["lastmod", ":fileModTime", ":default"]

   [permalinks]
     posts = "/:filename/"

   [urls]
     disablePathToLower = true
     preserveSymlinks = true

   [outputs]
     home = ["html", "json"]
   ```

## Step 2: Setting Up the Python Script

Use the following code to create a Python script (`files.py`) that will handle the conversion of Obsidian-style links and Dataview blocks to Hugo-compatible HTML:

```python
import os
import re
import shutil
import yaml
from datetime import datetime

# Paths
posts_dir = r"YOUR OBSIDIAN VAULT AND BLOG FOLDER"  # Update this path
attachments_base = r"THE ATTACHMENTS FOLDER THERE"    # Update this path
static_images_dir = r"IMAGE FOLDER INSIDE YOUR BLOG usually static\images"
static_files_dir = r"PDF and Other Files folder usually static\files"

# Ensure the target directories exist
os.makedirs(static_images_dir, exist_ok=True)
os.makedirs(static_files_dir, exist_ok=True)

def parse_dataview_query(query_block):
    """Parse a Dataview query block and convert it to Hugo-compatible format."""
    print("\nProcessing Dataview query block:")
    print(query_block)
    
    # Extract the query type and parameters
    lines = [line.strip() for line in query_block.strip().split('\n')]
    query_type = lines[0].lower()
    print(f"Query type: {query_type}")
    
    # Initialize result
    result = []
    
    if 'table' in query_type:
        print("Processing TABLE query")
        # Handle TABLE queries
        fields = []
        field_aliases = {}
        data = []
        in_data = False
        
        # First line might contain field definitions
        field_line = lines[0].lower().replace('table', '').strip()
        if field_line:
            # Parse fields and their aliases
            field_parts = [f.strip() for f in field_line.split(',')]
            for part in field_parts:
                if ' as ' in part.lower():
                    field, alias = [p.strip().strip('"') for p in part.lower().split(' as ')]
                    fields.append(field)
                    field_aliases[field] = alias
                else:
                    fields.append(part)
                    field_aliases[part] = part
        
        print(f"Fields: {fields}")
        print(f"Aliases: {field_aliases}")
        
        # Process the remaining lines
        for line in lines[1:]:
            if not line:  # Skip empty lines
                continue
            print(f"Processing line: {line}")
            if 'from' in line.lower():
                in_data = True
                source_folder = line.split('"')[1] if '"' in line else line.split(' ')[1]
                print(f"Found FROM clause, source: {source_folder}")
                # Get all markdown files in the posts directory
                for filename in os.listdir(posts_dir):
                    if filename.endswith('.md'):
                        file_path = os.path.join(posts_dir, filename)
                        row_data = []
                        for field in fields:
                            if 'file.name' in field:
                                value = os.path.splitext(filename)[0]
                            elif 'title' in field.lower():
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        front_matter = re.search(r'^---\s*\n(.*?)\n\s*---', content, re.DOTALL)
                                        if front_matter:
                                            metadata = yaml.safe_load(front_matter.group(1))
                                            value = metadata.get('title', os.path.splitext(filename)[0])
                                        else:
                                            value = os.path.splitext(filename)[0]
                                except Exception as e:
                                    print(f"Error getting title: {e}")
                                    value = os.path.splitext(filename)[0]
                            elif 'url' in field.lower() or 'file.path' in field.lower():
                                value = f"/blog/{get_file_url(os.path.splitext(filename)[0])}"
                            elif 'date' in field:
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        front_matter = re.search(r'^---\s*\n(.*?)\n\s*---', content, re.DOTALL)
                                        if front_matter:
                                            metadata = yaml.safe_load(front_matter.group(1))
                                            value = metadata.get('date', '')
                                        else:
                                            value = ''
                                except Exception as e:
                                    print(f"Error getting date: {e}")
                                    value = ''
                            elif 'tags' in field:
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        front_matter = re.search(r'^---\s*\n(.*?)\n\s*---', content, re.DOTALL)
                                        if front_matter:
                                            metadata = yaml.safe_load(front_matter.group(1))
                                            tags = metadata.get('tags', [])
                                            value = ', '.join(tags)
                                        else:
                                            value = ''
                                except Exception as e:
                                    print(f"Error getting tags: {e}")
                                    value = ''
                            else:
                                value = ''
                            row_data.append(value)
                            print(f"Field {field}: {value}")
                        
                        if row_data:
                            data.append(row_data)
                            print(f"Added row: {row_data}")
                continue
            
            if 'where' in line.lower() or 'sort' in line.lower():
                print(f"Skipping {line}")
                continue
        
        if fields:
            # Generate HTML table with styling
            html = ['<div class="dataview-table">']
            html.append('<style>')
            html.append('''
                .dataview-table {
                    margin: 2rem 0;
                    overflow-x: auto;
                }
                .dataview-table table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 0;
                    font-size: 0.95rem;
                    background: var(--background);
                }
                .dataview-table th {
                    background-color: var(--accent);
                    color: var(--background);
                    padding: 0.75rem 1rem;
                    text-align: left;
                    font-weight: bold;
                    border-bottom: 2px solid var(--border-color);
                }
                .dataview-table td {
                    padding: 0.75rem 1rem;
                    border-bottom: 1px solid var(--border-color);
                    vertical-align: top;
                }
                .dataview-table tr:hover {
                    background-color: var(--hover);
                }
                .dataview-table tr:last-child td {
                    border-bottom: none;
                }
                .dataview-table a {
                    color: var(--accent);
                    text-decoration: none;
                }
                .dataview-table a:hover {
                    text-decoration: underline;
                }
                @media (max-width: 768px) {
                    .dataview-table {
                        margin: 1rem -1rem;
                        width: calc(100% + 2rem);
                    }
                    .dataview-table th,
                    .dataview-table td {
                        padding: 0.5rem;
                    }
                }
            ''')
            html.append('</style>')
            html.append('<table>')
            
            # Add headers
            header_names = [field_aliases.get(field, field).title() for field in fields]
            html.append('<thead><tr>')
            for header in header_names:
                html.append(f'<th>{header}</th>')
            html.append('</tr></thead>')
            
            # Add data rows
            html.append('<tbody>')
            for row in data:
                html.append('<tr>')
                for i, cell in enumerate(row):
                    if 'url' in fields[i].lower() or 'file.path' in fields[i].lower():
                        html.append(f'<td><a href="{cell}">{cell}</a></td>')
                    else:
                        html.append(f'<td>{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
            
            html.append('</table>')
            html.append('</div>')
            
            result = '\n'.join(html)
            print("\nGenerated HTML table:")
            print(result)
    
    elif 'list' in query_type:
        # List processing code here (similar structure to table)
        pass
    
    return result

def process_dataview(content):
    """Find and process Dataview code blocks."""
    print("\nLooking for Dataview blocks in content...")
    dataview_pattern = r'(?:^|\n)[ \t]*```+[ \t]*dataview[ \t]*\n(.*?)\n[ \t]*```+[ \t]*(?:\n|$)'
    matches = re.finditer(dataview_pattern, content, flags=re.DOTALL)
    match_count = 0
    
    def replace_dataview(match):
        nonlocal match_count
        match_count += 1
        print(f"\nProcessing Dataview block #{match_count}")
        query_block = match.group(1).strip()
        result = parse_dataview_query(query_block)
        print(f"Replacing Dataview block with: {result}")
        return f"\n{result}\n"
    
    processed_content = re.sub(dataview_pattern, replace_dataview, content, flags=re.DOTALL)
    if match_count == 0:
        print("No Dataview blocks found in content")
        print("Content preview:")
        print(content[:500])
    else:
        print(f"Processed {match_count} Dataview blocks")
    
    return processed_content

def get_file_url(filename):
    """Get the URL-friendly version of a filename."""
    base_name = filename.replace('.md', '')
    return base_name.lower().replace(' ', '-')

def clean_filename(filename):
    """Extract the actual filename from Obsidian path and remove alias."""
    filename = filename.split('/')[-1]
    filename = filename.split('|')[0]
    return filename

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Process Dataview blocks
        content = process_dataview(content)

        # Handle internal links and media files
        # ... (additional processing code)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\nAll files processed successfully!")
```

## Step 3: Setting Up Automatic Deployment

Create a PowerShell script (`updateblog.ps1`) for automated deployment:

```powershell
# PowerShell Script for Windows

# Set variables for Obsidian to Hugo copy
$sourcePath = "YOUR OBSIDIAN VAULT BLOG FOLDER"  # Update this path
$destinationPath = "Your blog folder usually \content\posts"  # Update this path

# Set Github repo
$myrepo = "git@github.com:YOURUSERNAME\YOURREPO.git"  # Update this to your repo

# Set error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Change to the script's directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

# Check for required commands
$requiredCommands = @('git', 'hugo')

# Check for Python command
if (Get-Command 'python' -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python'
} elseif (Get-Command 'python3' -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python3'
} else {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

foreach ($cmd in $requiredCommands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Error "$cmd is not installed or not in PATH."
        exit 1
    }
}

# Initialize Git if needed
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

# Sync posts from Obsidian
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
$robocopyOptions = @('/MIR', '/Z', '/W:5', '/R:3')
$robocopyResult = robocopy $sourcePath $destinationPath @robocopyOptions

if ($LASTEXITCODE -ge 8) {
    Write-Error "Robocopy failed with exit code $LASTEXITCODE"
    exit 1
}

# Process Markdown files
Write-Host "Processing image links in Markdown files..."
if (-not (Test-Path "images.py")) {
    Write-Error "Python script images.py not found."
    exit 1
}

# Execute the Python script
try {
    & $pythonCommand images.py
} catch {
    Write-Error "Failed to process image links."
    exit 1
}

# Build the Hugo site
Write-Host "Building the Hugo site..."
try {
    hugo
} catch {
    Write-Error "Hugo build failed."
    exit 1
}

# Git operations
Write-Host "Staging changes for Git..."
git add .

# Commit changes with timestamp
$commitMessage = "New Blog Post on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m "$commitMessage"

# Push to master branch
Write-Host "Deploying to GitHub Master..."
try {
    git push origin master
} catch {
    Write-Error "Failed to push to Master branch."
    exit 1
}

# Deploy to Hostinger branch
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
    Write-Error "Subtree split failed."
    exit 1
}

# Push to hostinger branch with force
try {
    git push origin hostinger-deploy:hostinger --force
} catch {
    Write-Error "Failed to push to hostinger branch."
    git branch -D hostinger-deploy
    exit 1
}
```
## Step 4: Adding Special Features

### Dataview Support

To support Obsidian's Dataview plugin in Hugo, create shortcodes in `layouts/shortcodes/`:

1. `datatable.html` for tables
2. `datalist.html` for lists

Example Dataview query that works with this setup:
```markdown
<div class="dataview-table">
<style>

                .dataview-table {
                    margin: 2rem 0;
                    overflow-x: auto;
                }
                .dataview-table table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 0;
                    font-size: 0.95rem;
                    background: var(--background);
                }
                .dataview-table th {
                    background-color: var(--accent);
                    color: var(--background);
                    padding: 0.75rem 1rem;
                    text-align: left;
                    font-weight: bold;
                    border-bottom: 2px solid var(--border-color);
                }
                .dataview-table td {
                    padding: 0.75rem 1rem;
                    border-bottom: 1px solid var(--border-color);
                    vertical-align: top;
                }
                .dataview-table tr:hover {
                    background-color: var(--hover);
                }
                .dataview-table tr:last-child td {
                    border-bottom: none;
                }
                .dataview-table a {
                    color: var(--accent);
                    text-decoration: none;
                }
                .dataview-table a:hover {
                    text-decoration: underline;
                }
                @media (max-width: 768px) {
                    .dataview-table {
                        margin: 1rem -1rem;
                        width: calc(100% + 2rem);
                    }
                    .dataview-table th,
                    .dataview-table td {
                        padding: 0.5rem;
                    }
                }
            
</style>
<table>
<thead><tr>
<th>Name</th>
<th>Title</th>
<th>Url</th>
</tr></thead>
<tbody>
<tr>
<td>Do it Yourself</td>
<td>Create your own blog from Markdown!</td>
<td><a href="/blog/do-it-yourself">/blog/do-it-yourself</a></td>
</tr>
<tr>
<td>Test Blog 2</td>
<td>My Test Blog Post #2</td>
<td><a href="/blog/test-blog-2">/blog/test-blog-2</a></td>
</tr>
<tr>
<td>Test Blog</td>
<td>My Test Blog Post</td>
<td><a href="/blog/test-blog">/blog/test-blog</a></td>
</tr>
</tbody>
</table>
</div>

### PDF Embedding

Create a shortcode for PDF embedding (`layouts/shortcodes/pdf.html`):

```html
<div class="pdf-container">
    <iframe src="{{ .Get "src" }}" style="width: 100%; height: 800px;" frameborder="0">
        <p>It appears your browser doesn't support iframes.</p>
    </iframe>
</div>
```

## Step 5: Writing Blog Posts

1. Create your posts in Obsidian using standard markdown
2. Use front matter for metadata:
   ```yaml
   ---
   title: "Your Post Title"
   date: 2024-02-10
   author: "Your Name"
   description: "Post description"
   tags: ["tag1", "tag2"]
   categories: ["category"]
   draft: false
   toc: true
   ---
   ```

3. Use Dataview queries as needed
4. Add images and PDFs using Obsidian's syntax: `![[image.jpg]]` or `![[document.pdf]]`

## Step 6: Deployment

1. Run the update script:
   ```powershell
   .\updateblog.ps1
   ```

2. The script will:
   - Sync your Obsidian posts
   - Process all markdown files
   - Convert Dataview blocks to HTML
   - Build the Hugo site
   - Deploy to GitHub

## Customization Tips

1. **Theme Colors**: Modify the `themeColor` in `hugo.toml`
2. **Styling**: Add custom CSS in `assets/css/`
3. **Shortcodes**: Create new shortcodes in `layouts/shortcodes/`
4. **Python Script**: Extend `images.py` to handle additional Obsidian features

## Common Issues and Solutions

1. **Hugo Version Compatibility**: If you see warnings about module compatibility, update your Hugo version or use a compatible theme version
2. **Image Paths**: Ensure your Obsidian attachments folder is correctly configured in the Python script
3. **Git Line Endings**: Add a `.gitattributes` file to handle line ending issues:
   ```
   * text=auto eol=lf
   ```

## Conclusion

This setup provides a powerful blogging workflow that combines the ease of writing in Obsidian with the power of Hugo for static site generation. The Python script handles all the conversion automatically, making it seamless to publish your content.

For the complete source code and more detailed examples, check out my GitHub repository. Feel free to adapt this setup to your needs and contribute improvements!

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Terminal Theme Documentation](https://github.com/panr/hugo-theme-terminal)
- [Obsidian Documentation](https://help.obsidian.md/)
- [Python Documentation](https://docs.python.org/)