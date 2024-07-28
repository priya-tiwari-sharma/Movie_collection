from django.contrib import admin
from .models import Collection, Movie

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('uuid','title', 'description', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('uuid','user',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'genres', 'uuid')
    search_fields = ('title', 'description', 'genres')
    list_filter = ('genres',)
