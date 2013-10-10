import os, urlparse
from datetime import datetime
from rauth import OAuth1Service
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import mail_managers

from songs.models import Genre, Song, TwitterProfile

twitter = OAuth1Service(
	name = 'twitter',
	consumer_key = os.environ.get('TWITTER_CONS_KEY'),
	consumer_secret = os.environ.get('TWITTER_CONS_SECRET'),
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	authorize_url = 'https://api.twitter.com/oauth/authorize',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	base_url = 'https://api.twitter.com/'
)

def login(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = authenticate(username=username, password=password)
	if user is not None and user.is_active:
		login(request, user)
		messages.success(request, 'Logged in as ' + user.username + '.')
		return HttpResponseRedirect(reverse('songs:index'))
	else:
		messages.error(request, 'Invalid login.')
		return HttpResponseRedirect(reverse('songs:index'))

def logout(request):
	logout(request)
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

def twitter_login(request):
	request_token = twitter.get_raw_request_token(params={'oauth_callback': request.build_absolute_uri(reverse('songs:twitter_success'))})
	if request_token.status_code != 200:
		return twitter_login_failed(request)
	r = urlparse.parse_qs(request_token.text)
	if not r['oauth_callback_confirmed'][0]:
		return twitter_login_failed(request)
	request.session['request_token'] = r['oauth_token'][0]
	request.session['request_token_secret'] = r['oauth_token_secret'][0]
	return HttpResponseRedirect(twitter.base_url + 'oauth/authenticate?oauth_token=' + request.session['request_token'])

def twitter_login_failed(request):
	messages.error(request, 'Twitter login failed.')
	return HttpResponseRedirect(reverse('songs:index'))

def twitter_success(request):
	oauth_token = request.GET.get('oauth_token')
	oauth_verifier = request.GET.get('oauth_verifier')
	if 'request_token' in request.session and 'request_token_secret' in request.session:
		request_token = request.session['request_token']
		request_token_secret = request.session['request_token_secret']
		if request_token != oauth_token:
			return twitter_login_failed(request)
		access_token = twitter.get_raw_access_token(request_token, request_token_secret, params={'oauth_verifier': oauth_verifier})
		if access_token.status_code != 200:
			return twitter_login_failed(request)
		r = urlparse.parse_qs(access_token.text)
		request.session['access_token'] = r['oauth_token'][0]
		request.session['access_token_secret'] = r['oauth_token_secret'][0]
		request.session['user_id'] = r['user_id'][0]
		request.session['screen_name'] = r['screen_name'][0]
		# request.session['twitter_session'] = twitter.get_auth_session(request_token, request_token_secret)
		del request.session['request_token']
		del request.session['request_token_secret']
		messages.success(request, 'Logged in with Twitter as ' + request.session['screen_name'] + '.')
		return HttpResponseRedirect(reverse('songs:index'))
	else:
		return twitter_login_failed(request)

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
