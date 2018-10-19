import os, json, logging
from modules import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a file handler
handler = logging.FileHandler(CONFIG['log_path'] + 'info_the_release_note.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

dzr = Deezer(
	access_token=os.environ.get('ACCESS_TOKEN'),
	app_id=os.environ.get('APP_ID'),
	app_secret=os.environ.get('APP_SECRET')
	)

users = getContacts(CONFIG['contact_list_id']) if DEBUG['active'] == False else DEBUG['user']
logger.info(str(len(users)) + ' users found.')

for user in users:

	logger.info("Get new releases for user id " + str(user['deezer_user_id']) + "...")
	
	new_releases = dzr.getNewReleases(user['deezer_user_id'], CONFIG['released_since'])
	nb_releases = len(new_releases)
	
	logger.info("User id " + str(user['deezer_user_id']) + " has " + str(nb_releases) + " new releases available.")
	logger.debug(json.dumps(new_releases, sort_keys=True, indent=4, separators=(',', ': ')))

	if nb_releases < 1:
		continue

	subject = "Hey " + user['username'] + ", " + new_releases[0]['artist'] + " released a new album ! 💿💿💿"
	contenthtml = get_template(new_releases)
	 
	send = sendMail(CONFIG['from_mail'], CONFIG['from_name'], user['email'], subject, contenthtml)
	logger.info("Sending email - Status: " + str(send.status_code))
	logger.debug(send.headers)
