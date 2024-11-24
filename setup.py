from setuptools import setup, find_packages

setup(
    name='project-cli',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'typer',
        'typing-extensions',
    ],
    entry_points={
        'console_scripts': [
            'project=project.cli:app',
        ],
    },
    author='Philipp Lehmann',
    author_email='',
    description='A CLI tool for setting projects structures.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PhilippTheServer/create_project_cli-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache-2.0 license',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

