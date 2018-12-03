import os, json, logging, datetime
from modules import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a file handler for INFO
handler = logging.FileHandler(CONFIG['log_path'] + 'info_the_release_note.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
# create a file handler for DEBUG
debug_handler = logging.FileHandler(CONFIG['log_path'] + 'debug_the_release_note.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

if DEBUG == True:
	logger.setLevel(logging.DEBUG)
	logger.addHandler(debug_handler)

dzr = Deezer(
	access_token=os.environ.get('ACCESS_TOKEN'),
	app_id=os.environ.get('APP_ID'),
	app_secret=os.environ.get('APP_SECRET')
	)

weekday = datetime.datetime.today().weekday()

users = getContacts(CONFIG['contact_list_id']) if TEST_USER == None else TEST_USER
logger.info(str(len(users)) + ' users found.')

for user in users:

	logger.info("Get new releases for user id " + str(user['deezer_user_id']) + "...")

	# If released_since has not been defined through terminal, check if already defined in User (sendgrid value)
	if 'released_since' not in locals():
		try:
			if weekday == 4 and user['frequency'] == 'weekly': # For weekly, send new releases on friday only
				continue

			released_since = {
				'daily': 1,
				'weekly': 7
			}.get(user['frequency'], 7)
		except KeyError as error:
			logger.debug("Frequency setting not found. Fallback to default value.")
			released_since = 7

	new_releases = dzr.getNewReleases(user['deezer_user_id'], released_since)
	nb_releases = len(new_releases)
	
	logger.info("User id " + str(user['deezer_user_id']) + " has " + str(nb_releases) + " albums released in the past " + str(released_since) + " days.")
	logger.debug(json.dumps(new_releases, sort_keys=True, indent=4, separators=(',', ': ')))

	if nb_releases < 1:
		continue

	subject = "♩ Have you listened to " + new_releases[0]['artist'] + "'s new album ?"
	contenthtml = get_template(new_releases)
	 
	send = sendMail(CONFIG['from_mail'], CONFIG['from_name'], user['email'], subject, contenthtml)
	logger.info("Sending email - Status: " + str(send.status_code))
	logger.debug(send.headers)
