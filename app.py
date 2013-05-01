#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
genres = ('Country', 'Dance/Electronic', 'Hip-Hop/Rap', 'Jazz', 'R&B', 'Rock', 'Other')
songlist = [\
		{ 'id':1, 'rank':1, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':2, 'rank':2, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':3, 'rank':3, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':4, 'rank':4, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':5, 'rank':5, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':6, 'rank':6, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':7, 'rank':7, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':8, 'rank':8, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':9, 'rank':9, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':10, 'rank':10, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':11, 'rank':11, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':12, 'rank':12, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':13, 'rank':1, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':14, 'rank':2, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':15, 'rank':3, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':16, 'rank':4, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':17, 'rank':5, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':18, 'rank':6, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':19, 'rank':7, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':20, 'rank':8, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':21, 'rank':9, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':22, 'rank':10, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':23, 'rank':11, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':24, 'rank':12, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':25, 'rank':1, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':26, 'rank':2, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':27, 'rank':3, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':28, 'rank':4, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':29, 'rank':5, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':30, 'rank':6, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':31, 'rank':7, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':32, 'rank':8, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':33, 'rank':9, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 },\
		{ 'id':34, 'rank':10, 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':35, 'rank':11, 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':12, 'down':4 },\
		{ 'id':36, 'rank':12, 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':12, 'down':4 }\
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
	if title and artist and year and genre and (genre in genres):
		songlist.append({ 'id':len(songlist) + 1, 'rank':len(songlist) + 1, 'title':title, 'artist':artist, 'year':year, 'genre':genre, 'up':0, 'down':0 })
	return redirect(url_for('index'))

@app.route('/rate')
def rate():
	id = request.args.get('ID', type=int)
	rate = request.args.get('Rate', type=int)
	if id and rate:
		if rate == 1:
			songlist[id-1]['down'] += 1;
		elif rate == 2:
			songlist[id-1]['up'] += 1;
	return redirect(url_for('index'))

def copyf(key, valuelist):
	return [dictio for dictio in songlist if dictio[key] in valuelist]

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
