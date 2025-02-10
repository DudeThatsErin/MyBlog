import os
import re
import shutil
import yaml

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog-1\content\posts"
attachments_dir = r"E:\Obs\MyVault\Blogs\attachments"
static_images_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\images"
static_files_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\files"

# Ensure the target directories exist
os.makedirs(static_images_dir, exist_ok=True)
os.makedirs(static_files_dir, exist_ok=True)

def slugify(title):
    """Convert a title to a URL-friendly slug."""
    # Convert spaces to hyphens and make lowercase
    return title.lower().replace(' ', '-').replace('#', '')

# Get list of all markdown files and their metadata
file_metadata = {}
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        base_name = filename.replace('.md', '')
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # Extract front matter
            front_matter = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if front_matter:
                try:
                    metadata = yaml.safe_load(front_matter.group(1))
                    title = metadata.get('title', base_name)
                    file_metadata[base_name] = {
                        'title': title,
                        'slug': slugify(title)
                    }
                except:
                    print(f"Warning: Could not parse front matter for {filename}")
                    file_metadata[base_name] = {
                        'title': base_name,
                        'slug': slugify(base_name)
                    }

print("\nFound posts:", file_metadata)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Handle internal links (links to other posts)
        internal_links = re.findall(r'\[\[([^]\.]*)\]\]', content)
        for link_name in internal_links:
            # Try to match the link with a file
            link_base = link_name.replace('.md', '')
            if link_base in file_metadata:
                meta = file_metadata[link_base]
                markdown_link = f"[{meta['title']}](/blog/posts/{meta['slug']})"
                print(f"Converting internal link: {link_name} -> {markdown_link}")
                content = re.sub(r'\[\[' + re.escape(link_name) + r'\]\]', markdown_link, content)

        # Handle media files (images and PDFs)
        media_pattern = r'!\[\[([^]]+\.(jpg|jpeg|png|gif|pdf))\]\]'
        media_matches = re.finditer(media_pattern, content, re.IGNORECASE)
        
        for match in media_matches:
            file_name = match.group(1)
            file_ext = match.group(2).lower()
            file_source = os.path.join(attachments_dir, file_name)
            
            print(f"\nProcessing media file: {file_name}")
            print(f"Looking for file at: {file_source}")
            
            if os.path.exists(file_source):
                if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                    # Handle images
                    target_path = os.path.join(static_images_dir, file_name)
                    shutil.copy(file_source, target_path)
                    markdown_link = f'![{file_name}](/blog/images/{file_name})'
                    print(f"Copied image to: {target_path}")
                elif file_ext == 'pdf':
                    # Handle PDFs
                    target_path = os.path.join(static_files_dir, file_name)
                    shutil.copy(file_source, target_path)
                    markdown_link = f'{{{{< pdf src="/blog/files/{file_name}" >}}}}'
                    print(f"Copied PDF to: {target_path}")
                
                print(f"Replacing {match.group(0)} with {markdown_link}")
                # Replace the Obsidian link with the new markdown/shortcode
                content = content.replace(match.group(0), markdown_link)
            else:
                print(f"Warning: File not found at {file_source}")
                print(f"Contents of attachments directory:")
                try:
                    print(os.listdir(attachments_dir))
                except Exception as e:
                    print(f"Error listing attachments directory: {e}")

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\nAll files processed successfully!")
