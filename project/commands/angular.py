import subprocess
import typer
from project.utils.git_utils import create_repo, init_git_repo
from project.utils.project_utils import create_angular_structure, build_and_run_docker_dev
from project.utils.misc import to_lowercase

def angular(docker: bool = typer.Option(False, '--docker', help='Include Docker setup')):
    """
    Set up a new Angular project with optional Docker support.
    """
    repo_name = create_repo()
    init_git_repo()

    build_name = to_lowercase(f"{repo_name}:latest")

    # Run `ng new` command
    typer.echo("Running Angular CLI to initialize the project...")
    try:
        subprocess.run(["ng", "new", repo_name, "--directory", ".", "--defaults"], check=True)
    except subprocess.CalledProcessError:
        typer.echo("Error: Failed to create the Angular project using the Angular CLI.")
        raise typer.Exit(code=1)

    create_angular_structure(repo_name, build_name)

    if docker:
        build_and_run_docker_dev(repo_name, build_name)

