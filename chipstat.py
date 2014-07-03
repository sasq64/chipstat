import webapp2
import logging
from webapp2_extras import json
from google.appengine.ext import ndb

class SongPlayedData(ndb.Model):
	path = ndb.StringProperty(indexed=False)
	collection = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		q = SongPlayedData.query(ancestor=ndb.Key('SongsPlayed', 'default')).order(-SongPlayedData.date)
		songdata = q.fetch(10)

		self.response.headers['Content-Type'] = 'text/plain'
		for s in songdata:
			self.response.write(s.path + "\n") 

class GetList(webapp2.RequestHandler):
	def get(self):
		#p = self.request.body
		#data = json.decode(p)
		q = SongPlayedData.query(ancestor=ndb.Key('SongsPlayed', 'default')).order(-SongPlayedData.date)
		songdata = q.fetch(100)

		self.response.headers['Content-Type'] = 'application/json'
		plist = []
		for s in songdata:
			plist.append({ 'path' : s.path, 'collection' : s.collection })
		self.response.write(json.encode(plist))


class SongPlayed(webapp2.RequestHandler):
	def post(self):
		p = self.request.body
		logging.info('SongPlayed: ' + p)
		data = json.decode(p)
		logging.info('Data: ' + data['path'])

		spd = SongPlayedData(parent=ndb.Key('SongsPlayed', 'default'))
		logging.info('Key: ' + str(spd.key))
		spd.path = data['path']
		spd.collection = data['collection']
		spd.put()

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.encode("OK"))



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/song_played', SongPlayed),
	('/get_list', GetList),
], debug=True)
