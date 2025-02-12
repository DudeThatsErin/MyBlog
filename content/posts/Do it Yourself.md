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
  - blog
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
- Dataview Obsidian Plugin
- Auto Card Link Obsidian Plugin
- Handwritten Notes - it displays PDFs inline via the browser's PDF viewer.
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

Use the following code to create a Python script (`files.py`) that will handle the conversion of Obsidian-style links and Dataview blocks to Hugo-compatible HTML.

You will want to visit the following link and download and utilize the `files.py` there.
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
<a href="https://gist.github.com/DudeThatsErin/95bd33ca27a3c169d4a90622bafbcc8a" target="_blank" rel="noopener noreferrer">
<div class="cardlink-content">
<div class="cardlink-text">
<h3 class="cardlink-title">Everything you need to create your own blog with Hugo!</h3>
<p class="cardlink-description">Everything you need to create your own blog with Hugo! - files.py</p>
<div class="cardlink-host">gist.github.com</div>
</div>
<img class="cardlink-image" src="https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png" alt="Everything you need to create your own blog with Hugo!">
</div>
</a>
</div>

## Step 3: Setting Up Automatic Deployment
Visit this link to get the version that you need:
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
<a href="https://gist.github.com/DudeThatsErin/95bd33ca27a3c169d4a90622bafbcc8a" target="_blank" rel="noopener noreferrer">
<div class="cardlink-content">
<div class="cardlink-text">
<h3 class="cardlink-title">Everything you need to create your own blog with Hugo!</h3>
<p class="cardlink-description">Everything you need to create your own blog with Hugo! - files.py</p>
<div class="cardlink-host">gist.github.com</div>
</div>
<img class="cardlink-image" src="https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png" alt="Everything you need to create your own blog with Hugo!">
</div>
</a>
</div>

### Windows
Create a PowerShell script (`updateblog.ps1`) for automated deployment.
### Mac/Linux
Create a bash script (`updateblog.sh`) for automated deployment.
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
Make sure the update script is placed in the root of your blog. So you if your blog is at `C:\user\hugo\blog` it will be in the `blog` folder.

1. Run the update script:
**Windows**
   ```powershell
   .\updateblog.ps1
   ```
**Mac/Linux**
```bash
./updateblog.sh
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