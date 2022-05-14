from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

class CmdHelpFormatter(ArgumentDefaultsHelpFormatter):
    '''
    Ridiculous nonsense to rename the top-level "positional arguments" section
    to "commands".
    Seriously, why is this necessary for some basic print control?
    '''
    def start_section(self, heading) -> None:
        if heading == 'positional arguments':
            super().start_section('commands')
        else:
            super().start_section(heading)

parser = ArgumentParser(
    description='Converts Halo tags to and from YAML',
    prog='librarian',
    formatter_class=CmdHelpFormatter,
)

parser.add_argument('-v', '--version', action='version', version='0.0.0-dev')

subparser = parser.add_subparsers(dest='command')

cmd_config = subparser.add_parser('config', description='''
    Prints Librarian config for the current environment, including where that
    configuration is coming from.''',
)
cmd_export = subparser.add_parser('export', description='Exports tags to YAML')
cmd_import = subparser.add_parser('import', description='Imports tags from YAML')

if __name__ == '__main__':
    args = parser.parse_args()

    if (args.command is None):
        parser.print_help()

