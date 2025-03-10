# agents/folder_scanner.py

import os

def get_folder_tree(root_path):
    """
    Recursively scans the folder and returns a string representing the folder structure.
    Sensitive files are listed but not read.
    """
    tree_lines = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # List .git folder but do not descend into it
        if '.git' in dirnames:
            tree_lines.append(os.path.join(dirpath, '.git/'))
            dirnames.remove('.git')
        level = dirpath.replace(root_path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_lines.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            tree_lines.append(f"{subindent}{f}")
    return "\n".join(tree_lines)

def find_license(root_path):
    """
    Searches for a license file (e.g., LICENSE, COPYING) and returns its content.
    """
    possible_license_names = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYING.txt"]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower() in [name.lower() for name in possible_license_names]:
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    return f"Error reading license file: {e}"
    return "License not present."
