#!/usr/bin/env python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rank = db.Column(db.Integer)
	title = db.Column(db.String)
	artist = db.Column(db.String)
	year = db.Column(db.Integer)
	genre = db.Column(db.String)
	up = db.Column(db.Integer)
	down = db.Column(db.Integer)
	score = db.Column(db.Integer)

	def __init__(self, rank, title, artist, year, genre, up, down, score):
		self.rank = rank
		self.title = title
		self.artist = artist
		self.year = year
		self.genre = genre
		self.up = up
		self.down = down
		self.score = score

	def __repr__(self):
		return "<Song('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.rank, self.title, self.artist, self.year, self.genre, self.up, self.down, self.score)
