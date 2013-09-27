from django.contrib import admin
from songs.models import Genre, Song

class SongInline(admin.TabularInline):
	model = Song

class GenreAdmin(admin.ModelAdmin):
	inlines = [SongInline]

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'year', 'genre', 'up', 'down', 'score')

admin.site.register(Genre, GenreAdmin)
admin.site.register(Song, SongAdmin)
