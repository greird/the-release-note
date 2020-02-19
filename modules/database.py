import os
from sqlalchemy import create_engine, text, MetaData, Table, Column

class Database(object):
	"""docstring for Database"""
	engine = create_engine(os.environ.get('DATABASE'))
	def __init__(self):
		self.tables = self.engine.table_names()
		self.db = self.engine.connect()
		self.meta = MetaData(self.engine)

	def __del__(self):
		self.db.close()

	def getUser(self, user_id):
		tbl_user = Table('dim_user', self.meta,  
			Column('user_id'), 
			Column('first_name'), 
			Column('last_name'), 
			Column('email'), 
			Column('frequency'), 
			Column('last_check'))
		r = self.db.execute(tbl_user.select())
		print(r.fetchone())
		return r

	def createUser(self, user_id, first_name=None, last_name=None, email=None, frequency=None):
		sql = text('''INSERT INTO dim_user (user_id, first_name, last_name, email, frequency) VALUES (:user_id, :first_name, :last_name, :email, :frequency);''')
		self.db.execute(sql,
			user_id=user_id,
			first_name=first_name,
			last_name=last_name,
			email=email,
			frequency=frequency)

	def updateUserLastCheck(self, user_id):
		user_exists = self.db.execute("SELECT exists(SELECT user_id FROM dim_user WHERE user_id=" + str(user_id) + ");").fetchone()[0]
		if user_exists:
			self.db.execute("UPDATE dim_user SET last_check=NOW() WHERE user_id=" + str(user_id) + ";")
		else:
			self.createUser(user_id=user_id)

	def getArtist(self, artist_id):
		pass

	def createArtist(self, artist):
		artist_exists = self.db.execute("SELECT exists(SELECT artist_id FROM dim_artist WHERE artist_id=" + str(artist['id']) + ");").fetchone()[0]
		if artist_exists:
			self.db.execute("UPDATE dim_artist SET nb_fans=" + str(artist['nb_fan']) + ", updated_at=NOW() WHERE artist_id=" + str(artist['id']) + ";")
		else:
			sql = text('INSERT INTO dim_artist (artist_id, name, nb_fans) VALUES (:artist_id, :artist_name, :nb_fans);')
			self.db.execute(sql,
				artist_id=artist['id'],
				artist_name=artist['name'],
				nb_fans=artist['nb_fan'])

	def getAlbum(self, album_id):
		pass

	def createAlbum(self, album):
		album_exists = self.db.execute("SELECT exists(SELECT album_id FROM dim_album WHERE album_id=" + str(album['id']) + ");").fetchone()[0]
		if album_exists:
			self.db.execute("UPDATE dim_album SET nb_fans=" + str(album['fans']) + ", updated_at=NOW() WHERE album_id=" + str(album['id']) + ";")
		else:
			sql = text('INSERT INTO dim_album (album_id, artist_id, title, release_date, nb_fans, genre_id, type) VALUES (:album_id, :artist_id, :title, :release_date, :nb_fans, :genre_id, :type);')
			self.db.execute(sql, 
				album_id=album['id'], 
				artist_id=album['artist']['id'], 
				title=album['title'], 
				release_date=album['release_date'], 
				nb_fans=album['fans'], 
				genre_id=album['genre_id'], 
				type=album['record_type'])

	def storeNewReleases(self, new_releases, user_id):
		rows = []
		for a in new_releases:
			self.createAlbum(a)
			self.createArtist(a['artist'])
			rows.append("(" + str(user_id) + ", " + str(a['artist']['id']) + ", " + str(a['id']) + ", NOW())")

		self.db.execute("INSERT INTO fact_releases (user_id, artist_id, album_id, created_at) VALUES" + ', '.join(rows) + ";")	
		self.updateUserLastCheck(user_id)

	def getUserReleases(self, user_id, from_date=None):
		pass

db = Database()
db.getUser(34466551)