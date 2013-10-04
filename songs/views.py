from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from songs.models import Genre, Song

class IndexView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.order_by('-score', 'title')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(IndexView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['genre_list'] = Genre.objects.all().order_by('name')
		return context

class DetailView(generic.DetailView):
	model = Song
	template_name = 'songs/detail.html'

class GenreView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		genre = Genre.objects.filter(id=self.kwargs['genre'])
		return Song.objects.filter(genre=genre).order_by('-score', 'title')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(GenreView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['genre_list'] = Genre.objects.all().order_by('name')
		context['genre'] = Genre.objects.get(id=self.kwargs['genre'])
		return context

class YearView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		year = self.kwargs['year']
		return Song.objects.filter(year__year=year).order_by('-score', 'title')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(YearView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['genre_list'] = Genre.objects.all().order_by('name')
		return context

def submit(request):
	genre_list = Genre.objects.all().order_by('name')
	try:
		title = request.POST['title']
		artist = request.POST['artist']
		year = request.POST['year'] + '-01-01'
		genre = get_object_or_404(Genre, pk=request.POST['genre'])
		if title == '' or artist == '' or year == '':
			return render(request, 'songs/index.html', {
				'song_list': Song.objects.order_by('-score', 'title'),
				'genre_list': genre_list,
				'error_message': "Your submission was invalid.",
			})
	except (KeyError, Genre.DoesNotExist):
		# Redisplay the song submission form.
		return render(request, 'songs/index.html', {
			'genre_list': genre_list,
			'error_message': "Your submission was invalid.",
		})
	else:
		s = Song(title=title, artist=artist, year=year, genre=genre)
		s.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('songs:index'))

def rate(request, pk, rating, genre):
	genre_list = Genre.objects.all().order_by('name')
	try:
		song = get_object_or_404(Song, pk=pk)
	except (KeyError, Song.DoesNotExist):
		# Redisplay the song submission form.
		if genre == '0':
			return render(request, 'songs/index.html', {
				'genre_list': genre_list,
				'error_message': "Your rating was invalid.",
			})
		else:
			return render(request, 'songs/index.html', {
				'genre': Genre.objects.get(id=genre),
				'genre_list': genre_list,
				'error_message': "Your rating was invalid.",
			})
	else:
		if rating == '1':
			song.down += 1
		elif rating == '2':
			song.up += 1
		song.score = song.up - song.down
		song.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		if genre == '0':
			return HttpResponseRedirect(reverse('songs:index'))
		else:
			return HttpResponseRedirect(reverse('songs:genre', kwargs={'genre': genre}))
