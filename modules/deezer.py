import requests, re, json, time, os
from datetime import datetime
from pathlib import Path

class Deezer(object):
	"""This is a simple wrapper for the Deezer API"""
	def __init__(self, access_token=None, cache_duration=7200, quota_limit=50, quota_delay=5, tries=2):
		self.access_token = access_token
		self.cache_duration = cache_duration
		self.quota_limit = quota_limit
		self.quota_delay = quota_delay
		self.tries = tries
		self.quota = 0 # what's left

	def checkQueryQuota(self):
		"""
			Check API quota, if exceeded, wait and reset. Then decrease quota by 1.
		"""
		self.quota
		if self.quota < 1:
			time.sleep(self.quota_delay)
			self.quota = self.quota_limit
		self.quota -= 1

	def get(self, endpoint, **kwargs):
		"""
			Query a Deezer API endpoint with the proper parameter and output a clean response object
		"""
		get_cached = self.memoize(requests.get)

		query = "https://api.deezer.com" + str(endpoint)
		if self.access_token != None:
			query = query + "?access_token=" + self.access_token

		param = {
			'limit': 2000,
			'nb': 10000,
			'cache': True
		}

		# If user passed some params, overwrite the default ones
		if kwargs is not None:
			for key, value in kwargs.items():
				param[key] = value

			if param['nb'] < param['limit']:
				param['limit'] = param['nb']

		# Add params to url
		for key, value in param.items():
			query += "&" + key + "=" + str(value)

		self.checkQueryQuota()
		if param['cache'] == True: 
			for i in range(self.tries):
				try:
					raw_r = get_cached(query)
					r = raw_r.json()
				except OSError as e:
					print(e)
					continue
				except json.decoder.JSONDecodeError:
					print("JSON error !")
					print(raw_r)
					continue
				break
			else: 
				# All attempts to retrieve data failed. Abort mission !
				return False
		else:
			# TODO: fix simplejson error as above
			raw_r = requests.get(query)
			r = raw_r.json()

		response = r['data'] if 'data' in r.keys() else r

		# keep on fetching items until the last page is reached
		if 'next' in r.keys():
			while ('next' in r.keys()) & (int(param['nb']) > len(response)):
				self.checkQueryQuota()
				r = get_cached(r['next']).json() if param['cache'] == True else requests.get(r['next']).json()
				response += r['data'] if 'data' in r.keys() else r

		return response

	def getNewReleases(self, userId:int, number_of_days:int=7):
		number_of_days = number_of_days
		userId = userId
		new_releases = []
		now = datetime.now()
		base_path = os.path.dirname(os.path.abspath(__file__))

		stopwords = [line.rstrip('\n').lower() for line in open(os.path.join(base_path, '../models/stopwords'))]
		banned_artists = [line.rstrip('\n').lower() for line in open(os.path.join(base_path, '../models/banned_artists'))]
		
		# For each artist, check new releases
		fav_artists = self.get("/user/" + str(userId) + "/artists")

		for artist in fav_artists:
			if artist['name'].lower() not in banned_artists:
				albums = self.get("/artist/" + str(artist['id']) + "/albums")

				if albums != False:
					for album in albums:
						delta = abs((now - self.date(album['release_date'])).days)

						if delta < number_of_days:
							album['artist'] = artist
							new_releases.append(album)

		def findStopWords(string):
			for stopword in stopwords:
				if stopword in string.lower():
					return True

		# Post-processing to remove unwanted releases
		new_releases = list(filter(lambda album:  album['record_type'] == 'album', new_releases))
		new_releases = list(filter(lambda album:  album['tracklist'] != '', new_releases))
		new_releases = list(filter(lambda album:  album['artist']['name'].lower() not in banned_artists, new_releases))
		new_releases = list(filter(lambda album: not findStopWords(album['title']), new_releases))
		return new_releases 

	"""
		HELPERS
	"""
	def printjson(self, func):
		return print(json.dumps(func, sort_keys=True, indent=4))

	def date(self, d):
		format = "%Y-%m-%d"
		return datetime.strptime(d, format)

	def memoize(self, func):
		"""
			Cache wrapper function
		"""
		cache = dict()
		
		def memoized_func(*args):
			if args in cache:
				if (time.time() - cache[args]['insert_date']) < self.cache_duration:
					return cache[args]['result']

			result = func(*args)
			cache[args] = {
				'result': result,
				'insert_date': time.time()
			}

			return result

		return memoized_func