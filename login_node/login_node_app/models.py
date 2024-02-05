from django.db import models


class UserDataModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.username
