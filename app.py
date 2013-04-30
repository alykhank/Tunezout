#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
genres = ('Hip Hop', 'Electronic', 'R&B')
songs = [\
		{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':'2013', 'genre':'Hip Hop' },\
		{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':'2012', 'genre':'Hip Hop' },\
		{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':'2013', 'genre':'Electronic' }\
		]

@app.route('/')
def index():
	return render_template('index.html', genres=genres, genre=genres[0], songs=songs)

@app.route('/submit')
def submit():
	title = request.args.get('Song Title')
	artist = request.args.get('Artist')
	year = request.args.get('Year')
	genre = request.args.get('Genre')
	songs.append({ 'rank':str(len(songs) + 1), 'title':title, 'artist':artist, 'year':year, 'genre':genre })
	return redirect(url_for('index'))

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
