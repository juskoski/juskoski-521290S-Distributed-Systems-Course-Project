from login_node_app.models import UserDataModel
from login_node_app.serializers import UserDataModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


@api_view(["GET"])
def GetUserDetails(request: Request) -> Response:
    users = UserDataModel.objects.all()
    serializer = UserDataModelSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
