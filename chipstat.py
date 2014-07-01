import webapp2
import logging
from webapp2_extras import json
from google.appengine.ext import ndb

class SongPlayedData(ndb.Model):
	path = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		q = SongPlayedData.query(ancestor=ndb.Key('SongsPlayed', 'default')).order(-SongPlayedData.date)
		songdata = q.fetch(10)

		self.response.headers['Content-Type'] = 'text/plain'
		for s in songdata:
			self.response.write(s.path + "\n") 

class SongPlayed(webapp2.RequestHandler):
	def post(self):
		p = self.request.body
		logging.info('SongPlayed: ' + p)
		data = json.decode(p)
		logging.info('Data: ' + data['path'])

		spd = SongPlayedData(parent=ndb.Key('SongsPlayed', 'default'))
		logging.info('Key: ' + str(spd.key))
		spd.path = data['path']
		spd.put()

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(p)



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/song_played', SongPlayed),
], debug=True)
