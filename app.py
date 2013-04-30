#!/usr/bin/env python
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
	genres = ('Hip Hop', 'Electronic', 'R&B')
	songs = [\
			{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':'2013', 'genre':'Rap' },\
			{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':'2012', 'genre':'Hip Hop' },\
			{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':'2013', 'genre':'House' }\
			]
	return render_template('index.html', genres=genres, genre=genres[0], songs=songs)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
