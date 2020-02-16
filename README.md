# The Release Note
Every day/week at 9am, get a digest of all the new releases from your favorite artists (if any).

<img src="http://greird.webfactional.com/img/thereleasenote2.png" width="500">

## Requirements

All you need is Python3 and a [Sendgrid API key](https://app.sendgrid.com/settings/api_keys) (a free Sendgrid account is enough).

## Setup

1. Clone, fork or download this repository.
2. Install all dependencies `pip3 install -r requirements.txt`.
3. Create a credentials.env file with the lines `export SENDGRID_API_KEY='YOUR_API_KEY'` and replace `YOUR_API_KEY` with your own key. Load it with `source ./credentials.env`.
4. Add `export DATABASE='postgresql://login:password@host/database'`, replacing login, password, host and database
5. Run `psql postgresql://login:password@host/database -f sql/create.sql` to create all necessary tables
6. Edit the configuratin accordingly in `modules/__init__.py`.
7. Launch the script (see Usage below).

## Usage

The Release Note can be used to send newsletters to all recipient from a Sendgrid contact list OR directly to one recipient defined through the terminal.

```pycon
usage: the-release-note.py [-h] [-d] [-u DEEZER_ID EMAIL]
                           [-c SENDGRID_CONTACT_LIST_ID] [-s NUMBER_OF_DAYS]
                           [-n]

Sending new releases to a contact list or a given user.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug mode.
  -u DEEZER_ID EMAIL, --user DEEZER_ID EMAIL
                        Send all new releases from DEEZER_ID to EMAIL.
  -c SENDGRID_CONTACT_LIST_ID, --contact-list SENDGRID_CONTACT_LIST_ID
                        Send a personalized new releases digest to all
                        recipients of a Sendgrid contact list.
  -s NUMBER_OF_DAYS, --since NUMBER_OF_DAYS
                        Keep only the albums released since a given number of
                        days.
  -n, --no-mail         Do not send any email.
```

### Sending a New Releases digest to one user

`python3 the-release-note.py -u 5 mail@mail.com -s 7`

This will send all albums from user ID 5's favourite artists, released in the past 7 days, to mail@mail.com.

### Senging a personalize New Releases digest to all recipients from a contact list

First you will need to create a Contact List in your Sendgrid acccount. This contact list must come with 2 custom fields:
`deezer_user_id` : It must be an integer and match a Deezer user's ID.
`frequency` : It must be set to `daily` or `weekly`. This is the frequency at which the email will be sent. If not found, it will default to `daily`.

Now change the value of `contact_list_id` in `modules/__init__.py` to match your own contact list.

Once properly configured, run `python3 the-release-note.py` to send new releases for all recipients in the SendGrid contact list.

Alternatively, you can also specify the contact list ID through the command line:
`python3 the-release-note.py --contact-list <SENDGRID_CONTACT_LIST_ID>`

### Sending the digest on a regular basis

Set up a cron to run the script regularly. 

e.g. To send the newsletter every day at 8am (change path accordingly):
```
0 8 * * * source <yourpath>/credentials.env ; <yourpath>/python3 <yourpath>/the-release-note.py >> <yourpath>/cron.log 2>&1
```
Note that for users with "weekly" preferences, it will only send the email on Friday, containing new releases from the past 7 days.

### Debug mode

Run with `-d` or `--debug` to record debug log.

## Filtered new released

Only Albums and Single with a valid tracklist will appear in the digest. In addition, some artists or albums are banned.

### Banned artists

Some artists are banned from appearing in the digest. For instance, The Beatles are banned because they are unlikely to release any real new material. Unfortunately, new content with wrong release date is frequently delivered to Deezer, hence the necessity of this filter.

The list of banned artist is in `models/banned_artists`. 
To ban an artist, simply add one to the list `echo The Beatles >> models/banned_artists`

### Stopwords

If a stopword appear in a new release title, the content will be filtered. This is done to prevent shitty content (e.g. Karaoke or cover version) to appear in the digest. 

The list of stopwords is in `models/stopwords`. 
To add a stopword, simply add one to the list `echo MY_STOPWORD >> models/stopwords`

## Troubleshooting

### SSL issue with sendgrid

This worked for me.. 

```bash
pip3 install certifi
/Applications/Python\ 3.7/Install\ Certificates.command
```
Update with your Python path accordingly.
