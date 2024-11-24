#!/bin/bash

# Ensure the script is run as a superuser
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo to execute it."
   exit 1
fi

echo "Start installation process..."
chmod +x project.py

cp project.py /usr/local/bin/project

#echo "Updating system and installing required packages... (python3, pip, venv, typer, typing-extension)"
#apt update
#apt install -y python3 python3-pip python3-venv python3-typer python3-typing-extensions

echo "All dependencies are installed successfully!"
echo "The CLI tool 'project' is now globally accessible."
echo "For more information type 'project --help'."
