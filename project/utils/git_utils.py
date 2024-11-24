import os
import subprocess
import typer
from project.templates.gitignore import PYTHON_GITIGNORE_CONTENT

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
    except subprocess.CalledProcessError:
        typer.secho("Error: Failed to initialize Git repository.")
        raise typer.Exit(code=1)
    return True

def add_python_gitignore() -> bool:
    typer.secho("Adding Python .gitignore to repository...", fg=typer.colors.YELLOW)
    try:
        with open(".gitignore", "w") as f:
            f.write(PYTHON_GITIGNORE_CONTENT)
        typer.secho("Added Python .gitignore to the repo.")
    except Exception as e:
        typer.secho(f"Error: Failed to add .gitignore. Reason: {e}")
        raise typer.Exit(code=1)
    return True

