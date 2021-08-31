from setuptools import setup, find_packages

requirements = []
with open('requirements/common.txt', 'r') as f:
    requirements += f.readlines()
with open('requirements/prod.txt', 'r') as f:
    requirements += [l for l in f.readlines() if not l.startswith('-r')]

setup(
    install_requires=requirements,
    packages=find_packages(),
)
