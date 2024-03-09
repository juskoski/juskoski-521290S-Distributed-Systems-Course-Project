#!/bin/python3
import requests

REGISTER_URL = "http://localhost:8080/register/"
LOGIN_URL = "http://localhost:8080/login/"

access_token = ""
username = ""
password = ""


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
        login()
    else:
        print("Failed to create account:",  response.json()["error"])


def handle_menu_choice(choice: int) -> None:
    """
    Handle the user's choice from the menu.
    """
    if choice == 1:
        create_account()
    elif choice == 2:
        login()
        pass
    elif choice == 3:
        pass
        #request_secret()
    elif choice == 4:
        #create_secret()
        pass
    elif choice == 5:
        exit()
    else:
        print("Invalid choice. Please try again.")


def login() -> None:
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
    else:
        print("Failed to login:",  response.json()["error"])


def main() -> None:
    """
    Main function to run the client application.
    """
    print("Welcome to Distributed Secrets Management System!")
    while (True):
        handle_menu_choice(print_menu())


def print_menu() -> int:
    """
    Print the menu and return the user's choice.
    """
    print("\nPlease select an option from the following menu:")
    print("1. Create an account")
    print("2. Login")
    print("3. Request access to a secret")
    print("4. Create a secret")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice.isdigit():
        return int(choice)
    else:
        return -1


if __name__ == "__main__":
    main()
