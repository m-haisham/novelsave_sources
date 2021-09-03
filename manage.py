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

    return sorted(sources, key=lambda s: s.base_urls)


def mako_dest_file(mako_file: Path) -> Path:
    return mako_file.parent / mako_file.stem


def render(mako_file: Path, **kwargs):
    text = Template(filename=str(mako_file)).render(**kwargs)

    rendered_file = mako_file.parent / mako_file.stem
    with rendered_file.open('w') as f:
        f.write(text.replace('\r', ''))

    print(f'{mako_file.relative_to(BASE_DIR)} -> {rendered_file.relative_to(BASE_DIR)}')


@click.group()
def cli():
    pass


@cli.command(name='compile')
def compile_():
    """Compile all mako files"""
    sources = get_subclasses_in_module(NOVEL_MODULE, Source)
    meta_sources = get_subclasses_in_module(METADATA_MODULE, MetaSource)

    render(NOVEL_INIT_MAKO, sources=sources)
    render(METADATA_INIT_MAKO, meta_sources=meta_sources)
    render(README_MAKO, sources=sources, meta_sources=meta_sources)


if __name__ == '__main__':
    cli()
