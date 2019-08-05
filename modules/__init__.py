from .deezer import Deezer
from .template import *
from .mail import *
from .options import *

CONFIG = {
	# SendGrid configuration
	'from_mail' 		: "the-release-note@greird.webfactional.com",
	'from_name' 		: "The Release Note",
	'contact_list_id'	: "65ed1817-6ed8-48b4-9e1e-579690bf656d", # sendgrid contact list id
	# paths
	'log_path' 			: './logs/user/'
	}

if contact_list_id:
	CONFIG['contact_list_id'] = contact_list_id