#!/usr/bin/env python
from models import db, Song, Genre

genres = ('Country', 'Dance/Electronic', 'Hip-Hop/Rap', 'House', 'Jazz', 'R&B', 'Rock', 'Other')

songlist = [\
	{ 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':0, 'down':0, 'score':0 }\
	]

for item in songlist:
	song = Song(item['title'], item['artist'], item['year'], item['genre'], item['up'], item['down'], item['score'])
	db.session.add(song)
for item in genres:
	genre = Genre(item)
	db.session.add(genre)
db.session.commit()
