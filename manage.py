from pathlib import Path
from mako.template import Template
from collections import namedtuple

import click

from novelsave_sources.sources.novel import sources
from novelsave_sources.sources.metadata import meta_sources

BASE_DIR = Path(__file__).parent

README_MAKO = BASE_DIR / 'README.md.mako'
README_FILE = BASE_DIR / 'README.md'


@click.group()
def cli():
    pass


@cli.command(name='compile')
def compile_():
    """Compile all mako files"""
    text: str = Template(filename=str(README_MAKO)).render(sources=sources, metasources=meta_sources)
    with README_FILE.open('w') as f:
        f.write(text.replace('\r', ''))

    print(f'{README_MAKO.relative_to(BASE_DIR)} -> {README_FILE.relative_to(BASE_DIR)}')


if __name__ == '__main__':
    cli()
