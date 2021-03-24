from datetime import datetime

from cleaner.moduletracker import get_paths_to_clean
from cleaner.pathutils import extract_project_path, delete_node_modules
from cleaner.spacetracker import display_potential_saving


class bcolors:
    """
    Taken from SO (https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal)
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def display_package_stats(node_module_path, package_type, size, last_modified):

    project_path = extract_project_path(node_module_path)
    package_details = (
        ".."
        + bcolors.BOLD
        + bcolors.OKBLUE
        + project_path
        + bcolors.ENDC
        + "node_modules"
    )

    print(
        package_details + " " * (50 - len(project_path)),
        end=" ",
    )
    print(f"{int(size) // 1024:4}MB", end=" ")
    if package_type is None:
        print("no lock file")
    else:
        print(
            f"{package_type:12} – last modified: {datetime.fromtimestamp(last_modified).strftime('%d %b %Y')}"
        )


def prompt_for_cleaning():
    display_potential_saving()
    do_it = input("Do you want to remove these node modules? (y/n)")
    if do_it == "y":
        delete_node_modules(get_paths_to_clean())
