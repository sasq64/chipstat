import webapp2
import logging
import pickle
from webapp2_extras import json
from google.appengine.ext import ndb

class SongPlayedData(ndb.Model):
	path = ndb.StringProperty(indexed=False)
	collection = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	uid = ndb.StringProperty(indexed=False)

class PlayList(ndb.Model):
	data = ndb.BlobProperty(indexed=False)
	uid = ndb.StringProperty(indexed=False)
	username = ndb.StringProperty(indexed=False)

class User(ndb.Model):
	uid = ndb.StringProperty(indexed=False)
	username = ndb.StringProperty(indexed=False)


class MainPage(webapp2.RequestHandler):
	def get(self):
		q = SongPlayedData.query(ancestor=ndb.Key('SongsPlayed', 'default')).order(-SongPlayedData.date)
		songdata = q.fetch(10)

		self.response.headers['Content-Type'] = 'text/plain'
		for s in songdata:
			self.response.write(s.path + "\n") 

class GetPlayed(webapp2.RequestHandler):
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

class GetList(webapp2.RequestHandler):
	def get(self):
		q = PlayList.query(ancestor=ndb.Key('PlayLists', 'default'))
		songdata = q.fetch(100)

		self.response.headers['Content-Type'] = 'application/json'
		plist = []
		for favdata in songdata:
			songs = pickle.loads(favdata.data)
			for s in songs :
				s2 = s.split(':')
				plist.append({ 'path' : s2[0], 'collection' : s2[1] })
		self.response.write(json.encode(plist))

class GetLists(webapp2.RequestHandler):
	def get(self):
		q = PlayList.query(ancestor=ndb.Key('PlayLists', 'default'))
		songdata = q.fetch(100)

		self.response.headers['Content-Type'] = 'application/json'
		plist = []
		for favdata in songdata:
			plist.append({ 'name' : s2[0], 'user' : s2[1] })
		self.response.write(json.encode(plist))

class SetList(webapp2.RequestHandler):
	def post(self):
		p = self.request.body
		data = json.decode(p)
		uid = data['id']
		logging.info('Set list: ' + p)
		favs = PlayList(key=ndb.Key('Playlists', 'default', PlayList, uid))
		favs.data = pickle.dumps(data['songs'])
		favs.put()
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.encode("OK"))

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
		spd.uid = data['id']
		spd.put()

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.encode("OK"))



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/song_played', SongPlayed),
	('/get_played', GetPlayed),
	('/get_list', GetList),
	('/set_list', SetList),
], debug=True)
