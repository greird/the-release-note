import logging, datetime, sys
from modules import *

args = parser.parse_args()

start_time = datetime.datetime.now()

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

if args.debug:
	print("Now running in debug mode.") 
	logger.setLevel(logging.DEBUG)
	logger.addHandler(debug_handler)

dzr = Deezer()

weekday = datetime.datetime.today().weekday()

# Retrieve users, either from args of a contact list
if args.user:
	args.do_not_send = True if not args.email else False
	users = [{ 'deezer_user_id': int(user), 'email': args.email } for user in args.user]
else:
	try:
		users = getContacts(args.contact_list_id) if args.contact_list_id else getContacts(CONFIG['contact_list_id'])
	except Exception as e:
		logger.info("An error occured while trying to retrieve the contact list.")
		logger.debug(e)
		sys.exit(2)

logger.info(str(len(users)) + ' users found.')
logger.debug(users)

for user in users:
	print("Checking new releases for user id " + str(user['deezer_user_id']) + "...")
	logger.info("Checking new releases for user id " + str(user['deezer_user_id']) + "...")

	if args.released_since:
		released_since = args.released_since 
	else:
		try:
			# For weekly users, send new releases on friday only
			if weekday != 4 and user['frequency'] == 'weekly':
				logger.debug("Skipping this user as he's a weekly user and will only receive new releases on Friday.")
				continue
			else:
				released_since = {
					'daily': 1,
					'weekly': 7
				}.get(user['frequency'], 1)
		except KeyError as e:
			logger.debug("Frequency setting not found. Fallback to default value.")
			released_since = 1
		except Exception as e:
			logger.debug("An error occured while trying to retrieve the frequency setting:")
			logger.debug(e)
			continue

	try:
		new_releases = dzr.getNewReleases(user['deezer_user_id'], released_since)
	except IOError as e:
		logger.debug("Stopwords and banned artists could not be retrieved.")
		logger.debug(e)
		sys.exit(2)
	except Exception as e:
		logger.debug(e)
		sys.exit(2)

	nb_releases = len(new_releases)
	
	logger.info("User id " + str(user['deezer_user_id']) + " has " + str(nb_releases) + " albums released in the past " + str(released_since) + " days.")
	logger.debug(new_releases)

	if nb_releases < 1:
		continue

	# Store new releases into database
	try:
		db = Database()
		db.storeNewReleases(new_releases, user['deezer_user_id'])
		del(db)
	except Exception as e:
		logger.info("An error occured while trying to store the new releases in the database.")
		logger.debug(e)	

	# Send new releases by email
	subject = "♩ Have you listened to " + new_releases[0]['artist']['name'] + "'s new album ?"
	contenthtml = get_template(new_releases, user['deezer_user_id'])
	 
	if not args.do_not_send:
		try:
			send = sendMail(CONFIG['from_mail'], CONFIG['from_name'], user['email'], subject, contenthtml)
			logger.info("Sending email - Status: " + str(send.status_code))
			logger.debug(send.headers)
		except Exception as e:
			logger.info("An error occured while trying to send the mail.")
			logger.debug(e)
			sys.exit(2)

print('Done')
logger.info("Done in %s seconds " % (datetime.datetime.now() - start_time).total_seconds())