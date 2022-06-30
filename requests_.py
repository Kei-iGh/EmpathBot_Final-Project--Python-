import urllib.request
import requests
import json
import threading
from threading import Thread
login = "chatbotowner"
CLIENT_ID = "4chwl18cmbzrd9mvmvyprbea8fnylx"
CLIENT_SECRET = "6wprijwvszl27hts4jjzlyzml6gbmm"

class req():

    def make_request(self,URL):

        token = 'oauth:omq73dclve4qehac8nfmtfg3jlb7p0'

        header    = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {token}" }

        req = urllib.request.Request(URL, headers=header)
        recv = urllib.request.urlopen(req)
    
        return json.loads(recv.read().decode("utf-8"))

    
    def get_current_online_streams(self):

        streamer  = [
            f"{login}"
        ]
        URL = "https://api.twitch.tv/helix/streams?user_login="
        resps = []
        online_streams = []
        games = []

        for name in streamer:
            resps.append(self.make_request(URL + name))

        GAME_URL = "https://api.twitch.tv/helix/games?id="
        for i, r in enumerate(resps, 0):
            if r["data"]:
                game_id   = r["data"][0]["game_id"]
                game_resp = self.make_request(GAME_URL + game_id) 
                game_name = game_resp["data"][0]["name"]
                online_streams.append((streamer[i], game_name))
                games.append((game_name))
        return str(games[0])

run = req()
run.get_current_online_streams()

