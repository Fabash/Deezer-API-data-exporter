Deezer-API-data-exporter
========================

This small script exports your subscribed artists and your favourite tracks from Deezer. It is written in Python 3.4.

To start the script, insert your User-ID in the file "user_id" and your current Deezer-API-Key in the file "token". You can generate your temporary API-Key here: http://developers.deezer.com/api/explorer?url=user/me

Then, just run "deezer_api.py". Two semicolon-seperated CSV-Files named "artists.csv" and "tracks.csv" will be created, containing the respective data.

I'll document the code as soon as I have some time.

Obtain Access Token
===================
See https://developers.deezer.com/api/oauth

First, you need to create and register an App(lication) with a redirect URI
See: https://developers.deezer.com/myapps/app/<app_id>/edit
You will retrieve:
- AppID
- App secret

Go to https://connect.deezer.com/oauth/auth.php?app_id=YOUR_APP_ID&redirect_uri=YOUR_REDIRECT_URI&perms=basic_access,manage_library
The HTTPS response will give you the code in the form: https://<REDIRECT_URI>?code=<XXXXXXXX>

Then, go to the following URL to receive the access token (valid for 1 hour):
https://connect.deezer.com/oauth/access_token.php?app_id=YOU_APP_ID&secret=YOU_APP_SECRET&code=THE_CODE_FROM_ABOVE

HTTPS Respnse: access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
