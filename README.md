chipstat
========

*chipstat* is an App Engine server that allows music players to share play lists and play statistics.
It is mainly meant to be used by *Retro music players* (C64, Amiga etc) to help users find new music by
looking at others users play lists and what people are playing right now.

Currently only a few API calls are used, but the application is live at;

http://wired-height-596.appspot.com

(But until I get others to beta test my music player *Chipmachine* it will only show you what I am listening to :)


## API

All calls expects post data in json in and out

### `song_played`

Report that a song was played 

#### Parameters
```javascript
{ collection : String,
  path : String,
  uid : String
} 
```

* **collection** - The name of the collection containing the song
* **path** - The relative path to the song in the collection
* **uid** - The ID of the user

#### Result


### `get_played`

Get a list of the latest played songs

#### Parameters
```javascript
{ count : Number }
```

* **count** - Number of songs to get

#### Result
```javascript
{ songs : [
	{ collection : String,
	  path : String,
	  uid : String
	} 
] }
```

* **songs** - Array of the latest songs played
* **collection** - The name of the collection containing the song
* **path** - The relative path to the song in the collection
* **uid** - The ID of the user who played the song


### `login`

Bind a UID to a username. The name for a UID can be changed, but may not be bound
to a username that's already used.

#### Parameters
```javascript
{ uid : String,
  name : String }
```

* **uid** - The user ID
* **name** - The user name

#### Result
```javascript
{ rc : Number }
```

* **rc** - 0 = success, 1 = Username already taken.

### `set_list`

Save a playlist to the server. Used must have logged in, ie the given UID must be bound
to a username.

#### Parameters
```javascript
{ name : String,
  uid : String,
  songs : [ String... ]
}
```
* **uid** - User ID
* **name** - Playlist name
* **songs** - Array of strings, where each string is of the form `<path>:<collection>`


### `get_list`

Read a playlist from the server

#### Result
```javascript
{ name : String,
  username: String,
  songs : [ String... ]
}
```
* **username** - User who created playlist
* **name** - Playlist name
* **songs** - Array of strings, where each string is of the form `<path>:<collection>`

### `get_lists`

Get a list of all playlists

#### Result
```javascript
{ lists : [ 
	{ name : String,
      username: String
    }
] }
```
* **username** - User who created playlist
* **name** - Playlist name

