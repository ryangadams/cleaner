import shutil
import subprocess
import typing as T
from pathlib import Path


def get_directory_size(directory_path):
    return subprocess.getoutput(rf"du -sk '{directory_path}'").split()[0]


def path_as_string(directory: bytes):
    node_module_path = directory.decode("utf-8")
    node_module_path = node_module_path[:-1]
    return node_module_path


def delete_path(path):
    print(f"Deleting: {path}")
    shutil.rmtree(path)


def delete_node_modules(paths_to_clean):
    for path in paths_to_clean:
        delete_path(path)


def get_package_type_and_last_modified(node_module_path):
    package_json = Path(node_module_path) / ".." / "package-lock.json"
    package_type = "npm-lock"
    if not package_json.exists():
        # try yarn
        package_json = Path(node_module_path) / ".." / "yarn.lock"
        package_type = "yarn-lock"
        if not package_json.exists():
            return [None, 0]
    return [package_type, package_json.stat().st_mtime]


root_path: T.Union[Path, None] = None


def set_root_path(path):
    global root_path
    root_path = path


def extract_project_path(node_module_path):
    global root_path
    project_path = node_module_path.replace(str(root_path.absolute()), "")
    return project_path
