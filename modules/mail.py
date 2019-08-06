import os, json, sendgrid
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

# From a sendgrid contact list id, return contacts info in a dict
def getContacts(list_id:str):
	r_list = sg.client.marketing.contacts.get(query_params={'page_size': 1000 })
	data_list = json.loads(r_list.body.decode('utf-8'))

	users = []
	for recipient in data_list['result']: # retrieve all contacts

		if list_id in recipient['list_ids']: # keep only contact in the given contact list

			user = {
					'id:': recipient['id'],
					'name': recipient['first_name'],
					'email': recipient['email'],
					'list_ids': recipient['list_ids']
				}

			r_recipient = sg.client.marketing.contacts._(recipient['id']).get()
			data_recipient = json.loads(r_recipient.body.decode('utf-8'))

			try:
				user['deezer_user_id'] = data_recipient['custom_fields']['deezer_user_id']
				user['frequency'] = data_recipient['custom_fields']['frequency']
			except Exception as e:
				raise e

			users.append(user)
		
	return users

# Send a mail
def sendMail(mfrom:str, mfromname:str, mto:str, msubject:str, mcontent:str):
	mail = Mail(
		from_email=(mfrom, mfromname),
		to_emails=mto,
		subject=msubject,
		html_content=mcontent)
	r = sg.send(mail)

	return r
