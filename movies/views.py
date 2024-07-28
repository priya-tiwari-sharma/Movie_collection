# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Collection
from .serializers import CollectionSerializer
from .services import fetch_movies
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .paginations import CustomPagination


class MovieListView(APIView):
    def get(self, request, format=None):
        url = "https://demo.credy.in/api/v1/maya/movies/"
        try:
            data = fetch_movies(url)
            
            if data:
                # paginator = CustomPagination()
                # paginated_data = paginator.paginate_queryset(data, request)
                # return paginator.get_paginated_response(paginated_data)
                return Response(data, status=status.HTTP_200_OK)
            return Response({"error": "No data received"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
            collections = Collection.objects.filter(user=request.user)
            serializer = CollectionSerializer(collections, many=True)
            return Response({"is_success": True,"data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'collection_uuid':serializer.data["uuid"]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, uuid, format=None):
        try:
            collection = Collection.objects.get(user=request.user, uuid=uuid)
            serializer = CollectionSerializer(collection)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid, format=None):
        try:
            collection = Collection.objects.get(user=request.user, uuid=uuid)
            serializer = CollectionSerializer(collection, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid, format=None):
        try:
            collection = Collection.objects.get(user=request.user, uuid=uuid)
            collection.delete()
            return Response({"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)

class RequestCountView(APIView):
    def get(self, request, format=None):
        request_count = cache.get('request_count', 0)
        return Response({'requests': request_count}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        cache.set('request_count', 0)
        return Response({'message': 'Request count reset successfully'}, status=status.HTTP_200_OK)
