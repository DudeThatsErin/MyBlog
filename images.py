import os
import re
import shutil
import yaml
from datetime import datetime

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog-1\content\posts"
attachments_dir = r"E:\Obs\MyVault\Blogs\attachments"
static_images_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\images"
static_files_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\files"

# Ensure the target directories exist
os.makedirs(static_images_dir, exist_ok=True)
os.makedirs(static_files_dir, exist_ok=True)

def parse_dataview_query(query_block):
    """Parse a Dataview query block and convert it to Hugo-compatible format."""
    # Extract the query type and parameters
    lines = query_block.strip().split('\n')
    query_type = lines[0].lower()
    
    # Initialize result
    result = []
    
    if 'table' in query_type:
        # Handle TABLE queries
        fields = []
        for line in lines[1:]:
            if 'from' in line.lower():
                break
            fields.extend(f.strip() for f in line.split(',') if f.strip())
        
        # Create Hugo table header
        if fields:
            result.append('| ' + ' | '.join(fields) + ' |')
            result.append('|' + '---|' * len(fields))
    
    elif 'list' in query_type:
        # Handle LIST queries
        result.append('{{< postlist >}}')
    
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
                    title = metadata.get('title', 'My Test Blog Post #2' if '#2' in base_name else 'My Test Blog Post')
                    file_metadata[base_name] = {
                        'title': title,
                        'filename': create_filename(title)
                    }
                except Exception as e:
                    print(f"Warning: Could not parse front matter for {filename}: {str(e)}")
                    title = 'My Test Blog Post #2' if '#2' in base_name else 'My Test Blog Post'
                    file_metadata[base_name] = {
                        'title': title,
                        'filename': create_filename(title)
                    }
            else:
                title = 'My Test Blog Post #2' if '#2' in base_name else 'My Test Blog Post'
                file_metadata[base_name] = {
                    'title': title,
                    'filename': create_filename(title)
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
                url = format_url(meta['title'])
                markdown_link = f"[{meta['title']}](/blog/{url})"
                print(f"Converting internal link: {link_name} -> {markdown_link}")
                content = re.sub(r'\[\[' + re.escape(link_name) + r'\]\]', markdown_link, content)

        # Handle media files (images and PDFs)
        # Updated pattern to handle folder paths and aliases
        media_pattern = r'!\[\[(.*?(?:\.jpg|\.jpeg|\.png|\.gif|\.pdf))(?:\|[^]]*)?\]\]'
        media_matches = re.finditer(media_pattern, content, re.IGNORECASE)
        
        for match in media_matches:
            file_path = match.group(1)
            file_name = clean_filename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Try both with and without 'attachments' in the path
            possible_sources = [
                os.path.join(attachments_dir, file_name),
                os.path.join(attachments_dir, file_path.replace('blogs/attachments/', ''))
            ]
            
            file_found = False
            for file_source in possible_sources:
                print(f"\nTrying path: {file_source}")
                if os.path.exists(file_source):
                    if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        # Handle images
                        target_path = os.path.join(static_images_dir, file_name)
                        shutil.copy(file_source, target_path)
                        markdown_link = f'![{file_name}](/blog/images/{file_name})'
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
                print(f"Tried paths: {possible_sources}")
                print(f"Contents of attachments directory:")
                try:
                    print(os.listdir(attachments_dir))
                except Exception as e:
                    print(f"Error listing attachments directory: {e}")

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\nAll files processed successfully!")
