# movies/factories.py
import factory
from django.contrib.auth.models import User
from .models import Collection, Movie

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie
