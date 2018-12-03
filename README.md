# The Release Note
Get a digest of major updates about your favorite artists every day, week or month in your inbox.

## Requierements

- Python 3
- A Deezer API app ID, SECRET KEY and ACCESS TOKEN (https://developers.deezer.com/myapps)
- A Sendgrid API key (https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api)

## Setup

Clone, fork or download this repository.

Install all dependencies with `pip3 install -r requierements.txt`.

Create api.env file with the following information.
```env
export SENDGRID_API_KEY=''
export ACCESS_TOKEN=''
export APP_ID=''
export APP_SECRET=''
```
Then `source ./api.env`.

Edit CONFIG in `modules/__init__.py`

## Usage

The Release Note can be used to send newsletters to all recipient from a Sendgrid contact list OR directly to one recipient defined through the terminal.

### Sending directly to one user

Run `python3 the-release-note.py -u 5 -m mail@mail.com -r 7`. This will send all albums from user 5's favourite artists and released in the past 7 days to mail@mail.com.

### Sending to a contact list

First you will need to create a Contact List in your Sendgrid acccount. This contact list must come with 2 custom fileds:
`deezer_user_id` : It must be an integer and match a Deezer user's ID.
`frequency` : It must be set to `daily` or `weekly`. This is the frequency at which the email will be sent.

Now change the value of `contact_list_id` in `modules/__init__.py` to match your own contact list.

Once properly configured, run `python3 the-release-note.py` to send new releases for all recipients in the SendGrid contact list.

### Debug mode

Run with `-d` or `--debug` to record debug log.

### Sending the newsletter on a regular basis

Set up a cron to run the script regularly. 

e.g. To send the newsletter every day at 8am (change path accordingly):
```
0 8 * * * source <yourpath>/api.env ; <yourpath>/python3 <yourpath>/the-release-note.py >> <yourpath>/cron.log 2>&1
```

## Troubleshooting

### SSL issue with sendgrid

```bash
pip3 install certifi
/Applications/Python\ 3.7/Install\ Certificates.command
```
Update with your Python path accordingly.