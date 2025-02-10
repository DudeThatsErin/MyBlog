import os
import re
import shutil

# Paths
posts_dir = r"F:\repos\CURRENTBLOG\erinblog\content\blog\posts"
attachments_dir = r"E:\Obs\MyVault\posts\attachments"
static_images_dir = r"F:\repos\CURRENTBLOG\erinblog\static\posts\attachments"

# Ensure the target directory exists
os.makedirs(static_images_dir, exist_ok=True)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"Processing: {filename}\n---\n{content}\n---\n")  # Debugging output

        # Find all image links in the format [[image.png]]
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        print(f"Found images in {filename}: {images}")  # Debugging output

        for image in images:
            # Correct the Markdown image link format
            markdown_image = f"![Image Description](/{image.replace(' ', '%20')})"
            print(f"Replacing [[{image}]] with {markdown_image}")  # Debugging output

            # Ensure replacement works correctly, avoiding double '!'
            content = re.sub(r'!?(\[\[' + re.escape(image) + r'\]\])', markdown_image, content)

            # Copy the image if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Write the updated content back
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
