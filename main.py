import json
import requests
from secrets import spotify_user_id,  discover_weekly_id
from datetime import date
from refresh import Refresh

#definimos el ususario y los componentes basicos que se guardaran , com el ussuario,as ncanciones y la playlist 
class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

#lo primero qeu queremos hacer es encontrar las canciones asi que difinimos una funcion que lo haga 
    def find_songs(self):

        print("Finding songs in discover weekly...")
        # Recorrer la lista de canciones y luego agregarlas 
        #esta e sla referencia a la playlist que vamos a isar
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_id)

#definimos el tipo de contenido como Json 
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

#creamos la playlist y agragamos lo guardado y la informacion necesaria 
    def create_playlist(self):
       
        print("Trying to create playlist...")
        today = date.today()

        todayFormatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": todayFormatted + " discover weekly", "description": "Discover weekly rescued once again from the brink of destruction by your friendly neighbourhood python script", "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()

        return response_json["id"]

#las agragamos al la playlist creada ya pudiendo identificarlas 
    def add_to_playlist(self):
        # add all songs to new playlist
        print("Adding songs...")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response.json)

    def call_refresh(self):

        print("Refreshing token")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.find_songs()

#refrescamos la informacion 
a = SaveSongs()
a.call_refresh()
