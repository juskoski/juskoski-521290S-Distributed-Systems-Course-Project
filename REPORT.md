# Industry track
Corporate

## Project Title
Distributed Secrets Management with Multi-Party Approval

## About the project
The Distributed Secrets Management with Multi-Party Approval system's central idea is to ensure that sensitive information, or secrets, can only be accessed when several authorized individuals agree (common consensus). This way no single person can access crucial data without approval from their peers.

## Implemented components:
![Arcihtecture diagram](/img/DistributedSystemArchitectureFinal.png)
The system consists of
#### Client nodes
Client nodes offer a CLI tool for communicating with the system. They provide a simple way to create accounts and login, create secrets and request access to secret, view ongoing votes and view if your client has been granted access to a secret.

#### Secret node
Secret node is responsible for offering endpoints for
- Creating secrets
- Viewing secrets
- Granting access for secrets

#### Login node
Login node is responsible for account creation and login activities.

#### Monitor node
Monitor node is responsible for collecting events from the Secret node and the Login node.

#### Principles
- Secure Key Management
    Keys are securely stored and handled
- Resource naming
    User data is handled without the user knowing about the name (or format) of the stored data


## Built with:
The service is built with Django and Python. Communication happens mainly over HTTP. Some nodes communicate with databases via SQL.

## Getting Started:
Requirements:
- Ubuntu WSL2 running on Windows

0. Download the repository:
```sh
$ git clone https://github.com/juskoski/juskoski-521290S-Distributed-Systems-Course-Project.git
```
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

## Results of the tests:
The script `traffic_evaluation.py` can be used to evaluate how much traffic the system can withstand.  
The file has three parameters you can control:
- `CLIENT_AMOUNT` configures how many bot clients are created
- `KEY_AMOUNT_PER_CLIENT` configures how many clients are created per bot client
- `THREAD_COUNT` configures how many threads are run

The script will run as follows:
1. Create `CLIENT_AMOUNT` of bot accounts and logs those in
2. Spawn `THREAD_COUNT` of threads
3. In each thread, `KEY_AMOUNT_PER_CLIENT` will be created and posted to the backend

For example, `CLIENT_AMOUNT = 10`, `KEY_AMOUNT_PER_CLIENT = 10`, `THREAD_COUNT = 10` will create total of 1000 keys.

### Results
To evaluate how much traffic the system can stand, traffic was simulated with:
- 10 bot accounts
- 100 key creations per bot account
- 1, 5, 10, 15, 20 threads

We measured the amount of errors and the avereage time to create n keys. 

From the graphs we can see that when the amount of threads increase (concurrency) the amount of errors and the average time to create 100 keys increase. The backend did not crash and remained operational. The errors were caused by read/write operations clashing and trying to access database at the concurrently.

![Error count vs increasing concurrency](/img/ErrorCountVsIncreasingConcurrency.png)
![Average time to create 100 keys vs increasing concurrency](/img/TimeToCreate100KeysVsConcurrency.png)

The system could be made more scalable by introducing load balancers, threads, and managing access to databases more gracefully.
