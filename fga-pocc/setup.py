from setuptools import setup, find_packages

setup(
    name='{{ cookiecutter.pypi_name }}',
    version='{{ cookiecutter.version }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    license='MIT',
    author='{{ cookiecutter.full_name }}',
    description='{{ cookiecutter.project_short_description }}',
    long_description=__doc__,
    # name='fga-poc',
    # version='0.1.0',
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
