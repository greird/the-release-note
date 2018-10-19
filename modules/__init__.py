from .deezer import Deezer
from .template import *
from .mail import *
from .options import *

CONFIG = {
	'log_path' 			: 'logs/',
	'contact_list_id'	: 5497851, # sendgrid contact list id
	'released_since' 	: 1, # in days
	'from_mail' 		: "the-release-note@greird.webfactional.com",
	'from_name' 		: "The Release Note",
	}