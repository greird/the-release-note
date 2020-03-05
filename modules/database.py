import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text, MetaData, Table, Column, join, select, desc
from sqlalchemy.exc import IntegrityError

class Database(object):
	"""docstring for Database"""
	engine = create_engine(os.environ.get('DATABASE'))
	def __init__(self):
		self.tables = self.engine.table_names()
		self.db = self.engine.connect()
		self.meta = MetaData(self.engine)
		self.tbl_user = Table('dim_user', self.meta,  
			Column('user_id'), 
			Column('first_name'), 
			Column('last_name'), 
			Column('email'), 
			Column('frequency'), 
			Column('last_check'))
		self.tbl_artist = Table('dim_artist', self.meta,  
			Column('artist_id'), 
			Column('name'), 
			Column('nb_fans'), 
			Column('created_at'), 
			Column('updated_at'))
		self.tbl_album = Table('dim_album', self.meta,  
			Column('album_id'), 
			Column('title'), 
			Column('artist_id'), 
			Column('release_date'), 
			Column('nb_fans'),
			Column('genre_id'),
			Column('type'),
			Column('inserted_at'),
			Column('updated_at'))
		self.tbl_releases = Table('fact_releases', self.meta,  
			Column('id'), 
			Column('user_id'), 
			Column('artist_id'), 
			Column('album_id'), 
			Column('created_at'))

	def __del__(self):
		self.db.close()

	def getUser(self, user_id):
		return self.db.execute(self.tbl_user.select().where(Column('user_id') == user_id)).fetchone()

	def getAllUsers(self):
		return self.db.execute(self.tbl_user.select()).fetchall()

	def createUser(self, user_id, first_name=None, last_name=None, email=None, frequency=None):
		try:
			self.db.execute(self.tbl_user.insert().values(
				user_id=user_id, 
				first_name=first_name, 
				last_name=last_name, 
				email=email, 
				frequency=frequency))
			return True
		except Exception as e:
			return False

	def updateUserLastCheck(self, user_id):
		user_exists = self.createUser(user_id)
		if not user_exists:
			self.db.execute(self.tbl_user.update()
				.where(Column('user_id') == user_id)
				.values(last_check=datetime.now()))

	def getArtist(self, artist_id):
		return self.db.execute(self.tbl_artist.select().where(Column('artist_id') == artist_id)).fetchone()

	def createArtist(self, artist):
		try:
			self.db.execute(self.tbl_artist.insert()
				.values(artist_id=artist['id'], name=artist['name'], nb_fans=artist['nb_fan']))
		except IntegrityError as e:
			self.db.execute(self.tbl_artist.update()
				.where(Column('artist_id') == artist['id'])
				.values(nb_fans=artist['nb_fan'])) 
		except Exception as e:
			return False

	def getAlbum(self, album_id):
		return self.db.execute(self.tbl_album.select().where(Column('album_id') == album_id)).fetchone()

	def createAlbum(self, album):
		try:
			self.db.execute(self.tbl_album.insert().values(
				album_id=album['id'], 
				title=album['title'], 
				artist_id=album['artist']['id'], 
				release_date=album['release_date'], 
				nb_fans=album['fans'], 
				genre_id=album['genre_id'], 
				type=album['record_type']))
		except IntegrityError as e:
			self.db.execute(self.tbl_album.update()
				.where(Column('album_id') == album['id'])
				.values(nb_fans=album['fans'], updated_at=datetime.now())) 
		except Exception as e:
			return e

	def storeNewReleases(self, new_releases, user_id):
		rows = []
		for a in new_releases:
			self.createAlbum(a)
			self.createArtist(a['artist'])
			rows.append("(" + str(user_id) + ", " + str(a['artist']['id']) + ", " + str(a['id']) + ", NOW())")

		self.db.execute("INSERT INTO fact_releases (user_id, artist_id, album_id, created_at) VALUES" + ', '.join(rows) + ";")	
		self.updateUserLastCheck(user_id)

	def getReleases(self, user_id=None, since=7):
		try:
			if user_id:
				fact = self.tbl_releases.select().distinct(self.tbl_releases.c.album_id).where(Column('user_id') == user_id).alias('fact')
			else:
				fact = self.tbl_releases.select().distinct(self.tbl_releases.c.album_id).alias('fact')
			albums = self.tbl_album.select().where(Column('release_date') >= (datetime.now()-timedelta(int(since)))).alias('albums')
			releases = fact.\
				join(albums, fact.c.album_id == albums.c.album_id).\
				join(self.tbl_artist, albums.c.artist_id == self.tbl_artist.c.artist_id)

			r = self.db.execute(
				select([
					fact.c.user_id,
					self.tbl_artist.c.name,
					albums
				]).\
				select_from(releases).\
				order_by(desc(albums.c.release_date))).\
				fetchall()

			return r
		except Exception as e:
			raise e