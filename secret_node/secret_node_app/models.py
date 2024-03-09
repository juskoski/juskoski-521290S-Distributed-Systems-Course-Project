from django.db import models


class SecretModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.secret


class VoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    yay_count = models.IntegerField()
    nay_count = models.IntegerField()
    username = models.CharField(max_length=100)
    secret_name = models.CharField(max_length=100)
    voted_users = models.JSONField(default=list)

    def __str__(self):
        return self.vote
