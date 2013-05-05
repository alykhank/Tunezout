#!/usr/bin/env python
from models import db, Song, Genre

genres = (Genre('Country'), Genre('Dance'), Genre('Dubstep'), Genre('Electronica'), Genre('Hip-Hop/Rap'), Genre('House'), Genre('Jazz'), Genre('Pop'), Genre('R&B'), Genre('Rock'), Genre('Other'))

for genre in genres:
	db.session.add(genre)

songlist = [\
	{ 'title':'The Motto', 'artist':'Drake', 'year':2013, 'genre':genres[2], 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Started from the Bottom', 'artist':'Drake', 'year':2013, 'genre':genres[2], 'up':0, 'down':0, 'score':0 },\
	{ 'title':'Thrift Shop', 'artist':'Macklemore', 'year':2013, 'genre':genres[1], 'up':0, 'down':0, 'score':0 }\
	]

for item in songlist:
	song = Song(item['title'], item['artist'], item['year'], item['genre'], item['up'], item['down'], item['score'])
	db.session.add(song)
db.session.commit()
