#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
genres = ('Country', 'Dance/Electronic', 'Hip-Hop/Rap', 'Jazz', 'R&B', 'Rock', 'Other')
songlist = [\
		{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'4', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'5', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'6', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'7', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'8', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'9', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'10', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'11', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'12', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'4', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'5', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'6', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'7', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'8', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'9', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'10', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'11', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'12', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'1', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'2', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'3', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'4', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'5', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'6', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'7', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'8', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'9', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'rank':'10', 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'11', 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'rank':'12', 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 }\
		]

@app.route('/')
def index():
	genreFilter = request.args.get('Genre', type=int)
	if genreFilter and 0 < genreFilter and genreFilter < len(genres):
		genre = genres[genreFilter - 1]
		songs = copyf('genre', [genre])
	else:
		genre = 'All'
		songs = songlist
	return render_template('index.html', genres=genres, genre=genre, songs=songs)

@app.route('/submit')
def submit():
	title = request.args.get('Song Title', type=str)
	artist = request.args.get('Artist', type=str)
	year = request.args.get('Year', type=int)
	genre = request.args.get('Genre', type=str)
	if (title and artist and year and genre and genre in genres):
		songlist.append({ 'rank':str(len(songlist) + 1), 'title':title, 'artist':artist, 'year':year, 'genre':genre })
	return redirect(url_for('index'))

def copyf(key, valuelist):
	return [dictio for dictio in songlist if dictio[key] in valuelist]

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
