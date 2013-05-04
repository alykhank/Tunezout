#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import app, db, Song, Genre

@app.route('/')
def index():
	genreFilter = request.args.get('genre', 0, type=int)
	genre = Genre.query.filter(Genre.id == genreFilter).first()
	return index(genre)

def index(genre):
	genres = Genre.query.order_by(Genre.name.asc()).all()
	if genre:
		songs = Song.query.filter(Song.genre == genre).order_by(Song.score.desc()).all()
	else:
		songs = Song.query.order_by(Song.score.desc()).all()
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

@app.route('/songs')
def songs(genre=None):
	if not genre:
		genreFilter = request.args.get('genre', 0, type=int)
		genre = Genre.query.filter(Genre.id == genreFilter).first()
	genres = Genre.query.order_by(Genre.name.asc()).all()
	if genre:
		songs = Song.query.filter(Song.genre == genre).order_by(Song.score.desc()).all()
	else:
		songs = Song.query.order_by(Song.score.desc()).all()
	return render_template('songs.html', genre=genre, songs=songs)

@app.route('/submit')
def submit():
	title = request.args.get('title', '', type=str)
	artist = request.args.get('artist', '', type=str)
	year = request.args.get('year', 0, type=int)
	genre = request.args.get('genre', 'Other', type=str)
	genreMatch = Genre.query.filter(Genre.name == genre).first()
	if genreMatch:
		song = Song(title, artist, year, genreMatch, 0, 0, 0)
		db.session.add(song)
		db.session.commit()
	return index(None)

@app.route('/rate')
def rate():
	id = request.args.get('id', 0, type=int)
	rate = request.args.get('rate', 0, type=int)
	if rate is 1:
		Song.query.filter(Song.id == id).update({'down':Song.down+1, 'score':Song.score-1})
		db.session.commit()
	elif rate is 2:
		Song.query.filter(Song.id == id).update({'up':Song.up+1, 'score':Song.score+1})
		db.session.commit()
	genreFilter = request.args.get('genre', 0, type=int)
	genre = Genre.query.filter(Genre.id == genreFilter).first()
	return songs(genre)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
