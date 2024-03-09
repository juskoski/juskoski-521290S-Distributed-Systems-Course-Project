from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from secret_node_app.models import (
    SecretModel,
    VoteModel,
)
from rest_framework import status
import requests

# Remember to start the Login node before running the following code
VERIFY_TOKEN_URL = "http://localhost:8080/verify-token/"
LOGGING_NODE_URL = "http://localhost:8082/logging/"

VOTE_YAY_THRESHOLD = 2


@api_view(["GET"])
def GetVotes(request: Request) -> Response:
    # Verify the request contains a valid token
    if "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the token is valid
    token_data = {"access_token": request.data["access_token"]}
    response = requests.post(VERIFY_TOKEN_URL, data=token_data)

    # Return an error if the token is invalid
    if response.status_code != 200:
        return Response(
            {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Get all the votes from the database
    votes = VoteModel.objects.all()

    # Log the event
    log_data = {
        "action": "Get votes",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Return the votes
    return Response({"votes": list(votes.values())}, status=status.HTTP_200_OK)


@api_view(["POST"])
def GiveVote(request: Request) -> Response:
    # Verify the request contains a valid token
    if "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the token is valid
    token_data = {"access_token": request.data["access_token"]}
    response = requests.post(VERIFY_TOKEN_URL, data=token_data)

    # Return an error if the token is invalid
    if response.status_code != 200:
        return Response(
            {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify the request contains the name of the secret and the vote
    if "secret_name" not in request.data \
        or "username" not in request.data \
        or "vote" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Get the vote from the database
    vote_instance = \
        VoteModel.objects.get(secret_name=request.data["secret_name"])

    # Check if the user has already voted
    if request.data["username"] in vote_instance.voted_users:
        return Response(
            {"error": "User has already voted"},
            status=status.HTTP_409_CONFLICT
        )

    # Check the user is not voting for their own secret
    if request.data["username"] == vote_instance.username:
        return Response(
            {"error": "User cannot vote on their own secret"},
            status=status.HTTP_409_CONFLICT
        )

    # Update the vote
    if request.data["vote"] == "yay":
        vote_instance.yay_count += 1
    elif request.data["vote"] == "nay":
        vote_instance.nay_count += 1
    else:
        return Response(
            {"error": "Invalid vote"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Add the voter to the list of voted users
    vote_instance.voted_users.append(request.data["username"])

    # Save the vote to the database
    vote_instance.save()

    # Log the event
    log_data = {
        "username": request.data["username"],
        "action": "voted",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Return the vote
    return Response({
        "vote": {
            "secret_name": vote_instance.secret_name,
            "yay_count": vote_instance.yay_count,
            "nay_count": vote_instance.nay_count
        }
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
def StartVote(request: Request) -> Response:
    # Verify the request contains a valid token
    if "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the token is valid
    token_data = {"access_token": request.data["access_token"]}
    response = requests.post(VERIFY_TOKEN_URL, data=token_data)

    # Return an error if the token is invalid
    if response.status_code != 200:
        return Response(
            {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify the request contains the name of the secret and the vote
    if "secret_name" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    vote = VoteModel(username=request.data["username"],
                    secret_name=request.data["secret_name"],
                    yay_count=0,
                    nay_count=0)
    vote.save()

    # Log the event
    log_data = {
        "username": request.data["username"],
        "action": "started vote",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Start the vote
    return Response({"message": "Vote started"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def RequestAccessToSecret(request: Request) -> Response:
    # Verify the request contains name of the secret and a valid token
    if "secret_name" not in request.data or "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the token is valid
    token_data = {"access_token": request.data["access_token"]}
    response = requests.post(VERIFY_TOKEN_URL, data=token_data)

    # Return an error if the token is invalid
    if response.status_code != 200:
        return Response(
            {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify the vote has passed
    secret = SecretModel.objects.get(name=request.data["secret_name"])
    vote = VoteModel.objects.get(secret_name=request.data["secret_name"])
    if vote.yay_count < VOTE_YAY_THRESHOLD:
        return Response(
            {"error": "Vote has not passed"}, status=status.HTTP_409_CONFLICT
        )

    # Verify the vote starter is trying to access the secret
    if request.data["username"] != vote.username:
        return Response(
            {"error": "User cannot access secret"}, status=status.HTTP_409_CONFLICT
        )

    # Check if the secret exists
    if not SecretModel.objects.filter(name=request.data["secret_name"]).exists():
        return Response(
            {"error": "Secret does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Get the secret from the database
    secret = SecretModel.objects.get(name=request.data["secret_name"])

    # Delete the vote
    vote.delete()

    # Log the event
    log_data = {
        "username": request.data["username"],
        "action": "requested access to secret",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Return the secret
    return Response({"secret": secret.secret}, status=status.HTTP_200_OK)


@api_view (["POST"])
def CreateSecret(request: Request) -> Response:
    # Verify the request contains name of the secret and a valid token
    if "secret_name" not in request.data or "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the token is valid
    token_data = {"access_token": request.data["access_token"]}
    print("TOKEN DATA", token_data)
    response = requests.post(VERIFY_TOKEN_URL, data=token_data)

    # Return an error if the token is invalid
    if response.status_code != 200:
        return Response(
            {"error": response.json()["error"]},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Check if the secret already exists
    if SecretModel.objects.filter(name=request.data["secret_name"]).exists():
        return Response(
            {"error": "Secret already exists"},
            status=status.HTTP_409_CONFLICT
        )

    # Create the secret
    secret = SecretModel(name=request.data["secret_name"],
                         secret=request.data["secret"])

    # Save the secret to the database
    secret.save()

    # Log the event
    log_data = {
        "action": "created secret",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Return the secret
    return Response({"secret": secret.secret}, status=status.HTTP_201_CREATED)


@api_view (["POST"])
def GetSecretNames(request: Request) -> Response:
    # Verify the request contains a valid token
    if "access_token" not in request.data:
        # Return an error if the request is missing required fields
        return Response({"error": "Missing required fields"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Get all the secret names from the database
    secret_names = SecretModel.objects.values_list("name", flat=True)

    # Log the event
    log_data = {
        "action": "get secret names",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    # Return the secret names
    return Response({"secret_names": list(secret_names)},
                    status=status.HTTP_200_OK)
