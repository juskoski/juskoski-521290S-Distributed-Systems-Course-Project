from django.db import models


class LoggingModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action
