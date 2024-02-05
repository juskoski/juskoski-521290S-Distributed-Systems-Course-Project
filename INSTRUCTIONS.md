# Instructions
This document contains instructions on how to setup the development environment and run individual nodes.

## Server Nodes
Server nodes (such as Login and Secret node) will run as Django applications.

### Development environment
- Ubuntu WSL2 running on Windows

### Steps
1. Create a new venv and activate it via:
```sh
$ python3 venv -m /path/to/venv
$ source /path/to/venv/bin/activate
```
2. Install pip requirements via:
```sh
$ pip3 install -r requirements.txt
```
3. Install python3-django via apt:
```sh
$ sudo apt install python3-django
```
