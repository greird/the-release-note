from .deezer import Deezer
from .template import *
from .mail import *
from .options import *

CONFIG = {
	# SendGrid configuration
	'from_mail' 		: "the-release-note@greird.webfactional.com",
	'from_name' 		: "The Release Note",
	'contact_list_id'	: 5497851, # sendgrid contact list id
	# paths
	'log_path' 			: './logs/user/'
	}