import os
import re
import yaml
import shutil
from datetime import datetime
import traceback

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog-1\content\posts"
attachments_base = os.getenv('ATTACHMENTS_BASE', r"E:\Obs\MyVault\90-Attachments\Blogs")  # Get from environment or use default
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

def parse_kanban(kanban_content):
    """Parse a Kanban board and convert it to HTML."""
    try:
        # Remove kanban settings metadata
        kanban_content = re.sub(r'%%\s*kanban:settings\s*```.*?```\s*%%', '', kanban_content, flags=re.DOTALL)
        
        # Split content into sections by headers
        sections = re.split(r'(?m)^## ', kanban_content)
        
        html = ['<div class="kanban-board">']
        html.append('''<style>
            .kanban-board {
                display: flex;
                gap: 1rem;
                overflow-x: auto;
                padding: 1rem 0;
                min-height: 400px;
                margin: 1rem 0;
                background: var(--background);
            }
            .kanban-lane {
                min-width: 300px;
                flex: 1;
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1rem;
                display: flex;
                flex-direction: column;
            }
            .kanban-lane-header {
                font-weight: bold;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--accent);
                color: var(--accent);
            }
            .kanban-cards {
                flex: 1;
                min-height: 100px;
            }
            .kanban-card {
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 0.75rem;
                margin-bottom: 0.75rem;
                transition: transform 0.2s;
            }
            .kanban-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .kanban-card-text {
                color: var(--foreground);
                font-size: 0.9rem;
                white-space: pre-wrap;
            }
            .kanban-card-title {
                font-weight: bold;
                margin-bottom: 0.5rem;
                color: var(--accent);
            }
            .kanban-card-checklist {
                margin-top: 0.5rem;
                list-style: none;
                padding-left: 0;
            }
            .kanban-card-checklist-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 0.25rem;
                color: var(--foreground);
            }
            .kanban-card-checkbox {
                margin-right: 0.5rem;
                appearance: none;
                width: 16px;
                height: 16px;
                border: 1px solid var(--border-color);
                border-radius: 3px;
                cursor: not-allowed;
                position: relative;
                top: 2px;
            }
            .kanban-card-checkbox:checked {
                background-color: var(--accent);
                border-color: var(--accent);
            }
            .kanban-card-checkbox:checked::after {
                content: "✓";
                position: absolute;
                color: var(--background);
                font-size: 12px;
                left: 2px;
                top: -2px;
            }
            @media (max-width: 768px) {
                .kanban-board {
                    flex-direction: column;
                }
                .kanban-lane {
                    min-width: 100%;
                }
            }
        </style>''')
        
        # Process each section
        for section in sections[1:]:  # Skip the first empty section
            lines = section.strip().split('\n')
            header = lines[0].strip()  # First line is the header
            content = '\n'.join(lines[1:]).strip()
            
            # Start a new lane
            html.append('<div class="kanban-lane">')
            html.append(f'<div class="kanban-lane-header">{header}</div>')
            html.append('<div class="kanban-cards">')
            
            # Process cards
            cards = re.split(r'(?m)^- \[ \]', content)
            for card in cards[1:]:  # Skip the first empty split
                card_lines = card.strip().split('\n')
                card_title = card_lines[0].strip()
                
                html.append('<div class="kanban-card">')
                
                # Handle card title/text
                if card_title.startswith('# '):
                    title = card_title[2:].strip()
                    html.append(f'<div class="kanban-card-title">{title}</div>')
                else:
                    html.append(f'<div class="kanban-card-text">{card_title}</div>')
                
                # Process card content (description and checklist)
                if len(card_lines) > 1:
                    checklist = []
                    description = []
                    
                    for line in card_lines[1:]:
                        line = line.strip()
                        if line.startswith('- [ ]'):
                            checklist.append((False, line[5:].strip()))
                        elif line.startswith('- [x]'):
                            checklist.append((True, line[5:].strip()))
                        elif line:
                            description.append(line)
                    
                    # Add description if any
                    if description:
                        html.append(f'<div class="kanban-card-text">{"<br>".join(description)}</div>')
                    
                    # Add checklist if any
                    if checklist:
                        html.append('<ul class="kanban-card-checklist">')
                        for is_checked, item in checklist:
                            html.append('<li class="kanban-card-checklist-item">')
                            checked_attr = 'checked' if is_checked else ''
                            html.append(f'<input type="checkbox" class="kanban-card-checkbox" disabled {checked_attr}>')
                            html.append(f'<span>{item}</span>')
                            html.append('</li>')
                        html.append('</ul>')
                
                html.append('</div>')  # Close kanban-card
            
            html.append('</div>')  # Close kanban-cards
            html.append('</div>')  # Close kanban-lane
        
        html.append('</div>')  # Close kanban-board
        return '\n'.join(html)
        
    except Exception as e:
        print(f"Error parsing Kanban: {e}")
        print("Full traceback:")
        traceback.print_exc()
        print("\nKanban content preview:")
        print(kanban_content[:500])
        return f'<div class="error">Error parsing Kanban board: {str(e)}</div>'

def is_kanban_file(content):
    """Check if a file is a Kanban board by looking for the kanban-plugin YAML frontmatter."""
    try:
        frontmatter_match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            return frontmatter.get('kanban-plugin') == 'board'
    except:
        pass
    return False

