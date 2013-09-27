from django.db import models

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
