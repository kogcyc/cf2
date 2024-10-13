import os
import shutil
from markdownfilehandler import MarkdownFileHandler  # Import the class we defined

def copy_markdown_files(start_dir):
    # Define the 'built' directory path at the same level as the given directory
    built_dir = os.path.join(os.path.dirname(start_dir), 'built')
    
    # Remove the 'built' directory if it exists
    if os.path.exists(built_dir):
        shutil.rmtree(built_dir)
    
    # Recreate the 'built' directory
    os.makedirs(built_dir)
    
    # Loop through all files in the given directory and its subdirectories
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.md'):
                # Create the relative path to preserve the directory structure
                relative_path = os.path.relpath(root, start_dir)
                
                # Destination directory in the 'built' folder
                dest_dir = os.path.join(built_dir, relative_path)
                
                # Create the destination directory if it doesn't exist
                os.makedirs(dest_dir, exist_ok=True)
                
                # Copy each .md file to the appropriate location in 'built' directory
                src_file = os.path.join(root, file)
                shutil.copy(src_file, dest_dir)
    
    print(f"copied all .md files from {start_dir} to {built_dir}")

def convert_markdown_to_html_in_output(built_dir):
    # Step 4: Move to output directory and convert .md to .html
    for subdir, _, files in os.walk(built_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(subdir, file)
                html_file_path = os.path.splitext(md_file_path)[0] + '.html'
                
                # Use MarkdownFileHandler to process the markdown file
                md_handler = MarkdownFileHandler(md_file_path)
                item = md_handler.get_item()

                # Create a series of divs instead of ul/li
                html_content = ""
                for attribute, value in item.__dict__.items():
                    html_content += f"<div>{attribute}: {value}</div>\n"
                
                # Write the HTML content to a new .html file
                with open(html_file_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)
                
                # Optionally, delete the original .md file
                os.remove(md_file_path)

    print(f"rendered all .md files in {built_dir} into HTML")

# Example usage
start_dir = './content'  # Replace with the actual directory
built_dir = './built'
copy_markdown_files(start_dir)
convert_markdown_to_html_in_output("./built")
