#!/bin/python3
from enum import Enum
from typing import Dict
import requests

class MenuOptions(Enum):
    CREATE_ACCOUNT = 1
    LOGIN = 2
    REQUEST_SECRET = 3
    CREATE_SECRET = 4
    EXIT = 5

REGISTER_URL = "http://localhost:8080/register/"
LOGIN_URL = "http://localhost:8080/login/"
CREATE_SECRET_URL = "http://localhost:8081/create-secret/"
REQUEST_SECRET_URL = "http://localhost:8081/request-secret/"
REQUEST_SECRET_NAMES_URL = "http://localhost:8081/get-secret-names/"


def create_account() -> None:
    """
    Create a new account by sending a POST request to the server.
    """
    print("\nPlease enter your username and password to create an account.")
    username = ""
    while len(username) < 8:
        username = input("Username: ")
        if len(username) < 8:
            print("Username must be at least 8 characters long.")

    password = ""
    while len(password) < 8:
        password = input("Password: ")
        if len(password) < 8:
            print("Password must be at least 8 characters long.")

    print(f"Creating account for {username} with password {password}.")

    # Send the username and password to the server
    data = {"username": username, "password": password}
    response = requests.post(REGISTER_URL,
                             json=data)

    if response.status_code == 201:
        print("Account created successfully. Please login.")
    else:
        print("Failed to create account:",  response.json()["error"])


def create_secret(access_token: str) -> None:
    """
    Create a new secret by sending a POST request to the server.
    """
    print("\nPlease enter the name of the secret and the secret itself.")
    secret_name = ""
    while len(secret_name) < 5:
        secret_name = input("Secret name: ")
        if len(secret_name) < 5:
            print("Secret name must be at least 5 characters long.")

    secret = ""
    while len(secret) < 8:
        secret = input("Secret: ")
        if len(secret) < 8:
            print("Secret must be at least 8 characters long.")

    # Send the secret name and secret to the server
    data = {"secret_name": secret_name,
            "secret": secret,
            "access_token": access_token}
    response = requests.post(CREATE_SECRET_URL,
                             json=data)

    if response.status_code == 201:
        print("Secret created successfully.")
    else:
        print("Failed to create secret:",  response.json()["error"])


def handle_menu_choice(choice: int, user: Dict) -> None:
    """
    Handle the user's choice from the menu.
    """
    if choice == MenuOptions.CREATE_ACCOUNT.value:
        create_account()
    elif choice == MenuOptions.LOGIN.value:
        login(user)
    elif choice == MenuOptions.REQUEST_SECRET.value:
        request_secret(user["access_token"])
    elif choice == MenuOptions.CREATE_SECRET.value:
        create_secret(user["access_token"])
    elif choice == MenuOptions.EXIT.value:
        exit()
    else:
        print("Invalid choice. Please try again.")


def login(user: Dict) -> str:
    """
    Login to the server by sending a POST request with the username and
    password.
    """
    print("\nPlease enter your username and password to login.")
    username = input("Username: ")
    password = input("Password: ")

    # Send the username and password to the server
    data = {"username": username, "password": password}
    response = requests.post(LOGIN_URL,
                             json=data)

    if response.status_code == 200:
        print("Login successful.")
        access_token = response.json()["token"]
        user["username"] = username
        user["password"] = password
        user["access_token"] = access_token
        return access_token
    else:
        print("Failed to login:",  response.json()["error"])
        return ""


def main() -> None:
    """
    Main function to run the client application.
    """
    print("Welcome to Distributed Secrets Management System!")

    user = {"username": "", "password": "", "access_token": ""}

    while (True):
        handle_menu_choice(print_menu(), user)


def print_menu() -> int:
    """
    Print the menu and return the user's choice.
    """
    print("\nPlease select an option from the following menu:")
    print(MenuOptions.CREATE_ACCOUNT.value, "Create an account")
    print(MenuOptions.LOGIN.value, "Login")
    print(MenuOptions.REQUEST_SECRET.value, "Request access to a secret")
    print(MenuOptions.CREATE_SECRET.value, "Create a secret")
    print(MenuOptions.EXIT.value, "Exit")
    choice = input("Enter your choice: ")

    if choice.isdigit():
        return int(choice)
    else:
        return -1


def request_secret(access_token: str) -> None:
    """
    Request access to a secret by sending a POST request to the server.
    """
    print("\nPlease enter the name of the secret you want to access.")
    print("Available secrets:")
    secrets = {}
    data = {"access_token": access_token}
    response = requests.post(REQUEST_SECRET_NAMES_URL, data=data)
    if response.status_code == 200:
        secret_names = response.json()["secret_names"]
        for i, secret_name in enumerate(secret_names):
            print(i+1, secret_name)
            secrets[i+1] = secret_name

    choice = -1
    while choice == -1:
        choice = input("Select a secret: ")
        if choice.isdigit():
            choice = int(choice)
            if choice not in secrets.keys():
                print("Invalid secret name. Please try again.")
                choice = -1
                for i, secret_name in secrets.items():
                    print(i, secret_name)
        else:
            print("Invalid secret name. Please try again.")
            choice = -1

    # Send the secret name and access token to the server
    data = {"secret_name": secret_name,
            "access_token": access_token}
    response = requests.post(REQUEST_SECRET_URL,
                             json=data)

    if response.status_code == 200:
        print("Secret:", response.json()["secret"])
    else:
        print("Failed to access secret:",  response.json()["error"])


if __name__ == "__main__":
    main()
