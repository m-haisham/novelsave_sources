from setuptools import setup, find_packages

import novelsave_sources

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='novelsave_sources',
    version=novelsave_sources.__version__,
    author="Schicksal",
    description="This is a collection of webnovel scrapers",
    author_email='mhaisham79@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
    ],
    license="APACHE-2.0 license",
    keywords='webnovel novel lightnovel scraper',
    url='https://github.com/mHaisham/novelsave_sources',
    packages=find_packages(),
    python_requires='>=3.6',
)