import os
import shutil
import markdown

def delete_built_directory(built_dir):
    """Delete the built directory if it exists."""
    if os.path.exists(built_dir):
        shutil.rmtree(built_dir)
        print(f"Deleted existing {built_dir} directory.")

def copy_content_to_built(content_dir, built_dir):
    """Copy everything from content directory to built directory."""
    shutil.copytree(content_dir, built_dir)
    print(f"Copied {content_dir} to {built_dir}.")

def convert_markdown_to_html(md_file_path, template_file_path, output_html_file):
    """Convert a single markdown file to HTML using the template, if it exists."""
    # Step 1: Read and convert Markdown content to HTML
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
        rendered_html = markdown.markdown(markdown_content)
    
    # Check if the template file exists
    if os.path.exists(template_file_path):
        # Step 2: Read the HTML template file
        with open(template_file_path, 'r', encoding='utf-8') as template_file:
            template_content = template_file.read()
        
        # Step 3: Insert the rendered HTML into the template (replace {content})
        final_html_content = template_content.replace("{content}", rendered_html)
    else:
        # No template found, use the rendered HTML directly
        final_html_content = rendered_html
    
    # Step 4: Write the final HTML content to the output file
    with open(output_html_file, 'w', encoding='utf-8') as output_file:
        output_file.write(final_html_content)
    
    print(f"Converted {md_file_path} to {output_html_file}")

def process_built_directory(built_dir):
    """Convert .md files to .html and remove .md files."""
    templates_dir = os.path.join(built_dir, 'templates')  # Path to the templates directory

    for root, _, files in os.walk(built_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                output_html_file = os.path.splitext(md_file_path)[0] + '.html'

                # Determine the appropriate template file
                if file == 'index.md':
                    template_file_path = os.path.join(templates_dir, 'index.template')
                else:
                    parent_dir_name = os.path.basename(os.path.dirname(md_file_path))
                    template_file_path = os.path.join(templates_dir, f'{parent_dir_name}.template')
                
                # Convert the markdown file to HTML
                convert_markdown_to_html(md_file_path, template_file_path, output_html_file)

                # Remove the original .md file
                os.remove(md_file_path)
                print(f"Removed {md_file_path} after conversion.")

if __name__ == "__main__":
    # Since you're running from the root directory, paths are relative to the root.
    content_dir = './content'
    built_dir = './built'

    # Step 1: Delete the built directory if it exists
    delete_built_directory(built_dir)

    # Step 2: Copy everything from the content directory to the built directory
    copy_content_to_built(content_dir, built_dir)

    # Step 3: Process the built directory, convert .md to .html and remove .md files
    process_built_directory(built_dir)
