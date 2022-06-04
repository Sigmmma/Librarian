'''
Contains the map of all defined file types and structs used to manipulate them.
Provides functions for selecting the appropriate struct for a given file.
'''
from pathlib import Path

from construct import Struct
from structs.header import header
from structs.actor import actor

HEADER_BYTES = 64
GROUP_TO_STRUCT = dict({
    'actor': actor,
})

def getStructForFile(path: Path) -> Struct:
    'Returns the appropriate Construct struct that matches the given file'
    with open(path, 'rb') as f:
        data = f.read(HEADER_BYTES)

    parsed = header.parse(data)
    return GROUP_TO_STRUCT[parsed.group]

