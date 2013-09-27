from django.shortcuts import render, get_object_or_404
from django.views import generic

from songs.models import Genre, Song

class IndexView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.order_by('-score')
