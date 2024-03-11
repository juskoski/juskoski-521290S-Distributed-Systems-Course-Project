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

### Running the system
0. Enter the WSL, start the virtual environment, make sure pip requirements are installed
1. Run the Login node:
```sh
# Terminal 1
$ python3 login_node/manage.py makemigrations
$ python3 login_node/manage.py migrate
$ python3 login_node/manage.py runserver 8080
```
2. Run the Secret node:
```sh
# Termianl 2
$ python3 secret_node/manage.py makemigrations
$ python3 secret_node/manage.py migrate
$ python3 secret_node/manage.py runserver 8081
```
3. Run the Monitoring node
```sh
# Terminal 3
$ python3 logging_node/manage.py makemigrations
$ python3 logging_node/manage.py migrate
$ python3 logging_node/manage.py runserver 8082
```

### Accessing the system
Run
```sh
$ python3 client.py
```
to start a session.

### Traffic evaluation
You can evaluate how much traffic the service can withstand using `traffic_evaluation.py`. Adjust the `CLIENT_AMOUNT` and `KEY_AMOUNT_PER_CLIENT`.

#### Using the service via HTTP
1. Create new user
    - Endpoint: http://localhost:8080/register/
    - Parameters: {"username", "YOUR NAME", "password", "YOUR PASS"}
    - Returns `HTTP 200` if user was created, otherwise `HTTP 400`
2. Login as a valid user
    - Endpoint: http://localhost:8081/login/
    - Parameters: {"username", "YOUR NAME", "password", YOUR PASS"}
    - Returns `access_token` if login was successful, otherwise `HTTP 400`
3. Post a new secret
    - Endpoint: http://localhost:8080/create-secret/
    - Parameters: {"secret_name": "SECRET", "secret": "VALUE", "access_token": "`access_token`""}'
    - Returns `HTTP 200` if the secret was created, `HTTP 409` if the secret already exists, and `HTTP 400` in other scenarios.
4. Request a secret using `access_token`:
    - Endpoint: http://localhost:8080/request-secret/
    - Parameters: {"secret_name": "SECRET", "access_token": "`access_token`"}
    - Returns `HTTP 200` if the `access_token` is valid and the secret is found, otherwise `HTTP 400`
