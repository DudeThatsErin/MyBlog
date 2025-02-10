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

# Get list of all markdown files for reference
all_posts = {}
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # Extract front matter
            front_matter = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if front_matter:
                metadata = yaml.safe_load(front_matter.group(1))
                title = metadata.get('title', filename.replace('.md', ''))
                all_posts[title] = slugify(title)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"\nProcessing file: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # First handle internal links (links to other posts)
        internal_links = re.findall(r'\[\[([^]\.]*)\]\]', content)
        for link_title in internal_links:
            if link_title in all_posts:
                slug = all_posts[link_title]
                markdown_link = f"[{link_title}](/blog/{slug})"
                print(f"Converting internal link: {link_title} -> {markdown_link}")
                content = re.sub(r'\[\[' + re.escape(link_title) + r'\]\]', markdown_link, content)

        # Then handle media files (images and PDFs)
        media_pattern = r'!\[\[([^]]+\.(jpg|jpeg|png|gif|pdf))\]\]'
        media_matches = re.finditer(media_pattern, content, re.IGNORECASE)
        
        for match in media_matches:
            file_name = match.group(1)
            file_ext = match.group(2).lower()
            file_source = os.path.join(attachments_dir, file_name)
            
            print(f"Processing media file: {file_name}")
            
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
                
                # Replace the Obsidian link with the new markdown/shortcode
                content = content.replace(match.group(0), markdown_link)
            else:
                print(f"Warning: File not found: {file_source}")

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("\nAll files processed successfully!")
