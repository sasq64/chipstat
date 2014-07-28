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
	name = ndb.StringProperty(indexed=False)
	uid = ndb.StringProperty(indexed=False)
	username = ndb.StringProperty(indexed=False)

class User(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	plan = ndb.StringProperty(indexed=False)


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'


		q = SongPlayedData.query(ancestor=ndb.Key('SongsPlayed', 'default')).order(-SongPlayedData.date)
		songdata = q.fetch(10)

		for s in songdata:
			self.response.write(s.path + "\n")

		q = User.query(ancestor=ndb.Key('Users', 'default'))
		users = q.fetch(100)
		for u in users:
			self.response.write(u.name + " " + str(u.key) + "\n") 

		q = PlayList.query(ancestor=ndb.Key('PlayLists', 'default'))
		plists = q.fetch(100)
		for u in plists:
			self.response.write(u.name + " " + str(u.key) + "\n") 


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
		self.get_list(self.request.get('name'), self.request.get('username'))

	def post(self):
		data = json.decode(self.request.body)
		self.get_list(data['name'], data['username'])

	def get_list(self, name, username) :
		#q = PlayList.query(ndb.AND(PlayList.name == name, PlayList.username == username))
		#plists = q.fetch(100)
		id = username + ':' + name


		logging.info('Get list: ' + id)
		plKey = ndb.Key('PlayLists', 'default', PlayList, id)
		playlist = plKey.get();

		self.response.headers['Content-Type'] = 'application/json'
		if playlist :
			songs = pickle.loads(playlist.data)
			self.response.write(json.encode({ 'name' : playlist.name, 'songs' : songs}))
		else :
			self.response.write(json.encode({ 'rc' : 1, 'msg' : 'NO SUCH PLAYLIST'}))


class GetLists(webapp2.RequestHandler):
	def get(self):
		q = PlayList.query(ancestor=ndb.Key('PlayLists', 'default'))
		pquery = q.fetch(100)

		self.response.headers['Content-Type'] = 'application/json'
		plist = []
		for p in pquery :
			plist.append({ 'name' : p.name, 'user' : p.username })
		self.response.write(json.encode(plist))

class SetList(webapp2.RequestHandler):

	def get(self):
		self.set_list(self.request.get('uid'), self.request.get('name'), self.request.get('songs'))

	def post(self):
		p = self.request.body
		logging.info('Set list: ' + p)
		data = json.decode(p)
		uid = data['uid']
		name = data['name']
		songs = data['songs']
		self.set_list(uid, name, songs)

	def set_list(self, uid, name, songs):

		userKey = ndb.Key('Users', 'default', User, uid);

		user = userKey.get();

		self.response.headers['Content-Type'] = 'application/json'

		if user :

			id = user.name + ':' + name

			logging.info('Set list: ' + id)
			plist = PlayList(key=ndb.Key('PlayLists', 'default', PlayList, id))
			plist.name = name;
			plist.uid = uid
			plist.username = user.name
			plist.data = pickle.dumps(songs)
			plist.put()
			self.response.write(json.encode("OK"))
		else :
			self.response.write(json.encode("ERROR: NO SUCH USER:"))

class Login(webapp2.RequestHandler):
	def get(self):
		self.login(self.request.get("name"), self.request.get("uid"))

	def post(self):
		data = json.decode(self.request.body)
		self.login(data['name'], data['uid'])

	def login(self, name, uid):		

		self.response.headers['Content-Type'] = 'application/json'

		q = User.query(User.name == name)

		user = q.fetch(1)
		for u in user :
			logging.info('VS ' + u.key.id() + " " + uid)
			if u.key.id() != uid :
				self.response.write(json.encode({ 'rc' : 1, 'msg' : 'NAME ALREADY TAKEN'}))
			else :
				self.response.write(json.encode({ 'rc' : 0, 'msg' : 'WELCOME BACK'}))
			return

		user = User(key=ndb.Key('Users', 'default', User, uid))
		user.name = name
		user.put()

		self.response.write(json.encode("OK"))

class SongPlayed(webapp2.RequestHandler):
	def get(self):
		self.song_played(self.request.get('collection'), self.request.get('path'), self.request.get('uid'))

	def post(self):
		data = json.decode(self.request.body)
		self.song_played(data['collection'], data['path'], data['uid'])

	def song_played(self, collection, path, uid):

		spd = SongPlayedData(parent=ndb.Key('SongsPlayed', 'default'))
		logging.info('Key: ' + str(spd.key))
		spd.path = path
		spd.collection = collection
		spd.uid = uid
		spd.put()

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.encode("OK"))



application = webapp2.WSGIApplication([
	('/', MainPage),
	('/login', Login),
	('/song_played', SongPlayed),
	('/get_played', GetPlayed),
	('/get_list', GetList),
	('/get_lists', GetLists),
	('/set_list', SetList),
], debug=True)
