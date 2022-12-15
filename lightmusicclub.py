#!/usr/bin/env python3
#
# Light Music Club 
# 
# A bot which posts artwork based on various idol anime franchises to the
# Fediverse
#
# Copyright (c) 2021-22, redneonglow
# All rights reserved.
#
# Includes code from Dark Web Mystery Bot v4 stable (20200403)
# Copyright (c) 2019-20, redneonglow
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from mastodon import Mastodon,MastodonError
import argparse,json,requests,secrets,sys

#program version
progver = "2 stable (20221215)"

#anime franchises
franchises = ["hibike!_euphonium","idolmaster","k-on!","love_live!","show_by_rock!!"]

#ratings (general is tripled to make NSFW odds 50/50)
ratings = ["rating:general","rating:general","rating:general","rating:sensitive","rating:questionable","rating:explicit"]

#open json access token
def readtoken(token):
    try:
        with open(str(token)) as replyfile:
            json_obj = json.load(replyfile)
    except OSError as err:
            print("ERROR:",err,'\n')
            sys.exit(1)
    
    return json_obj["access_token"]

#read config file, return json config values
def readconfig(config):
    try:
        configfile = open(config,"r")
        configjson = configfile.read()
    except OSError:
        print("ERROR: Cannot open/read config file!")
        sys.exit(1)

    try:
        configvalues = json.loads(configjson) 
    except json.JSONDecodeError:
        print("ERROR: Not a valid config file!")
        sys.exit(1)

    return configvalues

#download image from danbooru
#returns true if downloaded picture is nsfw, false if sfw
def downloadimage(user,key,picfile,nsfw):
    if nsfw:
        picrating = secrets.choice(ratings)
    else:
        picrating = ratings[0]

    try:
        urlstring = str("https://danbooru.donmai.us/posts.json?random=true&tags=" + secrets.choice(franchises) + "+" + picrating + "&rating=s&limit=1")
        request = requests.get(urlstring,auth=(user,key))
    except ConnectionError as err:
        print("ERROR:",err,'\n')
        sys.exit(1)

    try:
        request = request.json()
    except json.JSONDecodeError:
        print("ERROR: Error requesting file from Danbooru!")
        sys.exit(1)
    request = request[0]["large_file_url"]
    reqimage = requests.get(request)
    try:
        with open(picfile,"wb") as imagefile:
            imagefile.write(reqimage.content)
    except OSError as err:
        print("ERROR:",err,'\n')
        sys.exit(1)

    if picrating == ratings[0]:
        return False
    else:
        return True

#returns the main version line as a string
#used in version and license commands
def verline():
    return str("Light Music Club v" + progver)

#return part two of version info as string
def verpart2():
    return str("A Fediverse picture bot by redneonglow.\nMore info: https://github.com/redblade7/lightmusicclub")

#shows version info
def optversion():
    print(verline())
    print(verpart2())

#shows license info
def optlicense():
    print(verline())
    print("\nCopyright (c) 2021-22, redneonglow\nAll rights reserved.\n")
    print("Redistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n")
    print("1. Redistributions of source code must retain the above copyright notice, this\n   list of conditions and the following disclaimer.")
    print("2. Redistributions in binary form must reproduce the above copyright notice,\n   this list of conditions and the following disclaimer in the documentation\n   and/or other materials provided with the distribution.\n")
    print("THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"\nAND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\nIMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE\nFOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\nDAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR\nSERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\nCAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\nOR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\nOF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")

#post version info to fediverse (unlisted)
def optpostver(baseurl,token):

    try:
        mastodon = Mastodon(api_base_url=str(baseurl),access_token=readtoken(str(token)))
        mastodon.status_post(verline()+'\n'+verpart2(),visibility="unlisted")
    except MastodonError as err:
        print("ERROR:",err,'\n')
        sys.exit(1)

    print("Successfully posted version info to " + str(baseurl) + '!')

#post picture to fediverse
def optpostpic(baseurl,token,vis,picfile,nsfw):
    try:
        mastodon = Mastodon(api_base_url=str(baseurl),access_token=readtoken(str(token)))
        picture = mastodon.media_post(picfile)
        mastodon.status_post(".",media_ids=picture,sensitive=nsfw,visibility=str(vis))
    except MastodonError as err:
        print("ERROR:",err,'\n')
        sys.exit(1)

    print("Successfully posted picture to " + str(baseurl) + '!')

#main
def main():
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--license",help="Show license info",action="store_true")
    parser.add_argument("-v","--version",action="store_true",help="Show version info")
    parser.add_argument("-w","--postversion",help="Post version info to Fediverse, always unlisted, using settings in config file CONFIG",type=str,metavar="CONFIG")
    parser.add_argument("-p","--postpic",help="Download picture from Danbooru and post it to the Fediverse, using settings in config file CONFIG.",type=str,metavar="CONFIG")

    args = parser.parse_args()

    if args.license:
        optlicense()
    elif args.version:
        optversion()
    elif args.postversion:
        configvalues = readconfig(args.postversion)
        optpostver(configvalues['instance'],configvalues['access_token'])
    elif args.postpic:
        configvalues = readconfig(args.postpic)
        ispicnsfw = downloadimage(configvalues['danbooru_username'],configvalues['danbooru_apikey'],configvalues['picfile'],configvalues['allow_nsfw'])
        optpostpic(configvalues['instance'],configvalues['access_token'],configvalues['visibility'],configvalues['picfile'],ispicnsfw)
    else:
        print("ERROR: Invalid command!")
        parser.print_help()
        sys.exit(2)
        
if __name__ == "__main__":
    main()
    sys.exit(0)
