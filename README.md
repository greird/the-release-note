# The Release Note
Every week, get a digest of major updates about your favorite artists and you activity on Deezer.

### Setup

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

### Usage

Once properly configured, run `python3 the-release-note.py` to send new releases for all recipients in the SendGrid contact list.

Run with `-d` or `--debug` to record debug log (containing dumps of api responses).

Run `python3 the-release-note.py --user 5 --mailto mail@mail.com` to send new releases from user ID 5 to mail@mail.com.

#### Send the newsletter regulary

Set up a cron to run the script regularly. 

e.g. To send the newsletter every day at 8am (change path accordingly):
```
0 8 * * * source <yourpath>/api.env ; <yourpath>/python3 <yourpath>/the-release-note.py >> <yourpath>/cron.log 2>&1
```

### Troubleshooting

#### SSL issue with sendgrid

```bash
pip3 install certifi
/Applications/Python\ 3.7/Install\ Certificates.command
```
Update with your Python path accordingly.