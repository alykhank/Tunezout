from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from songs.models import Song, Genre

def create_song(title, genre, artist="Artist", year="2000-01-01", approved=True):
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
		create_song(title="Unapproved", genre=genre, approved=False)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], [])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_one_approved_song(self):
		"""
		Songs with approved=True should be displayed on the index page.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Approved", genre=genre, approved=True)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_approved_song_and_unapproved_song(self):
		"""
		Even if approved and unapproved songs exist, only approved songs should be displayed.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Unapproved", genre=genre, approved=False)
		create_song(title="Approved", genre=genre, approved=True)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

	def test_index_view_with_two_approved_songs(self):
		"""
		The songs index page may display multiple songs.
		"""
		genre = Genre.objects.create(name="MyGenre")
		create_song(title="Approved1", genre=genre)
		create_song(title="Approved2", genre=genre)
		response = self.client.get(reverse('songs:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved1>', '<Song: Approved2>'])
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])

class SongDetailViewTests(TestCase):
	def test_detail_view_with_one_unapproved_song(self):
		"""
		The song detail page should not display a song's information when it is not approved.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = create_song(title="Unapproved", genre=genre, approved=False)
		response = self.client.get(reverse('songs:detail', args=(song.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_one_approved_song(self):
		"""
		The song detail page should display a song's information when it is approved.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = create_song(title="Approved", genre=genre, approved=True)
		response = self.client.get(reverse('songs:detail', args=(song.id,)))
		self.assertContains(response, song.title, status_code=200)
		self.assertEqual(response.context['song'], song)

class SongGenreViewTests(TestCase):
	def test_genre_view_with_one_song_of_same_genre(self):
		"""
		The genre view should display songs with the same genre.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = create_song(title="Approved", genre=genre)
		response = self.client.get(reverse('songs:genre', args=(genre.id,)))
		self.assertContains(response, genre.name, status_code=200)
		self.assertContains(response, song.title)
		self.assertEqual(response.context['genre'], genre)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])

	def test_genre_view_with_one_song_of_different_genre(self):
		"""
		The genre view should not display songs with a different genre.
		"""
		genre1 = Genre.objects.create(name="MyGenre1")
		genre2 = Genre.objects.create(name="MyGenre2")
		song = create_song(title="Approved", genre=genre2)
		response = self.client.get(reverse('songs:genre', args=(genre1.id,)))
		self.assertContains(response, genre1.name, status_code=200)
		self.assertNotContains(response, song.title)
		self.assertEqual(response.context['genre'], genre1)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre1>', '<Genre: MyGenre2>'])
		self.assertQuerysetEqual(response.context['song_list'], [])

	def test_genre_view_with_same_genre_song_and_different_genre_song(self):
		"""
		The genre view should display only songs with the same genre.
		"""
		genre1 = Genre.objects.create(name="MyGenre1")
		genre2 = Genre.objects.create(name="MyGenre2")
		song1 = create_song(title="Approved1", genre=genre1)
		song2 = create_song(title="Approved2", genre=genre2)
		response = self.client.get(reverse('songs:genre', args=(genre1.id,)))
		self.assertContains(response, genre1.name, status_code=200)
		self.assertContains(response, song1.title)
		self.assertNotContains(response, song2.title)
		self.assertEqual(response.context['genre'], genre1)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre1>', '<Genre: MyGenre2>'])
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved1>'])

class SongYearViewTests(TestCase):
	def test_year_view_with_one_song_of_same_year(self):
		"""
		The year view should display songs with the same year.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = create_song(title="Approved", year="1995-01-01", genre=genre)
		response = self.client.get(reverse('songs:year', args=(1995,)))
		self.assertContains(response, genre.name, status_code=200)
		self.assertContains(response, song.title)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved>'])

	def test_year_view_with_one_song_of_different_year(self):
		"""
		The year view should not display songs with a different year.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = create_song(title="Approved", year="1995-01-01", genre=genre)
		response = self.client.get(reverse('songs:year', args=(2005,)))
		self.assertContains(response, genre.name, status_code=200)
		self.assertNotContains(response, song.title)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], [])

	def test_year_view_with_same_year_song_and_different_year_song(self):
		"""
		The year view should display only songs with the same year.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song1 = create_song(title="Approved1", year="1995-01-01", genre=genre)
		song2 = create_song(title="Approved2", year="2005-01-01", genre=genre)
		response = self.client.get(reverse('songs:year', args=(1995,)))
		self.assertContains(response, genre.name, status_code=200)
		self.assertContains(response, song1.title)
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], ['<Song: Approved1>'])

class SongSubmitViewTests(TestCase):
	def test_submit_view_with_empty_submission(self):
		"""
		The submit view should display an error message on a blank submission.
		"""
		genre = Genre.objects.create(name="MyGenre")
		response = self.client.post(reverse('songs:submit'), {'title': '', 'artist': '', 'year': '', 'genre': genre.id})
		self.assertContains(response, genre.name, status_code=200)
		self.assertContains(response, 'You left something blank!')
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], [])

	def test_submit_view_with_too_long_submission(self):
		"""
		The submit view should display an error message on a submission that is too long.
		"""
		genre = Genre.objects.create(name="MyGenre")
		long_title = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
		response = self.client.post(reverse('songs:submit'), {'title': long_title, 'artist': 'Artist', 'year': '1995', 'genre': genre.id})
		self.assertContains(response, genre.name, status_code=200)
		self.assertContains(response, 'Your submission was too long.')
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], [])

	def test_submit_view_with_invalid_submission(self):
		"""
		The submit view should display an error message on a submission that is invalid.
		"""
		response = self.client.post(reverse('songs:submit'), {'title': 'Unapproved', 'artist': 'Artist', 'year': '1995', 'genre': 0})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Your submission was invalid.')
		self.assertQuerysetEqual(response.context['genre_list'], [])
		self.assertQuerysetEqual(response.context['song_list'], [])

	def test_submit_view_with_successful_submission(self):
		"""
		The submit view should display a success message on a submission that is successful.
		"""
		genre = Genre.objects.create(name="MyGenre")
		song = {'title': 'Unapproved', 'artist': 'Artist', 'year': '1995', 'genre': genre.id}
		response = self.client.post(reverse('songs:submit'), song, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'You successfully submitted &quot;' + song['title'] + '&quot; by &quot;' + song['artist'] + '&quot; for approval.')
		self.assertQuerysetEqual(response.context['genre_list'], ['<Genre: MyGenre>'])
		self.assertQuerysetEqual(response.context['song_list'], [])

class SongLogoutViewTests(TestCase):
	def test_logout_view_when_logged_out(self):
		"""
		The logout view should display a success message when logged out.
		"""
		response = self.client.get(reverse('songs:logout'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Successfully logged out.')

	def test_logout_view_when_logged_in(self):
		"""
		The logout view should display a success message when logged in.
		"""
		user = User.objects.create_user('test', password='test')
		self.assertTrue(self.client.login(username='test', password='test'))
		response = self.client.get(reverse('songs:logout'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Successfully logged out.')
