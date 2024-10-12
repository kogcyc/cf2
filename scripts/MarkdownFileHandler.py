import os
import yaml
import frontmatter

class MarkdownFileHandler:
    def __init__(self, filepath):
        """
        Initialize the handler with the .md file path and extract directories and front-matter attributes.
        """
        self.filepath = filepath
        self.item = self.Item()  # An instance of the nested Item class
        self._extract_directories()
        self._load_front_matter()
        self._load_project_config()

    class Item:
        """ A nested class to store attributes such as sdir, ssdir, front-matter, etc. """
        pass

    def _extract_directories(self):
        """ Extracts the superdir and super-superdir and stores them in the item. """
        full_dir = os.path.dirname(self.filepath)
        superdir = os.path.dirname(full_dir) if full_dir else None
        supersuperdir = os.path.dirname(superdir) if superdir and superdir != full_dir else None

        self.item.sdir = full_dir if superdir else None
        self.item.ssdir = supersuperdir if supersuperdir and supersuperdir != superdir else None

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


