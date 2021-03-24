import pathlib
import time

from cleaner.pathutils import get_package_type_and_last_modified


def test_get_package_json_last_modified_with_package_lock(tmp_path: pathlib.Path):
    timestamp = time.time()
    node_modules = tmp_path / "node_modules"
    package_lock = tmp_path / "package-lock.json"

    node_modules.mkdir()
    package_lock.touch()

    [type, last_modified] = get_package_type_and_last_modified(node_modules)
    assert last_modified > timestamp
    assert type == "npm-lock"


def test_get_package_json_last_modified_with_yarn_lock(tmp_path: pathlib.Path):
    timestamp = time.time()
    node_modules = tmp_path / "node_modules"
    package_lock = tmp_path / "yarn.lock"

    node_modules.mkdir()
    package_lock.touch()

    [type, last_modified] = get_package_type_and_last_modified(node_modules)
    assert last_modified > timestamp
    assert type == "yarn-lock"


def test_get_package_json_last_modified_with_no_lock(tmp_path: pathlib.Path):
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    [type, last_modified] = get_package_type_and_last_modified(node_modules)
    assert last_modified is 0
    assert type is None
