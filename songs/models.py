from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Song(models.Model):
	title = models.CharField(max_length=100)
	artist = models.CharField(max_length=100)
	year = models.DateField()
	genre = models.ForeignKey(Genre)
	up = models.PositiveIntegerField(default=0)
	down = models.PositiveIntegerField(default=0)
	score = models.IntegerField(default=0)
	approved = models.BooleanField()

	def __unicode__(self):
		return self.title

class TwitterProfile(models.Model):
	"""
		An example Profile model that handles storing the oauth_token and
		oauth_secret in relation to a user.
	"""
	user = models.OneToOneField(User)
	oauth_token = models.CharField(max_length=200)
	oauth_token_secret = models.CharField(max_length=200)
	screen_name = models.CharField(max_length=200)
