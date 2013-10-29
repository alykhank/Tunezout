from django.test import TestCase
from django.core.urlresolvers import reverse
from songs.models import Song, Genre

def create_song(title, artist, year, genre, approved):
	"""
	Creates a song with the given attributes.
	"""
	return Song.objects.create(title=title, artist=artist, year=year, genre=genre, approved=approved)

class SongIndexViewTests(TestCase):
	def test_index_view_with_no_songs(self):
		"""
		If no songs exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], [])
		self.assertQuerysetEqual(response.context['genre_list'], [])

	def test_index_view_with_one_unapproved_song(self):
		"""
		Songs with approved=False should not be displayed on the index page.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Unapproved", artist="Unapproved", year="2000-01-01", genre=genre, approved=False)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], [])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_one_approved_song(self):
		"""
		Songs with approved=True should be displayed on the index page.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Approved", artist="Approved", year="2000-01-01", genre=genre, approved=True)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_approved_song_and_unapproved_song(self):
		"""
		Even if approved and unapproved songs exist, only approved songs should be displayed.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Unapproved", artist="Unapproved", year="2000-01-01", genre=genre, approved=False)
		create_song(title="Approved", artist="Approved", year="2000-01-01", genre=genre, approved=True)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_two_approved_songs(self):
		"""
		The songs index page may display multiple songs.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Approved1", artist="Approved1", year="2000-01-01", genre=genre, approved=True)
		create_song(title="Approved2", artist="Approved2", year="2000-01-01", genre=genre, approved=True)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved1>', '<Song: Approved2>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
