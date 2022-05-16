from pathlib import Path

LIBRARIAN_PROJECT_DIR = 'librarian'
LIBRARIAN_FILTER_FILE = 'libinclude'

class LibConfig:
    '''Centralizes Librarian configuration in one place.
    Determines relevant project directories, such as the tags directory.
    '''
    def __init__(self,
        console: bool=False,
        dryrun: bool=False,
        # TODO maybe allow specifying filterlist directly
        filter: Path=None,
        silent: bool=False,
        tagdir: Path=None,
        yamldir: Path=None
    ):
        # Let us track where config comes from, for information purposes
        self._locations = dict()

        # Prioritize explicitly provided config values first.
        # Also, declare these up front so we can cleanly add docstrings. Thanks Python.
        self.console = console
        'Enables printing YAML to the console instead of a file.'
        self.dryrun = dryrun
        'Enables printing operations to the console without actually doing anything'
        self.filterlist = []
        'Filters for which files to include and ignore'
        self.filterpath = None
        'Path to the librarian project filter file'
        self.libdir = None
        'Path to the librarian root directory'
        self.silent = silent
        'Disables printing output to the console'
        self.tagdir = None
        'Path to the Halo tags directory'
        self.yamldir = None
        'Path to the YAML output directory'

        # Fall back on default config values based on project structure
        self.libdir = _determineLibrarianDir()

        self.filterpath, self._locations['filter'] = _determineUsedPath(
            self.libdir,
            filter,
            # For project, assume filter file lives in "librarian" root dir
            lambda root: root.joinpath(LIBRARIAN_FILTER_FILE),
            None,
        )

        self.filterlist = _loadFiltersFromFile(self.filterpath)

        self.tagdir, self._locations['tagdir'] = _determineUsedPath(
            self.libdir,
            tagdir,
            # For project, assume Halo's "tags" dir is next to "librarian"
            lambda root: root.parent.joinpath('tags'),
            # By default, export alongside the input file
            Path.cwd(),
        )

        self.yamldir, self._locations['yamldir'] = _determineUsedPath(
            self.libdir,
            yamldir,
            # For project, export YAML to "librarian" root dir
            lambda root: root,
            # By default, export alongside the input file
            Path.cwd(),
        )

    def __str__(self):
        def labelToStr(label):
            if label == 'cli':
                return 'Specified by user'
            if label == 'project':
                return 'Found relative to librarian root'
            if label == 'default':
                return 'Defaulting to current directory'
        text = '' + \
            f'Librarian root: {self.libdir}\n' + \
            f'Tags dir:       {self.tagdir}\n' + \
            f'                \t({labelToStr(self._locations["tagdir"])})\n' + \
            f'YAML dir:       {self.yamldir}\n' + \
            f'                \t({labelToStr(self._locations["yamldir"])})\n' + \
            f'Filter:         {self.filterpath}\n'
        if self.filterpath:
            text += f'                \t({labelToStr(self._locations["filter"])})'
            text += '\n'.join([f'\t{filter}' for filter in self.filterlist])
        return text

def _determineUsedPath(
    root_path: Path,
    cli_path: Path,
    root_transform,
    default_path: Path
):
    '''Determine the first "available" path, including a label describing it.
    root_transform is a lambda function that transforms the root_path. This lets
    us check that root_path exists before transforming it.
    '''
    # If the user specified a CLI path, try to use it even if it isn't good.
    cli_path = Path(cli_path) if cli_path else None
    if cli_path:
        return cli_path, 'cli'

    # We determine project paths ourselves, so scrutinize them a little harder.
    if root_path:
        project_path = root_transform(root_path)
        if project_path and project_path.exists():
            return project_path, 'project'

    # Finally fall back on a default, if we can.
    if default_path and default_path.exists():
        return default_path, 'default'
    # If all else fails, return None to ensure things are sanitizing Paths.
    return None, None

def _determineLibrarianDir() -> Path:
    '''Search for the nearest Librarian directory, kind of like .git'''
    cur_dir = Path.cwd()
    prev_dir = None
    while cur_dir != prev_dir:
        lib_dir = cur_dir.joinpath(LIBRARIAN_PROJECT_DIR)
        if lib_dir.exists():
            return lib_dir
        prev_dir = cur_dir
        cur_dir = cur_dir.parent

def _loadFiltersFromFile(file: Path):
    'Load filters into a list, stripping extra whitespace and comments'
    try:
        with open(file, 'r') as filter_file:
            lines = filter_file.readlines()
            lines = [line.rstrip() for line in lines]
            lines = [line for line in lines if not line.startswith('#')]
            return lines
    except:
        # TODO log a warning here
        return []
