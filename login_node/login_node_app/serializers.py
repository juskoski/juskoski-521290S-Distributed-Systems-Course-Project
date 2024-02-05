from login_node_app.models import UserDataModel
from rest_framework import serializers


class UserDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDataModel
        fields = ["username", "password"]
