#!/bin/python3
import json
import requests
import csv
import sys
import os

#Check command line arguments
dir='/tmp'
data_dir=dir
user_dir = data_dir

try:
    user_name=sys.argv[1]
except IndexError:
    user_name="default"

#Create empty lists to be filled later.
artists = []
albums = []
tracks = []

tracks_index=25
#Read the API-Token and User-ID from the respective file.
user_id = open(user_name + "_user_id", "r", encoding = "utf-8").read().rstrip()
token   = open(user_name + "_token",   "r", encoding = "utf-8").read().rstrip()

url_api_deezer = "https://api.deezer.com"
url_api_search = url_api_deezer + "/search"

#Get your artists and tracks in JSON-format.
url_user_id = url_api_deezer + "/user/" + user_id
url_artists = url_user_id + "/artists?access_token=" + token + "&output=json"
url_tracks  = url_user_id + "/tracks?access_token="  + token + "&output=json"
url_albums  = url_user_id + "/albums?access_token="  + token + "&output=json"
# Use POST HTTP request to update/add datas
post_request_arg = "&request_method=POST"

# MP3 data files
mp3_artists_albums_file = data_dir + "/" + user_name + "_MP3_ALBUMS.txt"

# CSV output files
csv_artists = data_dir + "/" + user_name + "_deezer_artists.txt"
csv_albums  = data_dir + "/" + user_name + "_deezer_albums.txt"
csv_tracks  = data_dir + "/" + user_name + "_deezer_tracks.txt"

def mp3_add_albums_and_artits():
    mp3file = mp3_artists_albums_file
    print("***** Add MP3 ALBUMS from file $[mp3file} *****\n")

    with open(mp3file,"r") as file:
        for line in file.readlines():
            try:
                (artist,album)=line.split('/')

                print("* Searching: Artist = %s, Album = %s\n" % (artist,album))

                # --- Artist
                # Search Artist ID
                url_search = url_api_search + "q=artist:" + '"' + artist + '"'
                # Add Artist if not followed
                try:
                    r = requests.get(url_search)
                    deezer = r.content
                    data = json.loads(deezer.decode("utf-8"))
                    an_object=data[0]
                    id=an_object['id']
                    name=an_object['name']
                    print("  -> Found artist %s (id=%)" % (artist,str(id)))
                except:
                    print("mp3_add_albums_and_artits: ERROR - Artist [" + artist + "] NOT added")

                # --- Album
                # Search Album ID
                url_search = url_api_search + "q=album:" + '"' + album + '"'
                r = requests.get(url_search)
                deezer = r.content
                deezer = json.loads(deezer.decode("utf-8"))
                data = deezer["data"]
                total = data['total']
                f_album_found = false
                idx=0

                # Add Album if not followed
                an_object=data[0]
                id=an_object['id']
                title=an_object['title']
                print("  -> Found album %s (id=%)" % (album,str(id)))
            except ValueError:
                print("[X] Syntax error in line:[" + line.strip('\n') + "]")
            except IndexError:
                print("[WARNING] Album [" + album + "] NOT found")
    print("")

#Function for fetching artists and writing them in the list "artists".
def get_artists(artists, url):
    while True:
        r = requests.get(url)
        deezer = r.content
        deezer = json.loads(deezer.decode("utf-8"))
        data = deezer["data"]
    
        i = 0
        while i <= len(data) - 1:
            artists.append((data[i]["name"]))
            i += 1
    
        try:
            url = deezer["next"]
        except:
            print(str(len(artists)) + " fetched artists.")
            #print(artists)
            break

#Function for fetching albums and writing them in the list "albums".
def get_albums(albums, url):
    while True:
        local_url=url+"&index=25"
        r = requests.get(url)
        deezer = r.content
        deezer = json.loads(deezer.decode("utf-8"))
        data = deezer["data"]
    
        i = 0
        while i <= len(data) - 1:
            albums.append((data[i]["title"]))
            i += 1
    
        try:
            url = deezer["next"]
        except:
            print(str(len(albums)) + " fetched albums.")
            #print(albums)
            break


#Function for fetching tracks and writing them in the list "tracks".
def get_tracks(tracks, url):
    # Read total number of tracks
    r = requests.get(url)
    deezer = r.content
    deezer = json.loads(deezer.decode("utf-8"))
    total=deezer["total"]
    print("Found " + str(total) + " total tracks.")
    idx = 0

    # Fetch tracks by groups of 25
    while idx <= total:
        idx_url=url+"&index="+str(idx)
        print("* URL="+idx_url)
        #while True:
        r = requests.get(idx_url)
        deezer = r.content;
        deezer = json.loads(deezer.decode("utf-8"))
        data = deezer["data"]
        #print(data)
        i = 0
        while i <= len(data) - 1:
            #print("..."+str(i))
            element = {}
            element["title"] = data[i]["title"]
            element["artist"] = data[i]["artist"]["name"]
            element["album"] = data[i]["album"]["title"]
            print(data[i]["title"])
            tracks.append(element)
            i += 1
        idx += 25
        #break
    #print(tracks)
    print(str(len(tracks)) + " fetched tracks.")
        

#Writing artists in the CSV-file
def write_artists():
    artists.sort()
    with open(csv_artists, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        #writer.writerow(["Artists:"])
        for val in artists:
            writer.writerow([val])
    print("Artists successfully written in CSV-file." + csv_artists)

# Writing albums in the CSV-file
def write_albums():
    albums.sort()
    with open(csv_albums, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        #writer.writerow(["Albums:"])
        for val in albums:
            writer.writerow([val])
    print("Albums successfully written in CSV-file." + csv_albums)

#Writing tracks in the CSV-file
def write_tracks():
    #tracks.sort()
    with open(csv_tracks, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        #writer.writerow(["Title:" + ";" + "Artists:" + ";" + "Album:"])
        for val in tracks:
            #writer.writerow([val["artist"] + "#" + val["title"]+ "#" + val["album"]])
            writer.writerow([val["title"]+ "#" +val["artist"]])
    print("Tracks written successfully in CSV-file." + csv_tracks)

#Calling all the functions one after another.

#mp3_add_albums_and_artits()
#exit()
get_artists(artists, url_artists)
write_artists()

get_albums(albums, url_albums)
write_albums()

get_tracks(tracks, url_tracks)
write_tracks()
