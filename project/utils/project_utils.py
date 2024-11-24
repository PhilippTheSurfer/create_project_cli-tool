import os
import subprocess
import time
import typer
from pathlib import Path
from project.utils.misc import get_current_path

def create_fastapi_structure(repo_name: str):
    # Create docker-compose.yml
    compose_content = f"""\
services:
  {repo_name}:
    build: ./src
    expose:
      - "8000"
    networks:
      frontproxy_fnet:
        ipv4_address: 172.20.20.90
      backend:
    restart: unless-stopped
    container_name: {repo_name}

networks:
  frontproxy_fnet:
    external: true
  backend:
    name: {repo_name}_backend
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
            f.write(f"# Init file for {sub_dir}")

    # Create tests directory and test file
    typer.secho("Creating tests directory...", fg=typer.colors.YELLOW)
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_api.py", "w") as f:
        f.write("# Test cases for the FastAPI project")

def create_angular_structure(repo_name: str, build_name: str):
    typer.secho("Adding Docker Prod Setup.", fg=typer.colors.YELLOW)
    compose_content = f"""\
services:
  {repo_name}:
    build: ./src
    container_name: {repo_name}
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
    name: {repo_name}_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

    dockerfile_content = f"""\
# Stage 1: Compile and Build angular codebase
FROM node:20.11.0-alpine as build

LABEL authors="Your Name"

WORKDIR /usr/local/app

COPY ./app /usr/local/app/

# Install dependencies and build the application
RUN npm install -g npm@10.4.0 && \\
    npm install -g @angular/cli && \\
    npm install && \\
    npm run build

# Stage 2: Serve app with nginx server
FROM nginx:latest

COPY --from=build /usr/local/app/dist/{build_name}/browser /usr/share/nginx/html

EXPOSE 80
"""
    os.makedirs("src", exist_ok=True)
    with open("src/Dockerfile", "w") as f:
        f.write(dockerfile_content)

def build_and_run_docker_dev(repo_name: str, build_name: str):
    typer.secho("Docker Dev Setup created.", fg=typer.colors.YELLOW)
    docker_dev_content = f"""\
services:
  {repo_name}:
    image: {build_name}
    volumes:
      - ./:/usr/local/app
    ports:
      - "4200:4200"
#    command: ["npm install"]
    container_name: {repo_name}
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
    name: {repo_name}_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
    with open("docker-compose.dev.yml", "w") as f:
        f.write(docker_dev_content)

    dockerfile_dev_content = f"""\
# Use Node.js 20.11.0-bullseye as the base image
FROM node:20.11.0-bullseye

# Set authors label
LABEL authors="Your name"

# Set the working directory
WORKDIR /usr/local/app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install npm and Angular CLI globally
RUN npm install -g npm@10.4.0 @angular/cli

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Add node_modules/.bin to PATH
ENV PATH /usr/local/app/node_modules/.bin:$PATH

# Expose the port for Angular
EXPOSE 4200

# Start the Angular development server
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_dev_content)

    subprocess.run(["docker", "build", "-t", build_name, "."])
    typer.secho("Docker build executed", fg=typer.colors.YELLOW)

    subprocess.run(["docker", "compose", "-f", "docker-compose.dev.yml", "up", "-d"])
    typer.echo("Waiting for 20 seconds...")
    time.sleep(20)  # Pause the program for 20 seconds
    subprocess.run(["docker", "compose", "-f", "docker-compose.dev.yml", "down"])

    current_path = get_current_path()
    docker_dev_file = Path(f"{current_path}/docker-compose.dev.yml")

    try:
        docker_dev_file.unlink()
        typer.echo(f"File '{docker_dev_file}' has been deleted.")
    except Exception as e:
        typer.echo(f"Error: File not deleted. Reason: {e}")
        raise typer.Exit(code=1)

    typer.echo("Continuing with the setup...")

    docker_dev2_content = f"""\
services:
  {repo_name}:
    image: {build_name}
    volumes:
      - ./:/usr/local/app
    ports:
      - "4200:4200"
    command: ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
    container_name: {repo_name}
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
    name: {repo_name}_backend
    driver: bridge
    driver_opts:
      com.docker.network.enable_ipv6: "false"
"""
    with open("docker-compose.dev.yml", "w") as f:
        f.write(docker_dev2_content)

    subprocess.run(["docker", "compose", "-f", "docker-compose.dev.yml", "up", "-d"])
    typer.secho("Docker Dev Setup successful", fg=typer.colors.GREEN)

