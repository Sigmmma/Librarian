'''
Functions for serializing Halo files out to YAML and binary.
'''
from pathlib import Path

from construct import Container, EnumIntegerString, Struct

import router

# TODO Need patterns that we treat differently
# - paddingx
# - do_not_use_x
# TODO all transforms should happen in one place so we don't lose track of them

def serializeFile(file: Path):
    construct_struct = router.getStructForFile(file)
    parsed_file = construct_struct.parse_file(file)

    yaml_data_dict = _buildYamlDict(construct_struct, parsed_file)
    return yaml_data_dict

def _buildYamlDict(struct: Struct, parsed):
    '''
    Builds a serialization-safe dict of the human-readable fields of the
    given struct data.

    Binary data under a specific size threshold is included in the YAML data.

    Since YAML fields export in alphabetical order, the names of invisible or
    otherwise user-ignored tag fields are slightly transformed so they sort
    to the bottom of the YAML file.
    '''
    yaml_data = dict()

    # Building on a private value isn't great, but this is the only way
    # to get the list of fields on a Construct struct.
    for field_name in struct._subcons:
        # TODO this is where we'd apply special handling for specific fields
        value = getattr(parsed, field_name)
        yaml_data[field_name] = _buildStructValue(value)

    return yaml_data

def _buildStructValue(value):
    '''Special-case transforms to make struct values serialization-safe.
    This function is built to be called recursively for nested structures.
    '''
    if isinstance(value, Container):
        data = dict()
        for key, val in value.items():
            # _io is an internal Construct thing we don't care about
            if key != '_io':
                data[key] = _buildStructValue(val)
        return data

    if isinstance(value, EnumIntegerString):
        return str(value)

    return value
