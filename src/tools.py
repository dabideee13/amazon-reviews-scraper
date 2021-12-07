from typing import Any
from pathlib import Path
import json


def pipe(raw_input: Any, *functions, **functions_with_args) -> Any:
    """
    Creates a pipeline (or chain) for every function. Basically,
    this function initially accepts a data then passes it to the next
    function, then the output passes it to the next function as input.
    Args:
        raw_input (Any): Any input, could be list, tuple, etc.
    Other Parameters:
        param1 (Callable): Any function with only one argument.
        param2 (Callable): Any function with only one argument.
        ...
    Keyword Args:
        key1 (Callable): Any function with one or more than one
            arguments with arguments written as list.
        key2 (Callable): Any function with one or more than one
            arguments with arguments written as list.
        ...
    Returns:
        Any: Any output as a result of the functions it goes through.
    """

    # TODO: Needs more improvement for robustness.
    # Currently it will only work for some cases.
    output = raw_input

    if functions:
        for function in functions:
            output = function(output)

    if functions_with_args:
        for function, args_list in functions_with_args.items():
            output = eval(function)(output, *args_list)

    return output


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
