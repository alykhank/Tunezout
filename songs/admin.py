from django.contrib import admin
from django.contrib.auth.models import User
from songs.models import Genre, Song, TwitterProfile

class SongInline(admin.TabularInline):
	model = Song

class GenreAdmin(admin.ModelAdmin):
	search_fields = ['name']
	inlines = [SongInline]

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'year', 'genre', 'up', 'down', 'score', 'approved')
	actions = ['make_approved']
	search_fields = ['title', 'artist', 'year']
	list_filter = ['genre']
	date_hierarchy = 'year'

	def make_approved(self, request, queryset):
		rows_updated = queryset.update(approved=True)
		if rows_updated == 1:
			message_bit = "1 song was"
		else:
			message_bit = "%s songs were" % rows_updated
		self.message_user(request, "%s successfully marked as approved." % message_bit)
	make_approved.short_description = "Mark selected songs as approved"

class TwitterProfileAdmin(admin.ModelAdmin):
	list_display = ('screen_name',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(TwitterProfile, TwitterProfileAdmin)
