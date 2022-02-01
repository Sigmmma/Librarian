# Bare-bones Librarian POC
import yaml
from structs.savegame import savegame, EnumIntegerString

save = savegame.parse_file('structs/savegame.bin')

obj = {
    'ameta': {
        'type': 'savegame',
        'tag': None,
        'file': 'savegame.bin',
        'engine': 'h1ce',
        'version': 'dev',
    },
    'data': {},
}
for field in savegame._subcons:
    value = getattr(save, field)

    if isinstance(value, EnumIntegerString):
        value = str(value)

    obj['data'][field] = value

# Write this out to a file
yaml_string = yaml.safe_dump(obj)

# Later on, loading from same file
loaded = yaml.safe_load(yaml_string)
# We know to use savegame from loaded.ameta.type
savegame.build_file(loaded['data'], 'test.bin')
