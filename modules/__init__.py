import sys, getopt
from .deezer import Deezer
from .template import *
from .mail import *
#from pathlib import Path

CONFIG = {
	'log_path' 			: 'logs/', #str(Path.home()) + '/logs/user/',
	'contact_list_id'	: 5497851, # sendgrid contact list id
	'released_since' 	: 1, # in days
	'from_mail' 		: "ensnare@greird.webfactional.com",
	'from_name' 		: "The Release Note",
	}

DEBUG = {
	'active': False,
	'user': {
		'deezer_user_id': 0,
		'username': '',
		'email': '',
	}
}

try:
	opts, args = getopt.getopt(sys.argv[1:], "d", ["debug"])
except getopt.GetoptError:
	print("Available option is -d or --debug to run debug mode.")
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--debug"):
		print("Configuring debug mode...") 
		DEBUG['user']['deezer_user_id'] = int(input("Get new releases for user ID: "))
		DEBUG['user']['username'] = input("Username: ") 
		DEBUG['user']['email'] = input("Send the newsletter to: ")
		DEBUG['active'] = True
		print("Now running in debug mode...") 
		print("Sending new releases from " + DEBUG['user']['username'] + " (" + str(DEBUG['user']['deezer_user_id']) + ") to " + DEBUG['user']['email'] + "...") 
