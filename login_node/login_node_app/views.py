from login_node_app.models import UserDataModel
from login_node_app.serializers import UserDataModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import os


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

    # Verify username does not already exist
    if UserDataModel.objects.filter(username=request.data["username"]).exists():
        return Response({"error": "username already exists"},
                        status=status.HTTP_400_BAD_REQUEST)


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

    user = UserDataModel.objects.filter(username=request.data["username"],
                                        password=request.data["password"])
    if not user.exists():
        return Response({"error": "invalid username or password"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Generate an authentication token from os.urandom()
    token = os.urandom(16).hex()

    # Store the token in the database
    user = user.first()
    user.token = token
    user.save()

    return Response({"token": token}, status=status.HTTP_200_OK)
