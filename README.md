# TL;DR

The Repository contains two important files:
- `project.py`
- `install.sh`

The *project.py* is a cli-tool written with the `typer` Python libary. 

*Install.sh* can be executed to install all dependencies to run the cli-tool.
It will also move the *project.py* to `/usr/local/bin/project` that it can be run as a cli command.


## Get Started

```
git clone git@github.com:PhilippTheSurfer/create_project_cli-tool.git
cd create_project_cli-tool
chmod +x install.sh
sudo ./install.sh
```

## Dependencies

- Python3.8 or higher
- Python-venv
- Python-typer
- Python-pip

> [!NOTE]
> The `install.sh` Script is going to attempt to install the dependencies. It has to be executed as **sudo**.


---

# In the Future:

- Angular Project Setup
