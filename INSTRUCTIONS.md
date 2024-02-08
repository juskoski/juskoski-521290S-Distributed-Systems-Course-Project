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
```

### Running the system
0. Enter the WSL, start the virtual environment, make sure pip requirements are installed
1. Run the Login node:
```sh
$ python3 login_node/manage.py makemigrations
$ python3 login_node/manage.py migrate
$ python3 login_node/manage.py runserver 8080
```
2. Run the Secret node:
```sh
$ python3 secret_node/manage.py makemigrations
$ python3 secret_node/manage.py migrate
$ python3 secret_node/manage.py runserver 8081
```

#### Requesting secrets
1. Create new user
    - Endpoint: http://localhost:8080/register/
    - Parameters: {"username", "YOUR NAME", "password", "YOUR PASS"}
    - Returns `HTTP 200` if user was created, otherwise `HTTP 400`
2. Login as a valid user
    - Endpoint: http://localhost:8081/login/
    - Parameters: {"username", "YOUR NAME", "password", YOUR PASS"}
    - Returns `access_token` if login was successful, otherwise `HTTP 400`
3. Request a secret using `access_token`:
    - Endpoint: http://localhost:8080/request-secret/
    - Parameters: {"secret_name": "SECRET", "access_token": "`access_token`"}
    - Returns `HTTP 200` if the `access_token` is valid and the secret is found, otherwise `HTTP 400`
