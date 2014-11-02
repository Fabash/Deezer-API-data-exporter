import json
import requests
import csv


index = 0
artists = []
tracks = []
token = open("token", "r", encoding = "utf-8").read().rstrip()
user_id = open("user_id", "r", encoding = "utf-8").read().rstrip()
url_artists = "http://api.deezer.com/user/" + user_id + "/artists?access_token=" + token + "&output=json"
url_tracks = "http://api.deezer.com/user/" + user_id + "/tracks?access_token=" + token + "&output=json"
csv_artists = "artists.csv"
csv_tracks = "tracks.csv"


def get_artists(index, artists, url):

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


def get_tracks(index, tracks, url):
    while True:
        r = requests.get(url)
        deezer = r.content;
        deezer = json.loads(deezer.decode("utf-8"))
        data = deezer["data"]
        
        i = 0
        while i <= len(data) - 1:
            element = {}
            element["title"] = data[i]["title"]
            element["artist"] = data[i]["artist"]["name"]
            element["album"] = data[i]["album"]["title"]
            #print(element)
            tracks.append(element)
            i += 1
        
        print(str(len(tracks)) + " fetched tracks.")
        #print(tracks)
        break


def write_artists():
    with open(csv_artists, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["Artists:"])
        for val in artists:
            writer.writerow([val])
    print("Artists successfully written in CSV-file.")

def write_tracks():
    with open(csv_tracks, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["Title:" + ";" + "Artists:" + ";" + "Album:"])
        for val in tracks:
            writer.writerow([val["title"]+ ";" + val["artist"] + ";" + val["album"]])
    print("Tracks written successfully in CSV-file.")


get_artists(index, artists, url_artists)
write_artists()
get_tracks(index, tracks, url_tracks)
write_tracks()
