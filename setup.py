import json
from pathlib import Path
import shutil

def setup_build():
    # Load configuration from config.json
    with open("config.json") as config_file:
        config = json.load(config_file)

    # Define paths based on the configuration
    root_dir = Path(config["root_directory"])
    build_dir = Path(config["build_directory"])
    static_dir = Path(config["static_directory"])

    # Step 1: Trash the build directory if it exists
    if build_dir.exists() and build_dir.is_dir():
        shutil.rmtree(build_dir)

    # Step 2: Create the build directory
    build_dir.mkdir(parents=True, exist_ok=True)

    # Step 3: Clone static directory from root_directory to build_directory
    source_static = root_dir / static_dir
    destination_static = build_dir / static_dir

    # Copy the entire static directory (recursively)
    if source_static.exists() and source_static.is_dir():
        shutil.copytree(source_static, destination_static)
    else:
        print(f"Warning: {source_static} does not exist or is not a directory.")

# Run the function
setup_build()
