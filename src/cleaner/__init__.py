import asyncio
import sys
from pathlib import Path

from cleaner.cleaner import find_node_modules
from cleaner.cli import prompt_for_cleaning


def main(args=None):
    if not args:
        args = sys.argv
    path = Path(args[1])
    print(f"Cleaning {path.absolute()}")
    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(find_node_modules(path))
    loop.close()
    prompt_for_cleaning()


if __name__ == "__main__":
    main(sys.argv)
