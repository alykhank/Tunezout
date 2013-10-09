from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_managers

from songs.models import Genre, Song

def login(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		auth.login(request, user)
		messages.success(request, 'Logged in as ' + user.username + '.')
		return HttpResponseRedirect(reverse('songs:index'))
	else:
		messages.error(request, 'Invalid login.')
		return HttpResponseRedirect(reverse('songs:index'))

def logout(request):
	auth.logout(request)
	messages.success(request, 'Successfully logged out.')
	return HttpResponseRedirect(reverse('songs:index'))

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			messages.success(request, 'Successfully created user ' + new_user.username + '.')
			return HttpResponseRedirect(reverse('songs:index'))
	else:
		form = UserCreationForm()
	return render(request, 'songs/register.html', {'form': form})

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
		genre = Genre.objects.get(pk=request.POST['genre'])
		if title == '' or artist == '' or year == '':
			messages.error(request, 'Your submission was invalid.')
			return render(request, 'songs/index.html', {
				'song_list': Song.objects.order_by('-score', 'title'),
				'genre_list': genre_list,
			})
		elif len(title) > 100 or len(artist) > 100:
			messages.error(request, 'Your submission was too long.')
			return render(request, 'songs/index.html', {
				'song_list': Song.objects.order_by('-score', 'title'),
				'genre_list': genre_list,
			})
	except (KeyError, Genre.DoesNotExist):
		messages.error(request, 'Your submission was invalid.')
		# Redisplay the song submission form.
		return render(request, 'songs/index.html', {
			'song_list': Song.objects.order_by('-score', 'title'),
			'genre_list': genre_list,
		})
	else:
		s = Song(title=title, artist=artist, year=year, genre=genre)
		s.save()
		messages.success(request, 'You successfully submitted "' + title + '" by "' + artist + '" for approval.')
		subject = '[Tunezout] Song Submission: "' + title + '" by "' + artist + '"'
		message = '[' + datetime.now().ctime() + '] A new song, "' + title + '" by "' + artist + '", was submitted to Tunezout at ' + request.build_absolute_uri() + '.'
		mail_managers(subject, message)
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('songs:index'))

def rate(request, pk, rating, genre):
	genre_list = Genre.objects.all().order_by('name')
	try:
		song = Song.objects.get(pk=pk)
	except (KeyError, Song.DoesNotExist):
		# Redisplay the song submission form.
		if genre == '0':
			messages.error(request, 'Your rating was invalid.')
			return render(request, 'songs/index.html', {
				'genre_list': genre_list,
			})
		else:
			messages.error(request, 'Your rating was invalid.')
			return render(request, 'songs/index.html', {
				'genre': Genre.objects.get(id=genre),
				'genre_list': genre_list,
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
