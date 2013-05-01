#!/usr/bin/env python
from models import db, Song

songlist = [\
	{ 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':'Hip-Hop/Rap', 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':'Dance/Electronic', 'up':0, 'down':0, 'score':0 }\
	]
for item in songlist:
	song = Song(item['title'], item['artist'], item['year'], item['genre'], item['up'], item['down'], item['score'])
	db.session.add(song)
db.session.commit()
