import os
import re
import shutil

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog-1\content\posts"
attachments_dir = r"E:\Obs\MyVault\Blogs\attachments"
static_images_dir = r"F:\repos\CURRENTBLOG\erinblog-1\static\posts\attachments"

# Ensure the target directory exists
os.makedirs(static_images_dir, exist_ok=True)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"Processing: {filename}\n---\n{content}\n---\n")  # Debugging output

        # Find all image links in the format [[file.ext]] where ext can be png, jpg, jpeg, pdf, etc.
        files = re.findall(r'\[\[([^]]*\.(png|jpg|jpeg|pdf))\]\]', content, re.IGNORECASE)
        print(f"Found files in {filename}: {files}")  # Debugging output

        for file_match in files:
            file_name = file_match[0]  # The full filename
            file_ext = file_match[1].lower()  # The extension

            # Correct the Markdown link format
            if file_ext in ['png', 'jpg', 'jpeg']:
                # For images, use image syntax
                markdown_link = f"![{file_name}](/blog/posts/attachments/{file_name.replace(' ', '%20')})"
            else:
                # For PDFs, use link syntax
                markdown_link = f"[{file_name}](/blog/posts/attachments/{file_name.replace(' ', '%20')})"

            print(f"Replacing [[{file_name}]] with {markdown_link}")  # Debugging output

            # Ensure replacement works correctly
            content = re.sub(r'!?\[\[' + re.escape(file_name) + r'\]\]', markdown_link, content)

            # Copy the file if it exists
            file_source = os.path.join(attachments_dir, file_name)
            if os.path.exists(file_source):
                shutil.copy(file_source, static_images_dir)
                print(f"Copied {file_name} to {static_images_dir}")
            else:
                print(f"Warning: File not found: {file_source}")

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and files copied successfully.")
