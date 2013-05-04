#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import app, db, Song, Genre

@app.route('/')
def index():
	genres = Genre.query.order_by(Genre.name.asc()).all()
	genre = None
	songs = Song.query.order_by(Song.score.desc()).all()
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

def index(genres, genre, songs):
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

@app.route('/songs')
def songs():
	genreFilter = request.args.get('genre', 0, type=int)
	genres = Genre.query.order_by(Genre.name.asc()).all()
	if genreFilter and 0 < genreFilter and genreFilter <= len(genres):
		genre = Genre.query.filter(Genre.id == genreFilter).first()
		songs = Song.query.filter(Song.genre == genre).order_by(Song.score.desc()).all()
	else:
		genre = None
		songs = Song.query.order_by(Song.score.desc()).all()
	return index(genres, genre, songs)

@app.route('/submit')
def submit():
	title = request.args.get('Song Title', '', type=str)
	artist = request.args.get('Artist', '', type=str)
	year = request.args.get('Year', 0, type=int)
	genre = request.args.get('Genre', 'Other', type=str)
	genreMatch = Genre.query.filter(Genre.name == genre).first()
	if title and artist and genreMatch:
		song = Song(title, artist, year, genreMatch, 0, 0, 0)
		db.session.add(song)
		db.session.commit()
	genres = Genre.query.order_by(Genre.name.asc()).all()
	songs = Song.query.order_by(Song.score.desc()).all()
	return index(genres, None, songs)

@app.route('/rate')
def rate():
	id = request.args.get('ID', 0, type=int)
	rate = request.args.get('Rate', 0, type=int)
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
