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
    # Extract the query type and parameters
    lines = [line.strip() for line in query_block.strip().split('\n')]
    query_type = lines[0].lower()
    
    # Initialize result
    result = []
    
    if 'table' in query_type:
        # Handle TABLE queries
        fields = []
        data = []
        in_data = False
        
        for line in lines[1:]:
            if not line:  # Skip empty lines
                continue
            if 'from' in line.lower():
                in_data = True
                continue
            if not in_data:
                # Collect fields before 'from'
                fields.extend(f.strip() for f in line.split(',') if f.strip())
            else:
                # Collect data after 'from'
                if 'where' not in line.lower() and 'sort' not in line.lower():
                    data.append(line)
        
        if fields:
            # Create datatable shortcode
            result.append(f'{{{{< datatable headers="{",".join(fields)}" >}}')
            for row in data:
                result.append(row)
            result.append('{{< /datatable >}}')
    
    elif 'list' in query_type:
        # Handle LIST queries
        query = ""
        for line in lines[1:]:
            if line.lower().startswith('where'):
                query = line[6:].strip()  # Extract the where clause
                break
        
        # Create datalist shortcode with optional query
        if query:
            result.append(f'{{{{< datalist query="{query}" >}}')
        else:
            result.append('{{{{< datalist >}}')
        result.append('{{< /datalist >}}')
    
    return '\n'.join(result)

def process_dataview(content):
    """Find and process Dataview code blocks."""
    dataview_pattern = r'```dataview\n(.*?)\n```'
    
    def replace_dataview(match):
        query_block = match.group(1)
        return parse_dataview_query(query_block)
    
    return re.sub(dataview_pattern, replace_dataview, content, flags=re.DOTALL)

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

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Process Dataview blocks first
        content = process_dataview(content)

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
