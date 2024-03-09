from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from secret_node_app.models import SecretModel
from rest_framework import status
import requests

# Remember to start the Login node before running the following code
VERIFY_TOKEN_URL = "http://localhost:8080/verify-token/"


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

    # Check if the secret exists
    if not SecretModel.objects.filter(name=request.data["secret_name"]).exists():
        return Response(
            {"error": "Secret does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Get the secret from the database
    secret = SecretModel.objects.get(name=request.data["secret_name"])

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

    # Return the secret
    return Response({"secret": secret.secret}, status=status.HTTP_201_CREATED)
