#!/usr/bin/env python
from models import db, Song, Genre

genres = (Genre('Country'), Genre('Dance'), Genre('Dubstep'), Genre('Electronica'), Genre('Hip-Hop/Rap'), Genre('House'), Genre('Jazz'), Genre('Pop'), Genre('R&B'), Genre('Rock'), Genre('Other'))

for genre in genres:
	db.session.add(genre)

songlist = [\
		('Thrift Shop', 'Macklemore & Ryan Lewis', 2012),\
		('Can\'t Hold Us', 'Macklemore ft. Ray Dalton', 2012),\
		('Inner Ninja', 'Classified ft. David Myles', 2013),\
		('Started from the Bottom', 'Drake', 2013),\
		('Wild for the Night', 'ASAP ft. Skrillex', 2013),\
		('Love Me', 'Lil\' Wayne ft. Drake & Future', 2013),\
		('Ni**as in Paris', 'Kanye West & Jay Z', 2011),\
		('Gotta Have It', 'Kanye West & Jay Z', 2011),\
		('No Church in the Wild', 'Kanye West & Jay Z ft. Frank Ocean', 2011),\
		('Hey Porsche', 'Nelly', 2013),\
		('Whistle', 'Flo Rida', 2012),\
		('The Motto', 'Drake', 2011),\
		('Practice', 'Drake', 2011),\
		('Make me Proud', 'Drake ft. Nicki Minaj', 2011),\
		('Take Care', 'Drake ft. Rihanna', 2011),\
		('Headlines', 'Drake', 2011),\
		('Empire State of Mind', 'Jay Z ft. Alicia Keys', 2009),\
		('Dope', 'Tyga ft. Rick Ross', 2013)\
		]

for item in songlist:
	song = Song(item[0], item[1], item[2], genres[4], 0, 0, 0)
	db.session.add(song)

songlist = [\
		('Blurred Lines', 'Robin Thicke ft. T.I. & Pharrell', 2013),\
		('Girl on Fire', 'Alicia Keys', 2012),\
		('DJ Got Us Fallin\' In Love', 'Usher ft. Pitbull', 2010),\
		('Scream', 'Usher', 2012),\
		('Numb', 'Usher', 2012),\
		('Look At Me Now', 'Chris Brown ft. Lil Wayne & Busta Rhymes', 2011),\
		('Brand New Day', 'Massari', 2012),\
		('Don\'t Wake Me Up', 'Chris Brown', 2012),\
		('OMG', 'Usher ft. will.i.am', 2010),\
		('Forever', 'Chris Brown', 2008),\
		('Super Bass', 'Nicki Minaj', 2011)\
		]

for item in songlist:
	song = Song(item[0], item[1], item[2], genres[8], 0, 0, 0)
	db.session.add(song)

db.session.commit()
