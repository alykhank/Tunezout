from django.shortcuts import render, get_object_or_404
from django.views import generic

from songs.models import Genre, Song

class IndexView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.order_by('-score')

class DetailView(generic.DetailView):
	model = Song
	template_name = 'songs/detail.html'

class YearView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.filter(year__year=self.kwargs['year']).order_by('-score')
