from typing import Any
from pathlib import Path
import json


def _join_path(*args: Any) -> Path:
    to_append = '/'.join(args[1:])
    return Path.joinpath(Path(args[0]), to_append)


def _resolve_file(*path: Any, **filename: Any) -> dict:
    if len(path) == 1 and len(filename) == 0:
        file = path[0]
    else:
        file = _join_path(*path, filename['filename'])
    return file


def read_json(*path: Any, **filename: Any) -> dict[str, str]:
    file = _resolve_file(*path, **filename)

    with open(file, 'r') as f:
        data = json.load(f)

    return data


def read_header() -> dict[str, str]:
    return read_json(Path.cwd(), filename='headers.json')
