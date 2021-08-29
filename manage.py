import importlib
import inspect
from pathlib import Path
from typing import List

import click
from mako.template import Template

from novelsave_sources.sources.metadata.metasource import MetaSource
from novelsave_sources.sources.novel.source import Source

BASE_DIR = Path(__file__).parent

README_MAKO = BASE_DIR / 'README.md.mako'
README_FILE = BASE_DIR / 'README.md'

NOVEL_MODULE = 'novelsave_sources.sources.novel.'
NOVEL_INIT_MAKO = BASE_DIR / 'novelsave_sources/sources/novel/__init__.py.mako'

METADATA_MODULE = 'novelsave_sources.sources.metadata.'
METADATA_INIT_MAKO = BASE_DIR / 'novelsave_sources/sources/metadata/__init__.py.mako'


@click.group()
def cli():
    pass


def get_subclasses_in_module(__pkg: str, __cls: type) -> List[type]:
    sources = []
    for path in Path(__pkg.replace('.', '/')).iterdir():
        if not path.is_file():
            continue
        elif not path.suffix == '.py':
            continue
        elif path.name == '__init__.py':
            continue

        module = importlib.import_module(__pkg + path.stem)
        for name, member in inspect.getmembers(module, inspect.isclass):
            if issubclass(member, __cls) and member is not __cls:
                sources.append(member)

    return sorted(sources, key=lambda s: s.__name__)


def mako_destination_file(mako_dir: Path) -> Path:
    return mako_dir.parent / mako_dir.stem


def write_rendered(mako_file: Path, text: str):
    with mako_destination_file(mako_file).open('w') as f:
        f.write(text.replace('\r', ''))

    print(f'{mako_file.relative_to(BASE_DIR)} -> {mako_destination_file(mako_file).relative_to(BASE_DIR)}')


@cli.command(name='compile')
def compile_():
    """Compile all mako files"""
    sources = get_subclasses_in_module(NOVEL_MODULE, Source)
    text = Template(filename=str(NOVEL_INIT_MAKO)).render(sources=sources)
    write_rendered(NOVEL_INIT_MAKO, text)

    meta_sources = get_subclasses_in_module(METADATA_MODULE, MetaSource)
    text = Template(filename=str(METADATA_INIT_MAKO)).render(meta_sources=meta_sources)
    write_rendered(METADATA_INIT_MAKO, text)

    text: str = Template(filename=str(README_MAKO)).render(sources=sources, meta_sources=meta_sources)
    write_rendered(README_MAKO, text)


if __name__ == '__main__':
    cli()


