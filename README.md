# The Release Note
Every day/week at 9am, get a digest of all the new releases from your favorite artists (if any).

![](http://greird.webfactional.com/img/thereleasenote2.png | width=600)

## Requierements

- Python 3
- A Deezer API Access Token (https://developers.deezer.com/api/explorer)
- A Sendgrid API key (https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api)

## Setup

Clone, fork or download this repository.

Install all dependencies with `pip3 install -r requierements.txt`.

Create api.env file with the following information.
```env
export SENDGRID_API_KEY=''
export DEEZER_ACCESS_TOKEN=''
```
Then `source ./api.env`.

Edit CONFIG in `modules/__init__.py`

## Usage

The Release Note can be used to send newsletters to all recipient from a Sendgrid contact list OR directly to one recipient defined through the terminal.

### How to send a New Releases digest to one user

`python3 the-release-note.py -u 5 -m mail@mail.com -r 7`

This will send all albums from user ID 5's favourite artists and released in the past 7 days to mail@mail.com.

### How to send a personalize New Releases digest to all recipients from a contact list

First you will need to create a Contact List in your Sendgrid acccount. This contact list must come with 2 custom fields:
`deezer_user_id` : It must be an integer and match a Deezer user's ID.
`frequency` : It must be set to `daily` or `weekly`. This is the frequency at which the email will be sent. If not found, it will default to 1.

Now change the value of `contact_list_id` in `modules/__init__.py` to match your own contact list.

Once properly configured, run `python3 the-release-note.py` to send new releases for all recipients in the SendGrid contact list.

Alternatively, you can also specify the contact list ID through the command line:
`python3 the-release-note.py --contactlist 123456`

### Debug mode

Run with `-d` or `--debug` to record debug log.

### How to send the digest on a regular basis

Set up a cron to run the script regularly. 

e.g. To send the newsletter every day at 8am (change path accordingly):
```
0 8 * * * source <yourpath>/api.env ; <yourpath>/python3 <yourpath>/the-release-note.py >> <yourpath>/cron.log 2>&1
```
Note that for users with "weekly" preferences, it will only send the email on Friday, containing new releases from the past 7 days.

## Troubleshooting

### SSL issue with sendgrid

This worked for me.. 

```bash
pip3 install certifi
/Applications/Python\ 3.7/Install\ Certificates.command
```
Update with your Python path accordingly.