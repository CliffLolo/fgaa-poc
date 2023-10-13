from setuptools import setup, find_packages

setup(
    name='fga-poc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'fga-poc=cli.src.cli:app',
        ],
    },
)
