from django.urls import path
from .views import MovieListView,CollectionListCreateView, CollectionDetailView,RegisterView,RequestCountView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('collection/', CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collection/<uuid:uuid>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
]
