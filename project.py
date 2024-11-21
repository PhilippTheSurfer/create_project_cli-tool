#!/usr/bin/env python3

import os
import subprocess
import typer
import time
from typer import Optional
from typing_extensions import Annotated
from pathlib import Path


def create_repo() -> str:
    repo_name = typer.prompt("Enter the repository name")
    if not repo_name.strip():
        typer.secho("❌ Repository name cannot be empty. Exiting.", fg=typer.colors.RED, bold=True)
        raise typer.Exit()

    # Prompt for base path
    base_path = typer.prompt("Enter the relative path where the repository should be created", default=".")
    full_path = os.path.join(os.path.abspath(base_path), repo_name)

    # Create directory structure
    typer.secho(f"Creating directory at {full_path}...", fg=typer.colors.YELLOW)
    os.makedirs(full_path, exist_ok=True)

    # Change to the repository directory
    os.chdir(full_path)

    return repo_name


def init_git_repo() -> bool:
    # Initialize Git repository
    typer.secho("Initializing Git repository...", fg=typer.colors.YELLOW)
    try:
        subprocess.run(["git", "init"], check=True)

        gitignore_content = """\
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/
# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
"""
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        typer.echo("Added Python .gitignore to the repo.")

    except subprocess.CalledProcessError:
        typer.echo("Error: Failed to initialize Git repository.")
        raise typer.Exit(code=1)

    return True


app = typer.Typer(help="A CLI tool for setting up and managing projects.")

@app.command(help="Setup FastAPI Project Structure")
def fastapi():
    """
    Set up a new FastAPI project with a clean, standard structure.
    """
    typer.secho("🚀 Welcome to the FastAPI Project Setup Tool! 🚀", fg=typer.colors.CYAN, bold=True)

    # setup repository
    create_repo()

    init_git_repo()

    # Create virtual environment
    typer.secho("Creating virtual environment...", fg=typer.colors.YELLOW)
    subprocess.run(["python3", "-m", "venv", "env"], check=True)
    #subprocess.run(["bash", "-c", "source venv/bin/activate && echo 'Virtual environment activated.'"])

    # Create docker-compose.yml
    compose_content = """\
services:
  api:
    build: ./src
    expose:
      - "8000"
    networks:
      frontproxy_fnet:
        ipv4_address: 172.20.20.90
      backend:
    restart: unless-stopped
    container_name: api

networks:
  frontproxy_fnet:
    external: true
  backend:
    name: api_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
    typer.secho("Creating docker-compose.yml...", fg=typer.colors.YELLOW)
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

    # Create src directory and Dockerfile
    typer.secho("Creating src directory and Dockerfile...", fg=typer.colors.YELLOW)
    os.makedirs("src", exist_ok=True)
    dockerfile_content = """\
FROM python:3.9-slim

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    with open("src/Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # Create app directory and files
    typer.secho("Setting up FastAPI application structure...", fg=typer.colors.YELLOW)
    os.makedirs("src/app", exist_ok=True)
    requirements_content = """\
fastapi
uvicorn[standard]
pydantic
typing_extensions
"""
    with open("src/app/requirements.txt", "w") as f:
        f.write(requirements_content)

    main_content = """\
from fastapi import FastAPI
import logging

# Configure logging once at the entry point
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Example router (you can replace this with your actual router)
# app.include_router(any_router.router)
"""
    with open("src/app/main.py", "w") as f:
        f.write(main_content)

    # Create subdirectories with __init__.py
    for sub_dir in ["models", "functions", "routers"]:
        dir_path = os.path.join("src/app", sub_dir)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "__init__.py"), "w") as f:
            f.write("# Init file for " + sub_dir)

    # Create tests directory and test file
    typer.secho("Creating tests directory...", fg=typer.colors.YELLOW)
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_api.py", "w") as f:
        f.write("# Test cases for the FastAPI project")

    typer.secho(f"✅ FastAPI project '{repo_name}' has been created at {full_path}.", fg=typer.colors.GREEN, bold=True)


