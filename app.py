#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
genres = ('Hip Hop', 'Electronic', 'R&B')
songlist = [\
		{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':'2013', 'genre':'Hip Hop' },\
		{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':'2013', 'genre':'Hip Hop' },\
		{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':'2013', 'genre':'Electronic' }\
		]

@app.route('/')
def index():
	genreFilter = request.args.get('Genre')
	if genreFilter and 0 <= int(genreFilter) and int(genreFilter) < len(genres):
		genre = genres[int(genreFilter)]
		songs = copyf('genre', [genre])
	else:
		genre = 'All'
		songs = songlist
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

@app.route('/submit')
def submit():
	title = request.args.get('Song Title')
	artist = request.args.get('Artist')
	year = request.args.get('Year')
	genre = request.args.get('Genre')
	if (title and artist and year and genre):
		songlist.append({ 'rank':str(len(songlist) + 1), 'title':title, 'artist':artist, 'year':year, 'genre':genre })
	return redirect(url_for('index'))

def copyf(key, valuelist):
	return [dictio for dictio in songlist if dictio[key] in valuelist]

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
