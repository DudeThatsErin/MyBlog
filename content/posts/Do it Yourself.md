---
title: "Create your own blog from Markdown!"
date: 2024-02-10
author: "Erin"
description: "A comprehensive guide on creating a blog using Hugo, Python, and Obsidian with automatic deployment"
tags: ["tutorial", "hugo", "python", "obsidian", "markdown"]
categories: ["tech"]
draft: false
toc: true
---

# Create your own blog from Markdown!

Want to create a blog that seamlessly integrates with Obsidian and automatically deploys your content? In this tutorial, I'll show you how I built my blog using Hugo, Python, and Obsidian, complete with automatic deployment and special features like Dataview table conversion.

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

Create a Python script (`images.py`) that will handle the conversion of Obsidian-style links and Dataview blocks to Hugo-compatible HTML. Here's a simplified version of what I use:

```python
import os
import re
import shutil
import yaml
from datetime import datetime

# Configure your paths
posts_dir = "content/posts"
attachments_base = "path/to/obsidian/attachments"
static_images_dir = "static/images"
static_files_dir = "static/files"

# Create necessary directories
os.makedirs(static_images_dir, exist_ok=True)
os.makedirs(static_files_dir, exist_ok=True)

# Main functions for processing markdown files
def process_markdown_files():
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            process_single_file(filename)

def process_single_file(filename):
    # Process Dataview blocks
    # Convert internal links
    # Handle images and attachments
    pass  # Full implementation in GitHub repo
```

## Step 3: Setting Up Automatic Deployment

Create a PowerShell script (`updateblog.ps1`) to automate the deployment process:

```powershell
# Set variables
$sourcePath = "path/to/obsidian/posts"
$destinationPath = "content/posts"
$myrepo = "git@github.com:yourusername/yourblog.git"

# Sync posts from Obsidian
robocopy $sourcePath $destinationPath /MIR /Z /W:5 /R:3

# Process markdown files
python images.py

# Build the Hugo site
hugo

# Deploy to GitHub
git add .
git commit -m "New Blog Post on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git push origin master
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