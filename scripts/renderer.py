import os
import shutil
from markdownfilehandler import MarkdownFileHandler  # Import the class we defined

def copy_content_to_output(root_dir):
    content_dir = os.path.join(root_dir, 'content')
    output_dir = os.path.join(root_dir, 'public')
    
    # Step 3: Copy all content from content to output
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Clear output directory if it exists
    shutil.copytree(content_dir, output_dir)
    
    return output_dir

def convert_markdown_to_html_in_output(output_dir):
    # Step 4: Move to output directory and convert .md to .html
    for subdir, _, files in os.walk(output_dir):
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

def static_site_generator():
    # Step 1: Start at the root directory
    root_dir = os.getcwd()  # Get the current working directory
    
    # Step 2: Go to root/content dir
    output_dir = copy_content_to_output(root_dir)
    
    # Step 4: Convert .md files in the output directory to .html
    convert_markdown_to_html_in_output(output_dir)

if __name__ == "__main__":
    static_site_generator()
