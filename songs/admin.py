from django.contrib import admin
from songs.models import Genre, Song

class SongInline(admin.TabularInline):
	model = Song

class GenreAdmin(admin.ModelAdmin):
	search_fields = ['name']
	inlines = [SongInline]

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'year', 'genre', 'up', 'down', 'score', 'approved')
	search_fields = ['title', 'artist', 'year']
	list_filter = ['genre']
	date_hierarchy = 'year'

admin.site.register(Genre, GenreAdmin)
admin.site.register(Song, SongAdmin)
