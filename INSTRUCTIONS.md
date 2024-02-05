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
2. Install requirements via:
```sh
$ pip3 install -r requirements.txt
```
