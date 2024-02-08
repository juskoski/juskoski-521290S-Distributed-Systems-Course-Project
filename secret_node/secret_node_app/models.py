from django.db import models


class SecretModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.secret
