#!/bin/python3
from enum import Enum
from typing import Dict
import requests

class MenuOptions(Enum):
    CREATE_ACCOUNT = 1
    LOGIN = 2
    REQUEST_SECRET = 3
    CREATE_SECRET = 4
    VIEW_VOTES = 5
    VIEW_YOUR_REQUEST = 6
    EXIT = 7

VOTE_COUNT_YAY_THRESHOLD = 2

REGISTER_URL = "http://localhost:8080/register/"
LOGIN_URL = "http://localhost:8080/login/"
CREATE_SECRET_URL = "http://localhost:8081/create-secret/"
REQUEST_SECRET_URL = "http://localhost:8081/request-secret/"
REQUEST_SECRET_NAMES_URL = "http://localhost:8081/get-secret-names/"

START_VOTE_URL = "http://localhost:8081/start-vote/"
GET_VOTES_URL = "http://localhost:8081/get-votes/"
GIVE_VOTE_URL = "http://localhost:8081/give-vote/"

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
        request_secret(user["access_token"], user["username"])
    elif choice == MenuOptions.CREATE_SECRET.value:
        create_secret(user["access_token"])
    elif choice == MenuOptions.VIEW_VOTES.value:
        view_votes(user["access_token"], user["username"])
    elif choice == MenuOptions.VIEW_YOUR_REQUEST.value:
        view_user_requests(user["access_token"], user["username"])
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
    print(MenuOptions.VIEW_VOTES.value, "View votes")
    print(MenuOptions.VIEW_YOUR_REQUEST.value, "View your request")
    print(MenuOptions.EXIT.value, "Exit")
    choice = input("Enter your choice: ")

    if choice.isdigit():
        return int(choice)
    else:
        return -1


def request_secret(access_token: str, username: str) -> None:
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
            "access_token": access_token,
            "username": username,}
    response = requests.post(START_VOTE_URL,
                             json=data)

    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Failed to access secret:",  response.json()["error"])


def view_user_requests(access_token: str, username: str) -> None:
    """
    View the requests by sending a GET request to the server.
    """
    print("\nViewing your requests:")

    # Send the access token to the server
    data = {"access_token": access_token}
    response = requests.get(GET_VOTES_URL,
                            data=data)

    if response.status_code != 200:
        print("Failed to view requests:",  response.json()["error"])
        return

    votes = response.json()["votes"]

    if len(votes) == 0:
        print("No requests found.")
        return

    for vote in votes:
        if username == vote["username"]:
            vote_str = "Your request for secret \"" + vote["secret_name"] + \
                       "\" has " + str(vote["yay_count"]) + " yays and " + \
                        str(vote["nay_count"]) + " nays."
            if vote["yay_count"] >= VOTE_COUNT_YAY_THRESHOLD:
                print("Would you like to view the secret for \"" + \
                      vote["secret_name"] + \
                      "\" (y/n)")
                view_secret = ""
                while view_secret.lower() != "y" and view_secret.lower() != "n":
                    view_secret = input()
                    if view_secret.lower() == "y":
                        data = {"secret_name": vote["secret_name"],
                                "access_token": access_token,
                                "username": username}
                        response = requests.post(REQUEST_SECRET_URL,
                                                json=data)
                        if response.status_code == 200:
                            print("Secret:", response.json()["secret"])
                        else:
                            print("Failed to view secret:",  response.json()["error"])
                        break
                    elif view_secret.lower() == "n":
                        break


def view_votes(access_token: str, username: str) -> None:
    """
    View the votes by sending a GET request to the server.
    """
    print("\nViewing votes:")

    # Send the access token to the server
    data = {"access_token": access_token}
    response = requests.get(GET_VOTES_URL,
                            data=data)

    if response.status_code != 200:
        print("Failed to view votes:",  response.json()["error"])
        return

    votes = response.json()["votes"]

    # Find votes that the user has not voted on
    available_vote_found = False
    for i, vote in enumerate(votes):
        if username in vote["voted_users"]:
            # User has already voted on this vote
            continue
        if username in vote["username"]:
            # User cannot vote on their own vote
            continue
        vote_str = "Vote started by \"" + vote["username"] + \
                   "\" for secret \"" + vote["secret_name"] + "\""
        print(i+1, vote_str)
        available_vote_found = True

    if not available_vote_found:
        print("No available votes to vote on.")
        return

    choice = 0
    while(True):
        choice = input("\nEnter a vote number to vote or \"exit\" to exit: ")

        if choice.isdigit():
            choice = int(choice)
        elif choice.lower() == "exit":
            return -1
        else:
            print("Invalid choice. Please try again.")
            continue

        # Check if valid choice was made
        if choice < 1 or choice > len(votes):
            print("Invalid choice. Please try again.")
            continue

        # Ask if the user wants to vote yay or nay
        vote_choice = input("Enter \"yay\" or \"nay\" to vote: ")
        if vote_choice.lower() == "yay":
            vote = "yay"
        elif vote_choice.lower() == "nay":
            vote = "nay"
        else:
            print("Invalid vote. Please try again.")
            continue

        # Send the vote
        data = {"secret_name": votes[choice-1]["secret_name"],
                "vote": vote,
                "access_token": access_token,
                "username": username}
        response = requests.post(GIVE_VOTE_URL,
                                json=data)

        if response.status_code == 200:
            print("Vote cast successfully.")
        else:
            print("Failed to cast vote:",  response.json()["error"])
        break

if __name__ == "__main__":
    main()
