# movies/tests.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from movies.models import Collection
from .factories import UserFactory, CollectionFactory, MovieFactory
from django.core.cache import cache

@pytest.mark.django_db
def test_register():
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.data

@pytest.mark.django_db
def test_login():
    user = UserFactory(username='testuser', password='password123')
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    access_token = response.data['access_token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.get(reverse('movie-list'))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_collection():
    user = UserFactory(username='testuser', password='password123')
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    access_token = response.data['access_token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    response = client.post(reverse('collection-list-create'), {
        'title': 'My Collection',
        'description': 'A description of my collection',
        'movies': []
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert 'collection_uuid' in response.data

@pytest.mark.django_db
def test_get_collection():
    user = UserFactory(username='testuser', password='password123')
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    access_token = response.data['access_token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    collection = CollectionFactory(user=user)
    
    response = client.get(reverse('collection-detail', kwargs={'pk': collection.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == collection.title

@pytest.mark.django_db
def test_update_collection():
    user = UserFactory(username='testuser', password='password123')
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    access_token = response.data['access_token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    collection = CollectionFactory(user=user)
    
    response = client.put(reverse('collection-detail', kwargs={'pk': collection.pk}), {
        'title': 'Updated Title',
        'description': 'Updated description',
        'movies': []
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Title'

@pytest.mark.django_db
def test_delete_collection():
    user = UserFactory(username='testuser', password='password123')
    client = APIClient()
    response = client.post(reverse('register'), {'username': 'testuser', 'password': 'password123'})
    access_token = response.data['access_token']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    collection = CollectionFactory(user=user)
    
    response = client.delete(reverse('collection-detail', kwargs={'pk': collection.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Collection.objects.filter(pk=collection.pk).count() == 0

@pytest.mark.django_db
def test_request_count():
    client = APIClient()
    response = client.get(reverse('request-count'))
    assert response.status_code == status.HTTP_200_OK
    initial_count = response.data['requests']
    
    client.get(reverse('request-count'))
    response = client.get(reverse('request-count'))
    assert response.data['requests'] == initial_count + 1

    response = client.post(reverse('request-count/reset'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'request count reset successfully'

    response = client.get(reverse('request-count'))
    assert response.data['requests'] == 0

@pytest.mark.django_db
def test_fetch_movies():
    client = APIClient()
    response = client.get(reverse('movie-list'))
    assert response.status_code == status.HTTP_200_OK
    assert 'count' in response.data
    assert 'data' in response.data
