import os
import subprocess
import typer
from project.utils.git_utils import create_repo, init_git_repo, add_python_gitignore
from project.utils.project_utils import create_fastapi_structure
from project.utils.misc import get_current_path

def fastapi():
    """
    Set up a new FastAPI project with a clean, standard structure.
    """
    typer.secho("🚀 Welcome to the FastAPI Project Setup Tool! 🚀", fg=typer.colors.CYAN, bold=True)

    # Setup repository
    repo_name = create_repo()

    init_git_repo()

    add_python_gitignore()

    # Create virtual environment
    typer.secho("Creating virtual environment...", fg=typer.colors.YELLOW)
    subprocess.run(["python3", "-m", "venv", "env"], check=True)

    # Set up FastAPI project structure
    create_fastapi_structure(repo_name)

    typer.secho(f"✅ FastAPI project '{repo_name}' has been created successfully.", fg=typer.colors.GREEN, bold=True)

