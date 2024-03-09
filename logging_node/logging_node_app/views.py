from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

@api_view(["POST"])
def PostLog(request: Request) -> Response:
    print(request.data)
    return Response(status=status.HTTP_200_OK)
