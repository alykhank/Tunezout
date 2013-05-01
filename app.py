#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for
from models import app, db, Song

genres = ('Country', 'Dance/Electronic', 'Hip-Hop/Rap', 'Jazz', 'R&B', 'Rock', 'Other')

@app.route('/')
def index():
	genreFilter = request.args.get('Genre', type=int)
	if genreFilter and 0 < genreFilter and genreFilter <= len(genres):
		genre = genres[genreFilter - 1]
		songs = Song.query.filter(Song.genre == genre)
	else:
		genre = 'All'
		songs = Song.query.order_by(Song.score.desc())
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

@app.route('/submit')
def submit():
	title = request.args.get('Song Title', type=str)
	artist = request.args.get('Artist', type=str)
	year = request.args.get('Year', type=int)
	genre = request.args.get('Genre', type=str)
	if title and artist and year and genre and (genre in genres):
		song = Song(title, artist, year, genre, 0, 0, 0)
		db.session.add(song)
		db.session.commit()
	return redirect(url_for('index'))

@app.route('/rate')
def rate():
	id = request.args.get('ID', type=int)
	rate = request.args.get('Rate', type=int)
	if id and rate:
		if rate == 1:
			Song.query.filter(Song.id == id).update({'down':Song.down+1, 'score':Song.score-1})
			db.session.commit()
		elif rate == 2:
			Song.query.filter(Song.id == id).update({'up':Song.up+1, 'score':Song.score+1})
			db.session.commit()
	return redirect(url_for('index'))

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
