import argparse

parser = argparse.ArgumentParser(description='Sending new releases to a contact list or a given user.')

parser.add_argument('-d', '--debug',
	const=True,
	action='store_const',
	help='Enable debug mode.')

parser.add_argument('-u', '--user', 
	nargs='+', 
	metavar='DEEZER_ID',
	dest='user',
	help='Retrieve new releases for DEEZER_ID. Can be multiple DEEZER_ID.')

parser.add_argument('-m', '--mail', 
	type=str,
	metavar='EMAIL',
	dest='email',
	help='Send all new releases found to EMAIL.')

parser.add_argument('-c', '--contact-list', 
	type=str,
	metavar='SENDGRID_CONTACT_LIST_ID',
	dest='contact_list_id',
	help='Send a personalized new releases digest to all recipients of a Sendgrid contact list.')

parser.add_argument('-s', '--since', 
	metavar='NUMBER_OF_DAYS',
	type=int,
	dest='released_since',
	help='Keep only the albums released since a given number of days.')

parser.add_argument('-n', '--no-mail',
	const=True,
	action='store_const',
	dest='do_not_send',
	help='Do not send any email.')