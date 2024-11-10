import os
import json
import frontmatter  # You'll need to install this package
import rich  # You'll need to install this package
from jinja2 import Environment, FileSystemLoader  # You'll need to install this package

def load_config(config_path='config.json'):
    """Load JSON configuration file."""
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def read_markdown_files(root_dir):
    """Read all markdown files in a directory, extract frontmatter metadata and content."""
    collections = {}
    
    for dirpath, _, filenames in os.walk(root_dir):
        collection_name = os.path.basename(dirpath)
        
        if collection_name not in collections:
            collections[collection_name] = []

        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)  # Load front matter and content
                
                # Get all metadata as a dictionary
                metadata = post.metadata  # All frontmatter keys/values
                
                # Add metadata, content, path, and filename to collections
                collections[collection_name].append({
                    'filename': filename,
                    'content': post.content,
                    'path': dirpath,  # Store only the directory path
                    **metadata  # Unpack all frontmatter metadata as part of the dictionary
                })

    return collections

# Load configuration and process markdown files
config = load_config()
root_directory = config['root_directory']
collections = read_markdown_files(root_directory)

# Inspect the 'pages' collection using rich for detailed structure display
q = collections['pages']
for item in q:
    #rich.inspect(item, methods=all)
    page = f'<div><h3>{item["title"]}</h3></div>\n<div>{item["content"]}</div>'
    fn = item["path"].replace("root","build")+"/"+item["filename"].replace(".md",".html")
    print(page)
    print(fn)
    # Specify the directory path
    directory_path = item["path"].replace("root","build")
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    with open(fn, 'w') as file:
        # Write content to the file
        file.write(page)




