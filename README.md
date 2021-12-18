# lightmusicclub

**Light Music Club v1 stable (20211218)**

Light Music Club, created by redneonglow, is a Fediverse picture bot for fans of idol anime. Light Music Club downloads random artwork from Danbooru based on various anime music franchises and posts them to the Fediverse.

Franchises supported are:

* Hibike! Euphonium
* The Idolmaster
* K-On!
* Love Live!
* Show By Rock!!

Light Music Club can post directly to Mastodon and Pleroma instances and is great for use in an hourly cronjob.

**REQUIREMENTS:**

* Python 3.6 or higher
* Mastodon.py and its dependencies
* Requests and its dependencies
* curl

**SET UP THE TOKEN FILE:**

1. Create a Fediverse account for Light Music Club.
2. Set up a token here: https://tinysubversions.com/notes/mastodon-bot/
3. Create a token file by running this command:
   `curl <command you are given> > tokenfile.json`

Note that if you change the password on the account, you will need to create a new token file.

**CONFIGURATION:**

Configuration for Light Music Club is in the form of a JSON file with the following values:

* `allow_nsfw` Allow the bot to possibly download and post NSFW artwork. Valid values are true or false.
* `access_token` Location of the Mastodon access token. See above for instructions on how to create the token file.
* `danbooru_apikey` Danbooru API key.
* `danbooru_username` Danbooru username.
* `picfile` Location of the downloaded picture file.
* `instance` Fediverse instance.
* `visibility` More information below.

See `lightmusicclub.json.example` for an example config file.

**VISIBILITY:**

The visibility setting may be any of the following:

* `direct` (only visible to the bot account)
* `private` (only visible to the bot account's followers)
* `public` (visible to everyone)
* `unlisted` (visible to everyone, but hidden from the public timeline)

In most cases you would want to use either `public` or `unlisted` for the visibility setting.

**EXAMPLE COMMANDS:**

Show help: `./lightmusicclub.py -h`

Show license (Simplified BSD): `./lightmusicclub.py -l`

Show version: `./lightmusicclub.py -v`

Post random idol anime picture to the Fediverse using config file lightmusicclub.json: `./lightmusicclub.py -p lightmusicclub.json`

Post version info to the Fediverse using config file lightmusicclub.json: `./lightmusicclub.py -w lightmusicclub.json`

Enjoy!

-redblade7 aka redneonglow

**FEDIVERSE CONTACT INFO:**

* `@redneonglow@bae.st` / https://bae.st/redneonglow (main)
* `@redneonglow@weeaboo.space` / https://weeaboo.space/redneonglow (backup)
* `@redneonglow@gameliberty.club` / https://gameliberty.club/@redneonglow (backup)

The author runs an instance of Light Music Club here, posting images (including NSFW) every half hour:

* `@LightMusicClub@bae.st` / https://bae.st/LightMusicClub
