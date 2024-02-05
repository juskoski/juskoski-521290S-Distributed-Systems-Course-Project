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

### Running Django application
Make sure you're in your WSL environment and the Python venv has been activated!
1. Run `cd` to `/login_node`
2. Make migrations via:
```sh
$ python3 manage.py makemigrations
```
3. Migrate via:
```sh
$ python3 manage.py migrate
```
4. Run the application via:
```sh
$ python3 manage.py runserver
```

The server is now running and you can make HTTP requests. For example:
```sh
$ curl -X POST -H "Content-Type: application/json" -d '{"username": "temp", "password":"s3cr3t"}' http://localhost:8000/register/ # Create new user
```
```sh
$  curl -X POST -H "Content-Type: application/json" -d '{"username": "temp", "password":"s3cr3t"}' http://localhost:8000/login/ # Login as existing user
```
```sh
$ curl "http://localhost:8000/users/" # Returns all users
=======
3. Install python3-django via apt:
```sh
$ sudo apt install python3-django
```
