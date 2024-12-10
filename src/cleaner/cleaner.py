# find node_modules find ~ -type d -regex '.*/node_modules$' -not -regex '.*/node_modules/.*/node_modules.*'
# find directory size: du -sh _PATH_
import asyncio
import subprocess
import typing as T
from pathlib import Path

from cleaner.cli import display_package_stats
from cleaner.moduletracker import save_path
from cleaner.pathutils import (
    get_directory_size,
    path_as_string,
    get_package_type_and_last_modified,
    set_root_path,
)
from cleaner.spacetracker import track_saving


def process_modules(directory: bytes):
    node_module_path = path_as_string(directory)
    save_path(node_module_path)
    size = get_directory_size(node_module_path)
    track_saving(int(size))

    [package_type, last_modified] = get_package_type_and_last_modified(node_module_path)
    display_package_stats(node_module_path, package_type, size, last_modified)


async def dequeue(stream: asyncio.StreamReader, callback: T.Callable[[bytes], None]):
    while True:
        line = await stream.readline()
        if not line:
            break
        callback(line)


async def find_modules_and_venvs(path: Path):
    set_root_path(path)

    node_command = [
        "find",
        str(path.absolute()),
        "-type",
        "d",
        "-regex",
        "'.*/node_modules$'",
        "-not",
        "-regex",
        "'.*/node_modules/.*/node_modules.*'",
        "-exec",
        "echo",
        "{}",
        "\\;",
    ]

    venv_command = [
        "find",
        str(path.absolute()),
        "-type",
        "d",
        "-regex",
        "'.*/.venv$'",
        "-exec",
        "echo",
        "{}",
        "\\;"
    ]

    node_module_search = await asyncio.create_subprocess_shell(
        " ".join(node_command), stdout=subprocess.PIPE
    )

    venv_search = await asyncio.create_subprocess_shell(
        " ".join(venv_command), stdout=subprocess.PIPE
    )

    await asyncio.wait(
        [
            asyncio.create_task(dequeue(node_module_search.stdout, process_modules)),
            asyncio.create_task(dequeue(venv_search.stdout, process_modules)),
        ]
    )
    await node_module_search.wait()
    await venv_search.wait()