def copy_file_to_static(source_file, is_image=True):
    """Copy a file to the appropriate static directory and return the new path."""
    try:
        # Determine target directory based on file type
        target_dir = static_images_dir if is_image else static_files_dir
        
        # Get the filename and create target path
        filename = os.path.basename(source_file)
        target_path = os.path.join(target_dir, filename)
        
        # Copy the file
        shutil.copy2(source_file, target_path)
        
        # Return the path relative to the static directory
        return f"/blog/{'images' if is_image else 'files'}/{filename}"
    except Exception as e:
        print(f"Error copying file {source_file}: {e}")
        return None

def process_embedded_files(content, base_name):
    """Process embedded files including Kanban boards, images, and PDFs."""
    print("\nChecking content for embedded files...")
    
    # Process PDFs - handle the format ![[filename.pdf|src3]]
    pdf_pattern = r'!\[\[(.*?\.pdf)\|src3\]\]'
    content = re.sub(pdf_pattern, lambda m: process_pdf_link(m, base_name), content)
    
    # Process Kanban files - handle the format ![[filename.md|embed]]
    kanban_pattern = r'!\[\[(.*?\.md)\|embed\]\]'
    content = re.sub(kanban_pattern, lambda m: process_kanban_link(m, base_name), content)
    
    # Process images - handle the format ![[filename.jpg]]
    image_pattern = r'!\[\[(.*?(?:\.jpg|\.jpeg|\.png|\.gif|\.webp))\]\]'
    content = re.sub(image_pattern, lambda m: process_image_link(m, base_name), content)
    
    return content

def process_image_link(match, post_name):
    """Process an image link and return the updated markdown."""
    image_path = match.group(1)
    
    # Clean up the image path
    image_path = clean_filename(image_path)
    print(f"Processing image: {image_path}")
    
    # Try multiple possible locations for the image
    possible_sources = [
        os.path.join(get_post_attachments_dir(post_name), image_path),
        os.path.join(attachments_base, image_path),
        os.path.join(attachments_base, post_name, image_path)
    ]
    
    for source in possible_sources:
        print(f"Trying source: {source}")
        if os.path.exists(source):
            print(f"Found image at: {source}")
            # Copy the image to static directory and get new path
            new_path = copy_file_to_static(source, is_image=True)
            if new_path:
                return f"![{image_path}]({new_path})"
    
    print(f"Warning: Image not found: {image_path}")
    return match.group(0)

def process_pdf_link(match, post_name):
    """Process a PDF link and return the updated markdown."""
    pdf_path = match.group(1)
    
    # Clean up the PDF path
    pdf_path = clean_filename(pdf_path)
    print(f"Processing PDF: {pdf_path}")
    
    # Try multiple possible locations for the PDF
    possible_sources = [
        os.path.join(get_post_attachments_dir(post_name), pdf_path),
        os.path.join(attachments_base, pdf_path),
        os.path.join(attachments_base, post_name, pdf_path)
    ]
    
    for source in possible_sources:
        print(f"Trying source: {source}")
        if os.path.exists(source):
            print(f"Found PDF at: {source}")
            # Copy the PDF to static directory and get new path
            new_path = copy_file_to_static(source, is_image=False)
            if new_path:
                return f'{{{{< pdf src="{new_path}" >}}}}'
    
    print(f"Warning: PDF not found: {pdf_path}")
    return match.group(0)

def process_kanban_link(match, post_name):
    """Process a Kanban link and return the HTML content."""
    file_path = match.group(1)
    file_name = clean_filename(file_path)
    print(f"Processing Kanban: {file_name}")
    
    # Try multiple possible locations for the file
    possible_sources = [
        os.path.join(get_post_attachments_dir(post_name), file_name),
        os.path.join(attachments_base, file_name),
        os.path.join(posts_dir, file_name),
        os.path.join(attachments_base, post_name, file_name)
    ]
    
    for file_source in possible_sources:
        print(f"Trying source: {file_source}")
        if os.path.exists(file_source):
            try:
                with open(file_source, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                if is_kanban_file(file_content):
                    print(f"Found valid Kanban at: {file_source}")
                    return parse_kanban(file_content)
                else:
                    print(f"Warning: File {file_name} exists but is not a Kanban board")
            except Exception as e:
                print(f"Error processing Kanban file {file_name}: {e}")
                traceback.print_exc()
    
    print(f"Warning: Kanban file not found: {file_name}")
    return match.group(0)

# Update the main file processing loop
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")
        base_name = os.path.splitext(filename)[0]

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Process Dataview blocks
        content = process_dataview(content)

        # Process Cardlink blocks
        cardlink_pattern = r'```cardlink\n(.*?)\n```'
        content = re.sub(cardlink_pattern, lambda m: parse_cardlink(m.group(1)), content, flags=re.DOTALL)

        # Process embedded files
        content = process_embedded_files(content, base_name)

        # Handle internal links
        internal_links = re.findall(r'\[\[([^]\.]*)\]\]', content)
        for link_name in internal_links:
            # Try to match the link with a file
            link_base = link_name.replace('.md', '')
            if link_base in file_metadata:
                meta = file_metadata[link_base]
                markdown_link = f"[{meta['title']}](/blog/{meta['url']})"
                print(f"Converting internal link: {link_name} -> {markdown_link}")
                content = re.sub(r'\[\[' + re.escape(link_name) + r'\]\]', markdown_link, content)

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
