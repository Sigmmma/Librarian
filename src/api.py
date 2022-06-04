'''
The programmatic entry point for Librarian functions.

CLI apps, GUI apps, and third-party apps should mostly interact with Librarian
through these functions.
'''
from pathlib import Path
from typing import Callable

import yaml

from serialize import serializeFile

def exportToYaml(paths: 'list[Path]'):
    'paths is an array of Paths either to files or directories'
    for file in filesInPathList(paths):
        data = serializeFile(file)
        outfile = Path(str(file) + '.yaml')
        with open(outfile, 'w') as f:
            f.write(yaml.safe_dump(data))

def filesInPathList(
    paths: 'list[Path]',
    include_filter: Callable[[Path], bool] = None
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