@app.command(help="just for the help command")
def angular(docker: Annotated[Optional[str], typer.Argument()] = None):
    if docker is None:
        
        repo_name=create_repo()
        init_git_repo()
        
        # Run `ng new` command
        typer.echo("Running Angular CLI to initialize the project...")
        try:
            subprocess.run(["ng", "new", repo_name, "--directory", ".", "--defaults"], check=True)
        except subprocess.CalledProcessError:
            typer.echo("Error: Failed to create the Angular project using the Angular CLI.")
            raise typer.Exit(code=1)
        
        typer.secho("Adding Docker Prod Setup.")
        compose_content="""\
services:
  angular-project:
    build: ./src
    container_name: angular-project
    restart: unless-stopped
    networks:
      frontproxy_fnet:
        ipv4_address: 172.20.20.90
      backend:
    logging:
      driver: "json-file"
      options:
        max-size: "1024m"

networks:
  frontproxy_fnet:
    external: true
  backend:
    name: angular-project_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"

"""
        with open("docker-compose.yml", "w") as f:
            f.write(compose_content)

        dockerfile_content = """\
# Stage 1: Compile and Build angular codebase
FROM node:20.11.0-alpine as build

LABEL authors="Your Name"

WORKDIR /usr/local/app

COPY ./app /usr/local/app/

# Install dependencies and build the application
RUN npm install -g npm@10.4.0 && \
    npm install -g @angular/cli && \
    npm install && \
    npm run build

# Stage 2: Serve app with nginx server
FROM nginx:latest

COPY --from=build /usr/local/app/dist/{angular-project-name}/browser /usr/share/nginx/html

EXPOSE 80
"""
        with open("src/Dockerfile", "w") as f:
            f.write(dockerfile_content)

    else:
        docker_dev_content="""\
services:
  anular-project:
    image: anular-project:latest
    volumes:
      - ./app:/usr/local/app
    ports:
      - "4200:4200"
    command: ["npm install"]
    container_name: anular-project
    restart: unless-stopped
    networks:
      frontproxy_fnet:
        ipv4_address: 172.20.20.91
      backend:
    logging:
      driver: "json-file"
      options:
        max-size: "1024m"

networks:
  frontproxy_fnet:
    external: true
  backend:
    name: anular-project_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
        with open("docker-compose.dev.yml", "w") as f:
            f.write(docker_dev_content)

        dockerfile_dev_content="""\
# Use Node.js 20.11.0-alpine as the base image
FROM node:20.11.0-bullseye

# Set authors label
LABEL authors="Your name"

# Set the working directory
WORKDIR /usr/local/app

# Copy only package files to install dependencies
COPY ./app/package*.json ./

# Install npm and Angular CLI globally
RUN npm install -g npm@10.4.0 @angular/cli && \
    npm install

# Expose the port for Angular
EXPOSE 4200

# Start the Angular development server
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
"""
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_dev_content)
        typer.secho("Docker Dev Setup craeted.")

        build_name=f"{repo_name}:latest"

        subprocess.run(["docker", "build", "-t", build_name, "."])
        subprocess.run(["docker", "compose", "docker-compose.dev.yml", "up", "-d"])
        typer.echo("Waiting for 60 seconds...")
        time.sleep(60)  # Pause the program for 60 seconds
        subprocess.run(["docker", "compose", "docker-compose.dev.yml", "down"])

        docker_dev_file = f"{repo_name}/docker-compose.dev.yml"
        try:
            docker_dev_file.unlink()
            typer.echo(f"File '{docker_dev_file}' has beemn deleted.")
        except Exception as e:
            typer.echo(f"Error: File not deleted. Reason: {e}")
            raise typer.Exit(code=1)

        typer.echo("Continuing with the setup...")

        docker_dev2_content="""\
services:
  angular-project:
    image: angular-project:latest
    volumes:
      - ./ai-internal_yggdrasil_sw/app:/usr/local/app
    ports:
      - "4200:4200"
    command: ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
    container_name: angular-project
    restart: unless-stopped
    networks:
      frontproxy_fnet:
        ipv4_address: 172.20.20.91
      backend:
    logging:
      driver: "json-file"
      options:
        max-size: "1024m"

networks:
  frontproxy_fnet:
    external: true
  backend:
    name: angular-project_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
        with open("docker-compose.dev.yml", "w") as f:
            f.write(docker_dev2_content)

        subprocess.run(["docker", "compose", "docker-compose.dev.yml", "up", "-d"])
        typer.secho("Docker Dev Setup successfull")


if __name__ == "__main__":
    app()
