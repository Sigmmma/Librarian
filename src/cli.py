from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
from sys import exit

from api import exportToYaml
from config import LibConfig

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
cmd_export = subparser.add_parser('export', description='Exports Halo tags to YAML')
cmd_import = subparser.add_parser('import', description='Imports Halo tags from YAML')

cmd_export.add_argument('-c', '--console', action='store_true',
    help='output YAML to the console instead of to a file'
)

for cmd in [cmd_export, cmd_import]:
    if cmd is cmd_export:
        filetype = 'tag'
    if cmd is cmd_import:
        filetype = 'YAML'

    cmd.add_argument('files', type=Path, nargs='*',
        help=f'A {filetype} file, or directory containing {filetype} files'
    )

    cmd.add_argument('-d', '--dryrun', action='store_true',
        help='print operations without actually doing anything'
    )
    cmd.add_argument('-s', '--silent', action='store_true',
        help='do not print anything'
    )

for cmd in [cmd_config, cmd_export, cmd_import]:
    cmd.add_argument('-f', '--filter', type=Path,
        help='specify a filter file for excluding files and/or directories'
    )
    cmd.add_argument('-o', '--outdir', type=Path,
        help='specify directory to output processed files to')

if __name__ == '__main__':
    args = parser.parse_args()

    if (args.command is None):
        parser.print_help()
        exit(0)

    config = LibConfig(
        console=getattr(args, 'console', False),
        dryrun=getattr(args, 'dryrun', False),
        filter=args.filter,
        silent=getattr(args, 'silent', False),
        tagdir= args.outdir if args.command == 'export' else None,
        yamldir=args.outdir if args.command == 'import' else None,
    )

    if args.command == 'config':
        print(config)
        exit(0)

    if args.command == 'export':
        exportToYaml(args.files)
