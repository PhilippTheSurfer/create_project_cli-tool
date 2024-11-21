#!/usr/bin/env python3

import os
import subprocess
import typer

app = typer.Typer(help="A CLI tool for setting up and managing projects.")

@app.command(help="Setup FastAPI Project Structure")
def fastapi():
    """
    Set up a new FastAPI project with a clean, standard structure.
    """
    typer.secho("🚀 Welcome to the FastAPI Project Setup Tool! 🚀", fg=typer.colors.CYAN, bold=True)

    # Prompt for repository name
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

    # Initialize Git repository
    typer.secho("Initializing Git repository...", fg=typer.colors.YELLOW)
    subprocess.run(["git", "init"], check=True)

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


@app.command()
def angular(help="just for the help command"):
    typer.secho("Not implemented yet")


if __name__ == "__main__":
    app()
