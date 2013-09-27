from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from songs.models import Genre, Song

class IndexView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.order_by('-score')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(IndexView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['genre_list'] = Genre.objects.all().order_by('-name')
		return context

class DetailView(generic.DetailView):
	model = Song
	template_name = 'songs/detail.html'

class YearView(generic.ListView):
	template_name = 'songs/index.html'

	def get_queryset(self):
		return Song.objects.filter(year__year=self.kwargs['year']).order_by('-score')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(YearView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the genres
		context['genre_list'] = Genre.objects.all().order_by('-name')
		return context

def submit(request):
	genre_list = Genre.objects.all().order_by('-name')
	try:
		title = request.POST['title']
		artist = request.POST['artist']
		year = request.POST['year'] + '-01-01'
		genre = get_object_or_404(Genre, pk=request.POST['genre'])
	except (KeyError, Genre.DoesNotExist):
		# Redisplay the song submission form.
		return render(request, 'songs/index.html', {
			'genre_list': genre_list,
			'error_message': "Your submission was invalid.",
		})
	else:
		try:
			s = Song(title=title, artist=artist, year=year, genre=genre)
			s.save()
		except (ValueError):
			# Redisplay the song submission form.
			return render(request, 'songs/index.html', {
				'genre_list': genre_list,
				'error_message': "Your submission was invalid.",
			})
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('songs:index'))
