import os
import frontmatter
import yaml

def get_parent_or_filename(filepath):
    # Get the parent directory of the file
    parent_dir = os.path.basename(os.path.dirname(filepath))
    
    # If the parent is 'built', return the filename without extension
    if parent_dir == 'built':
        return os.path.splitext(os.path.basename(filepath))[0]
    
    # Otherwise, return the immediate parent directory
    return parent_dir

class MarkdownFileHandler:
    def __init__(self, filepath):
        """
        Initialize the handler with the .md file path and extract directories and front-matter attributes.
        """
        self.filepath = filepath
        self.item = self.Item()  # An instance of the nested Item class
        self._extract_directories(filepath)
        self._load_front_matter()
        self._load_project_config()

    class Item:
        """ A nested class to store attributes such as cdir, cclass, front-matter, etc. """
        pass

    def _extract_directories(self,filepath):
        """ Extracts the cdir and sets cdir and cclass to 'blogs' if file is in /content/blogs. """
        self.item.cdir = get_parent_or_filename(filepath)
        self.item.cclass = get_parent_or_filename(filepath)

    def _load_front_matter(self):
        """ Loads the front-matter and content from the markdown file into the item. """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            for key, value in post.metadata.items():
                setattr(self.item, key, value)
            self.item.content = post.content

    def _load_project_config(self):
        """ Traces back to the project root and loads the tdir from config.yaml. """
        project_root = self._find_project_root()
        if project_root:
            config_path = os.path.join(project_root, "config.yaml")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.item.tdir = config.get('tdir')

    def _find_project_root(self, config_filename="config.yaml"):
        """ Recursively searches for the project root by looking for the config.yaml file. """
        current_dir = os.path.dirname(self.filepath)
        while current_dir != os.path.dirname(current_dir):  # Stop when reaching the root
            if config_filename in os.listdir(current_dir):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return None

    def get_item(self):
        """ Returns the item containing all the loaded data. """
        return self.item