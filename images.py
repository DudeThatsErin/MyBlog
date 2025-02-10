import os
import re
import shutil
import yaml
from datetime import datetime

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog-1\content\posts"
attachments_base = r"E:\Obs\MyVault\90-Attachments\blogs"  # Updated base attachments path
static_images_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\images"
static_files_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\files"

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
            # Generate HTML table
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
        print("Processing LIST query")
        # Handle LIST queries
        query = ""
        for line in lines[1:]:
            if line.lower().startswith('where'):
                query = line[6:].strip()  # Extract the where clause
                print(f"Found WHERE clause: {query}")
                break
        
        # Generate HTML list
        html = ['<div class="dataview-list">']
        html.append('<style>')
        html.append('''
            .dataview-list {
                margin: 2rem 0;
            }
            .dataview-list ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .dataview-list li {
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid var(--border-color);
            }
            .dataview-list li:last-child {
                border-bottom: none;
            }
            .dataview-list h4 {
                margin: 0 0 0.5rem 0;
            }
            .dataview-list .metadata {
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 0.5rem;
            }
            .dataview-list .tags {
                margin-left: 1rem;
            }
            .dataview-list .tags a {
                margin-right: 0.5rem;
                color: var(--accent);
                text-decoration: none;
            }
            .dataview-list .tags a:hover {
                text-decoration: underline;
            }
            .dataview-list .description {
                margin: 0.5rem 0 0 0;
                color: #444;
            }
        ''')
        html.append('</style>')
        html.append('<ul>')
        
        # Get all markdown files in the posts directory
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(posts_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        front_matter = re.search(r'^---\s*\n(.*?)\n\s*---', content, re.DOTALL)
                        if front_matter:
                            metadata = yaml.safe_load(front_matter.group(1))
                            if not query or query.lower() in content.lower():
                                title = metadata.get('title', os.path.splitext(filename)[0])
                                date = metadata.get('date', '')
                                tags = metadata.get('tags', [])
                                description = metadata.get('description', '')
                                url = get_file_url(os.path.splitext(filename)[0])
                                
                                html.append('<li>')
                                html.append('<div class="list-item">')
                                html.append(f'<h4><a href="/blog/{url}">{title}</a></h4>')
                                html.append('<div class="metadata">')
                                if date:
                                    html.append(f'<span class="date">{date}</span>')
                                if tags:
                                    html.append('<span class="tags">')
                                    for tag in tags:
                                        html.append(f'<a href="/blog/tags/{tag.lower()}">{tag}</a>')
                                    html.append('</span>')
                                html.append('</div>')
                                if description:
                                    html.append(f'<p class="description">{description}</p>')
                                html.append('</div>')
                                html.append('</li>')
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
        
        html.append('</ul>')
        html.append('</div>')
        
        result = '\n'.join(html)
        print("\nGenerated HTML list:")
        print(result)
    
    return result

def process_dataview(content):
    """Find and process Dataview code blocks."""
    print("\nLooking for Dataview blocks in content...")
    # Updated pattern to be more flexible with whitespace and backticks
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
        print(content[:500])  # Print first 500 chars to help debug
    else:
        print(f"Processed {match_count} Dataview blocks")
    
    return processed_content

def create_filename(title):
    """Convert a title to a filename-friendly format."""
    # Replace spaces with hyphens and preserve special characters
    filename = title.lower().replace(' ', '-')
    # Ensure special characters are preserved (single encoding)
    filename = filename.replace('#', '2')  # Just use 2 for the number
    return filename

def format_url(title):
    """Format a title into a URL-friendly string."""
    # Convert to lowercase and replace spaces with hyphens
    url = title.lower().replace(' ', '-')
    # Handle special characters
    url = url.replace('#', '%232')
    return url

def clean_filename(filename):
    """Extract the actual filename from Obsidian path and remove alias."""
    # Remove any folder structure
    filename = filename.split('/')[-1]
    # Remove any alias
    filename = filename.split('|')[0]
    return filename

def get_file_url(filename):
    """Get the URL-friendly version of a filename."""
    # Remove .md extension if present
    base_name = filename.replace('.md', '')
    # For Test Blog 2, return test-blog-2
    if base_name == 'Test Blog 2':
        return 'test-blog-2'
    # For Test Blog, return test-blog
    if base_name == 'Test Blog':
        return 'test-blog'
    return base_name.lower().replace(' ', '-')

def get_post_attachments_dir(post_name):
    """Get the attachments directory for a specific post."""
    return os.path.join(attachments_base, post_name)

# Get list of all markdown files and their metadata
file_metadata = {}
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        base_name = filename.replace('.md', '')
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # Extract front matter
            front_matter = re.search(r'^---\s*\n(.*?)\n\s*---', content, re.DOTALL)
            if front_matter:
                try:
                    metadata = yaml.safe_load(front_matter.group(1))
                    title = metadata.get('title', base_name)
                    file_metadata[base_name] = {
                        'title': title,
                        'url': get_file_url(base_name)
                    }
                except Exception as e:
                    print(f"Warning: Could not parse front matter for {filename}: {str(e)}")
                    file_metadata[base_name] = {
                        'title': base_name,
                        'url': get_file_url(base_name)
                    }
            else:
                file_metadata[base_name] = {
                    'title': base_name,
                    'url': get_file_url(base_name)
                }

print("\nFound posts:", file_metadata)

def parse_cardlink(cardlink_block):
    """Parse a Cardlink block and convert it to Hugo-compatible HTML."""
    print("\nProcessing Cardlink block:")
    print(cardlink_block)
    
    # Extract cardlink properties
    properties = {}
    lines = [line.strip() for line in cardlink_block.strip().split('\n')]
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            properties[key.strip()] = value.strip().strip('"')
    
    # Generate HTML for the cardlink
    html = ['<div class="cardlink">']
    html.append('<style>')
    html.append('''
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
    ''')
    html.append('</style>')
    
    # Create the card content
    html.append(f'<a href="{properties.get("url", "#")}" target="_blank" rel="noopener noreferrer">')
    html.append('<div class="cardlink-content">')
    
    # Text content
    html.append('<div class="cardlink-text">')
    if 'title' in properties:
        html.append(f'<h3 class="cardlink-title">{properties["title"]}</h3>')
    if 'description' in properties:
        html.append(f'<p class="cardlink-description">{properties["description"]}</p>')
    if 'host' in properties:
        html.append(f'<div class="cardlink-host">{properties["host"]}</div>')
    html.append('</div>')
    
    # Image if available
    if 'image' in properties:
        html.append(f'<img class="cardlink-image" src="{properties["image"]}" alt="{properties.get("title", "Link preview")}">')
    
    html.append('</div>')
    html.append('</a>')
    html.append('</div>')
    
    return '\n'.join(html)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Process Dataview blocks first
        content = process_dataview(content)

        # Process Cardlink blocks
        cardlink_pattern = r'```cardlink\n(.*?)\n```'
        content = re.sub(cardlink_pattern, lambda m: parse_cardlink(m.group(1)), content, flags=re.DOTALL)

        # Handle internal links (links to other posts)
        internal_links = re.findall(r'\[\[([^]\.]*)\]\]', content)
        for link_name in internal_links:
            # Try to match the link with a file
            link_base = link_name.replace('.md', '')
            if link_base in file_metadata:
                meta = file_metadata[link_base]
                markdown_link = f"[{meta['title']}](/blog/{meta['url']})"
                print(f"Converting internal link: {link_name} -> {markdown_link}")
                content = re.sub(r'\[\[' + re.escape(link_name) + r'\]\]', markdown_link, content)

        # Handle media files (images and PDFs)
        # Updated pattern to handle folder paths and aliases
        media_pattern = r'!\[\[(.*?(?:\.jpg|\.jpeg|\.png|\.gif|\.pdf))(?:\|([^]]*)?)?\]\]'
        media_matches = re.finditer(media_pattern, content, re.IGNORECASE)
        
        for match in media_matches:
            file_path = match.group(1)
            alias = match.group(2) if match.group(2) else None
            file_name = clean_filename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Get the post-specific attachments directory
            post_attachments_dir = get_post_attachments_dir(base_name)
            
            # Try multiple possible locations for the file
            possible_sources = [
                os.path.join(post_attachments_dir, file_name),  # In post's attachments folder
                os.path.join(attachments_base, file_name),      # In base attachments
                os.path.join(posts_dir, file_name),             # Direct in posts
                os.path.join(posts_dir, "attachments", file_name)  # In posts/attachments
            ]
            
            print(f"\nLooking for {file_name}")
            print(f"Original path: {file_path}")
            print(f"Alias: {alias}")
            print(f"Post attachments dir: {post_attachments_dir}")
            
            file_found = False
            for file_source in possible_sources:
                print(f"Trying path: {file_source}")
                if os.path.exists(file_source):
                    print(f"Found file at: {file_source}")
                    if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        # Handle images
                        target_path = os.path.join(static_images_dir, file_name)
                        shutil.copy(file_source, target_path)
                        markdown_link = f'![{alias or file_name}](/blog/images/{file_name})'
                        print(f"Copied image to: {target_path}")
                    elif file_ext == '.pdf':
                        # Handle PDFs
                        target_path = os.path.join(static_files_dir, file_name)
                        shutil.copy(file_source, target_path)
                        markdown_link = f'{{{{< pdf src="/blog/files/{file_name}" >}}}}'
                        print(f"Copied PDF to: {target_path}")
                    
                    print(f"Replacing {match.group(0)} with {markdown_link}")
                    # Replace the Obsidian link with the new markdown/shortcode
                    content = content.replace(match.group(0), markdown_link)
                    file_found = True
                    break
            
            if not file_found:
                print(f"Warning: File not found in any location")
                print(f"Tried paths:")
                for path in possible_sources:
                    print(f"  - {path}")
                print(f"\nContents of directories:")
                print(f"Post attachments dir ({post_attachments_dir}):")
                try:
                    print(os.listdir(post_attachments_dir))
                except Exception as e:
                    print(f"Error listing post attachments directory: {e}")
                print(f"\nBase attachments dir ({attachments_base}):")
                try:
                    print(os.listdir(attachments_base))
                except Exception as e:
                    print(f"Error listing base attachments directory: {e}")

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\nAll files processed successfully!")

def process_markdown_content(content):
    """Process markdown content and convert special blocks."""
    # Process Dataview blocks
    dataview_pattern = r'```dataview\n(.*?)\n```'
    content = re.sub(dataview_pattern, lambda m: parse_dataview_query(m.group(1)), content, flags=re.DOTALL)
    
    # Process Cardlink blocks
    cardlink_pattern = r'```cardlink\n(.*?)\n```'
    content = re.sub(cardlink_pattern, lambda m: parse_cardlink(m.group(1)), content, flags=re.DOTALL)
    
    return content
