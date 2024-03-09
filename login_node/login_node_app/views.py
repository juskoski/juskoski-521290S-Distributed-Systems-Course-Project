from login_node_app.models import UserDataModel
from login_node_app.serializers import UserDataModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import crypto_utils
import os
import requests

# Define parameters for username and password
USERNAME_MIN_LEN = 8
PASSWORD_MIN_LEN = 8

LOGGING_NODE_URL = "http://localhost:8082/logging/"


@api_view(["GET"])
def GetUserDetails(request: Request) -> Response:
    users = UserDataModel.objects.all()
    serializer = UserDataModelSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def CreateUser(request: Request) -> Response:
    # Verify that the request contains the required fields
    if "username" not in request.data or "password" not in request.data:
        return Response({"error": "username and password are required"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify username and password meet minimum length requirements
    if len(request.data["username"]) < USERNAME_MIN_LEN or \
            len(request.data["password"]) < PASSWORD_MIN_LEN:
        return Response(
            {"error":"username and password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST)

    # Verify username does not already exist
    if UserDataModel.objects.filter(username=request.data["username"]).exists():
        return Response({"error": "username already exists"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Hash the password
    request.data["password"] = \
        crypto_utils.hash_password(request.data["password"].encode()).decode()

    # Log the event
    log_data = {
        "username": request.data["username"],
        "action": "create user",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    serializer = UserDataModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def LoginUser(request: Request) -> Response:
    if "username" not in request.data or "password" not in request.data:
        return Response({"error": "username and password are required"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Fetch the user's credentials from database
    user = UserDataModel.objects.filter(username=request.data["username"])

    # Verify the user exists
    if not user.exists():
        return Response({"error": "invalid username or password"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the provided password against the stored hash
    if not crypto_utils.verify_password(user.first().password.encode(),
                                        request.data["password"].encode()):
        return Response({"error": "invalid username or password"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Generate an authentication token from os.urandom()
    token = os.urandom(16).hex()

    # Store the token in the database
    user = user.first()
    user.token = token
    user.save()

    # Log the event
    log_data = {
        "username": request.data["username"],
        "action": "login",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    return Response({"token": token}, status=status.HTTP_200_OK)


@api_view(["POST"])
def VerifyToken(request: Request) -> Response:
    # Verify that the request contains access_token
    if "access_token" not in request.data:
        return Response({"error": "access_token is required"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verify the access token exists
    user = UserDataModel.objects.filter(token=request.data["access_token"])

    if not user.exists():
        return Response({"error": "invalid access token"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Log the event
    log_data = {
        "action": "Verified access token",
    }
    requests.post(LOGGING_NODE_URL, data=log_data)

    return Response(
        {"message": "valid access token"}, status=status.HTTP_200_OK
    )
