import os, json, sendgrid
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

# From a sendgrid contact list id, return contacts info in a dict
def getContacts(list_id:int):
	params = {'page': 1, 'page_size': 1000, 'list_id': list_id}
	r = sg.client.contactdb.lists._(list_id).recipients.get(query_params=params)
	data = json.loads(r.body.decode('utf-8'))
	
	users = []
	for recipient in data['recipients']:
		user = {
			'email': recipient['email'],
		}

		for custom_field in recipient['custom_fields']:
			user[custom_field['name']] = custom_field['value']

		users.append(user)

	return users

# Send a mail
def sendMail(mfrom:str, mfromname:str, mto:str, msubject:str, mcontent:str):
	mail = Mail(
		Email(mfrom, mfromname), 
		msubject, 
		Email(mto), 
		Content("text/html", mcontent)
		)
	r = sg.client.mail.send.post(request_body=mail.get())
	return r