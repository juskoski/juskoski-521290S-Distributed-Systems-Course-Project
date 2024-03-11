#!/bin/python3
import os
import requests
import time
import threading

CLIENT_AMOUNT = 10
KEY_AMOUNT_PER_CLIENT = 10
THREAD_COUNT = 10

REGISTER_URL = "http://localhost:8080/register/"
LOGIN_URL = "http://localhost:8080/login/"
CREATE_SECRET_URL = "http://localhost:8081/create-secret/"

bot_clients = {}


def create_clients() -> None:
    """
    Create bot clients
    """
    start_time = time.time()
    registration_times = []
    login_times = []
    for i in range(CLIENT_AMOUNT):
        # Send the username and password to the server
        random_str = os.urandom(16).hex()
        username = "bot_client" + random_str
        password = "password" + random_str
        data = {"username": username, "password": password}
        start_time_bot = time.time()
        response = requests.post(REGISTER_URL, json=data)
        end_time_bot = time.time()

        # Login to get the access token
        response = requests.post(LOGIN_URL, json=data)
        registration_times.append(end_time_bot - start_time_bot)

        token = response.json()["token"]

        # Store the bot client's username, password and token
        start_time_bot = time.time()
        bot_clients[i] = {"username": username, "password": password, "token": token}
        end_time_bot = time.time()
        login_times.append(end_time_bot - start_time_bot)
        print("Bot client: " + username + " registered and logged in time " + str(end_time_bot - start_time_bot) + " seconds")
    end_time = time.time()
    print("Time taken to create bot clients: " + str(end_time - start_time) + " seconds")
    print("Average time taken to create a bot client: " + str((end_time - start_time) / CLIENT_AMOUNT) + " seconds")
    print("Average time taken to register a bot client: " + str(sum(registration_times) / CLIENT_AMOUNT) + " seconds")
    print("Average time taken to login a bot client: " + str(sum(login_times) / CLIENT_AMOUNT) + " seconds")


def create_keys() -> None:
    """
    Create random keys for the bot clients
    """
    start_time = time.time()
    for i in range(CLIENT_AMOUNT):
        username = "bot_client" + bot_clients[i]["username"]
        start_time_bot = time.time()
        for j in range(KEY_AMOUNT_PER_CLIENT):
            # Send the key to the server
            key = os.urandom(32).hex()
            #print("Bot client: " + username + " created key: " + key)
            headers = {"Authorization": "Bearer " + bot_clients[i]["token"]}
            data = {"secret_name": key, "secret": key, "access_token": bot_clients[i]["token"]}
            response = requests.post(CREATE_SECRET_URL, headers=headers, json=data)
        end_time = time.time()
        print("Time taken to create " + str(KEY_AMOUNT_PER_CLIENT) + " keys for bot client: " + username + " is " + str(end_time - start_time_bot) + " seconds")
    print("Average time to create " + str(KEY_AMOUNT_PER_CLIENT) + \
          " keys for bot clients: " + str((end_time - start_time) / CLIENT_AMOUNT) + \
          " seconds")


def main() -> None:
    # Create thread for creating bot clients
    t = threading.Thread(target=create_clients)
    t.start()

    # Wait for the bot clients to be created
    t.join()

    # Create threads for each bot client
    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=create_keys)
        threads.append(t)
        t.start()


if __name__ == "__main__":
    main()