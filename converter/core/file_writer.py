import os
import shutil

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def copy_component_file(src_file: str, dest_dir: str):
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy(src_file, dest_dir)
