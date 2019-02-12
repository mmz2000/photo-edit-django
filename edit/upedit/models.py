from django.db import models


class pic (models.Model):
    on_delete = models.CASCADE
    name = models.CharField(max_length = 500)
    edited = models.BooleanField(default=False)
