from flask import Flask, render_template
from modules import *

app = Flask(__name__)

@app.route("/")
def index():
	db = Database()
	r = db.getAllUsers()
	del(db)

	users = list(map(lambda user: {
		'id': user.user_id,
		'last_checked': user.last_check
		}, r))

	return render_template('index.html', users=users)
	
@app.route('/user/<int:user_id>')
def user(user_id):
	db = Database()
	r = db.getReleases(user_id, 30)
	del(db)

	releases = list(map(lambda release: {
		'album_id': release.album_id,
		'artist_id': release.artist_id,
		'artist_name': release.name,
		'title': release.title,
		'release_date': release.release_date,
		'genre_id': release.genre_id,
		'nb_fans': release.nb_fans
		}, r))

	return render_template('releases.html', releases=releases)