'''
The programmatic entry point for Librarian functions.

CLI apps, GUI apps, and third-party apps should mostly interact with Librarian
through these functions.
'''
from pathlib import Path
from typing import Callable

import yaml

import router

def exportToYaml(paths: 'list[Path]'):
    'paths is an array of Paths either to files or directories'
    for file in filesInPathList(paths):
        struct = router.getStructForFile(file)
        parsed = struct.parse_file(file)
        data = buildYamlData(struct, parsed)
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

# TODO extract this to its own module
from construct import Container, EnumIntegerString

def buildYamlData(struct, parsed):
    data = dict()

    # Building on private values? Oh yeah!
    for field in struct._subcons:
        data[field] = buildStructValue(getattr(parsed, field))

    return data

def buildStructValue(value):
    if isinstance(value, Container):
        return buildContainer(value)
    if isinstance(value, EnumIntegerString):
        value = str(value)
    return value

def buildContainer(container):
    data = dict()
    for key,val in container.items():
        # Better believe we're relying on more private values.
        if key != '_io':
            data[key] = buildStructValue(val)
    return data