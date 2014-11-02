import json
import requests
import csv

#Create empty lists to be filled later.
artists = []
tracks = []

#Read the API-Token and User-ID from the respective file.
token = open("token", "r", encoding = "utf-8").read().rstrip()
user_id = open("user_id", "r", encoding = "utf-8").read().rstrip()

#Get your artists and tracks in JSON-format.
url_artists = "http://api.deezer.com/user/" + user_id + "/artists?access_token=" + token + "&output=json"
url_tracks = "http://api.deezer.com/user/" + user_id + "/tracks?access_token=" + token + "&output=json"

#Create variables.
csv_artists = "artists.csv"
csv_tracks = "tracks.csv"


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


#Function for fetching tracks and writing them in the list "tracks".
def get_tracks(tracks, url):
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


#Writing artists in the CSV-file "artists.csv".
def write_artists():
    with open(csv_artists, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["Artists:"])
        for val in artists:
            writer.writerow([val])
    print("Artists successfully written in CSV-file.")

#Writing tracks in the CSV-file "tracks.csv".
def write_tracks():
    with open(csv_tracks, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["Title:" + ";" + "Artists:" + ";" + "Album:"])
        for val in tracks:
            writer.writerow([val["title"]+ ";" + val["artist"] + ";" + val["album"]])
    print("Tracks written successfully in CSV-file.")


#Calling all the functions one after another.
get_artists(artists, url_artists)
write_artists()
get_tracks(tracks, url_tracks)
write_tracks()
