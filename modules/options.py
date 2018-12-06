import sys, getopt

DEBUG = False

def usage():
	print("Available options are")
	print("-d or --debug to record debug logs.")
	print("-u <user_id> or --user <user_id> to get new releases from 1 given user")
	print("-m <email> or --mailto <email> to send only one newsletter to the given email address.")
	print("-u and -m should be used together to send a one shot newsletter to a given user.")
	print("-r <number of days> or --releasedsince <number of days> to send releases from the n previous days (default is 7).")
	sys.exit(2)

try:
	opts, args = getopt.getopt(sys.argv[1:], 'hdu:m:r:', ['help', 'debug', 'user=', 'mail=', 'releasedsince='])
except getopt.GetoptError as e:
	print(e)
	usage()
for opt, arg in opts:
	if opt in ("-h", "--help"):
		usage()
	if opt in ("-d", "--debug"):
		DEBUG = True
		print("Now running in debug mode.") 
	if opt in ("-u", "--user"):
		try:
			deezer_user_id = int(arg)
		except ValueError as e:
			print(e)
			usage()
	if opt in ("-m", "--mail"):
		email = arg
	if opt in ("-r", "--releasedsince"):
		try:
			opt_released_since = int(arg)
		except ValueError as e:
			print(e)
			usage()

try:
	TEST_USER = [{
		'deezer_user_id': deezer_user_id,
		'email': email
	}]
	print("Sending new releases from user ID " + str(TEST_USER[0]['deezer_user_id']) + " to " + TEST_USER[0]['email'])
except NameError:
    TEST_USER = None