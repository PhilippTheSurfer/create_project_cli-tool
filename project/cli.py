import typer
from project.commands import fastapi as fastapi_command
from project.commands import angular as angular_command

app = typer.Typer(help="A CLI tool for setting up and managing projects.")

app.command(help="Setup FastAPI Project Structure")(fastapi_command.fastapi)
app.command(help="Setup Angular Project Structure")(angular_command.angular)

if __name__ == "__main__":
    app()

