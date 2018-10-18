# deezer-digest
Every week, get a digest of major updates about your favorite artists and you activity on Deezer.

Create api.env file with the following information.
```
export SENDGRID_API_KEY=''
export ACCESS_TOKEN=''
export APP_ID=''
export APP_SECRET=''
```

Then `source ./api.env`.

### Troubleshooting

#### SSL issue with sendgrid

```bash
pip3 install certifi
/Applications/Python\ 3.7/Install\ Certificates.command
```
Update with your Python path accordingly.