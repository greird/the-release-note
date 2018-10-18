import os, json, logging
from modules import *
from pathlib import Path

CONFIG = {
	'log_path' 			: str(Path.home()) + '/logs/user/',
	'contact_list_id'	: 5497851, # sendgrid contact list id
	'released_since' 	: 1, # in days
	'from_mail' 		: "",
	'from_name' 		: "The Release Note",
	'debug' 			: False, # if True, will send newsletter to test_user only
	'test_user' : [{
		'email'			: "",
		'deezer_user_id': 158316,
		'username'		: "Test User"
		}]	
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a file handler
handler = logging.FileHandler(CONFIG['log_path'] + 'ensnare_info.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

dzr = Deezer(
	access_token=os.environ.get('ACCESS_TOKEN'),
	app_id=os.environ.get('APP_ID'),
	app_secret=os.environ.get('APP_SECRET')
	)

users = getContacts(CONFIG['contact_list_id']) if CONFIG['debug'] == False else CONFIG['test_user']
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
