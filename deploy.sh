#!/usr/bin/env sh

# abort on errors
set -e

ssh greird@greird.webfactional.com
cd webapps/the_release_note

# Fetch all new files and reset local repo to what have been fetched
git fetch --all
git reset --hard origin/master

# update python modules if needed
. venv/bin/activate
pip install -r requirements.txt 

exit