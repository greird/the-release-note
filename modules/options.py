import argparse

parser = argparse.ArgumentParser(description='Sending new releases to a contact list or a given user.')

parser.add_argument('-d', '--debug',
	const=True,
	action='store_const',
	help='Enable debug mode.')

parser.add_argument('-u', '--user', 
	nargs=2, 
	metavar=('DEEZER_ID', 'EMAIL'),
	dest='user',
	action='append',
	help='A Deezer user id and an email address.')

parser.add_argument('-c', '--contact-list', 
	type=str,
	dest='contact_list_id',
	help='A Sendgrid contact list ID.')

parser.add_argument('-s', '--since', 
	metavar='NUMBER_OF_DAYS',
	type=int,
	dest='released_since',
	help='Keep only the albums released since a given number of days.')

args = parser.parse_args()