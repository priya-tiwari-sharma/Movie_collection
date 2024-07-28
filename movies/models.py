from django.db import models
from django.contrib.auth.models import User
import uuid

class Collection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    uuid = models.CharField(max_length=36, unique=True)
    collections = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
