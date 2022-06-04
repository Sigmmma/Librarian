'''
The programmatic entry point for Librarian functions.

CLI apps, GUI apps, and third-party apps should mostly interact with Librarian
through these functions.
'''
from pathlib import Path
from typing import Callable

from serialize import serializeFile

# TODO modify this to take a single file too?
def exportToYaml(paths: 'list[Path]'):
    '''Exports all the relevant files in the given list of paths.
    Each path can point to a directory or a file. Directories are
    recursively resolved into relevant files.
    '''
    for file_path in filesInPathList(paths):
        out_map = serializeFile(file_path)
        for file_name, data in out_map.items():
            with open(file_path.parent.joinpath(file_name), 'w') as file:
                file.write(data)

def filesInPathList(
    paths: 'list[Path]',
    include_filter: Callable[[Path],bool] = None
):
    '''Recursively generates a list of files from a list of paths.
    A filter can be specified to optionally restrict the result set.
    '''
    if include_filter is None:
        include_filter = lambda _: True

    for path in paths:
        if path.is_dir():
            for file in path.rglob('*'):
                if file.is_file() and include_filter(file):
                    yield file
        elif include_filter(path):
            yield path
