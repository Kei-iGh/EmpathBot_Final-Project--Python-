from datetime import date
import logging
import time
import socket
import requests
import json
import os
from emoji import demojize #if not installed, pip install emoji
today = date.today()

#connecting to the twitch server, the time.sleep(0.1) is needed to not get error in case one of the operations gets completed too fast. 
#we need to run the lines in a strict order to connect successfully
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'empathbot'
token = 'oauth:omq73dclve4qehac8nfmtfg3jlb7p0' #tokens are generated after creating an application through twitch/developers web page
login = "chatbotowner"
channel = f'#{login}'

time.sleep(0.1)

sock = socket.socket()

time.sleep(0.1)

sock.connect((server, port))

time.sleep(0.1)

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

time.sleep(0.1)

resp = sock.recv(2048).decode('utf-8')
today = date.today()

time.sleep(0.1)

#creating a general format, so we have an organised final outcome that would look like this:
#game: {name of the game}.
#{date} — Starting new HTTPS connection (1): api.twitch.tv:443
#{date} — https://api.twitch.tv:443 "GET /helix/{id or name}   #in each of those lines we request one kind of data, depending on what parameter we use
#{date} — :{username}!{username}@{username}.tmi.twitch.tv PRIVMSG #{channel name} :{message}
#{date} — Starting new HTTPS connection (1): api.twitch.tv:443
#{date} — https://api.twitch.tv:443 "GET /helix/{id or name}
#...

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s — %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', handlers=[logging.FileHandler(f'{today}_{login}_chat.log', encoding='utf-8')])

time.sleep(0.1)

logging.info(resp)

time.sleep(0.1)

#after connecting the bot to the channel, we need to send rquests using the Twitch API, to get the information from the channel
token = "y7lsc52g72syzlsk4ei4jzqetwexza"
BASE_URL = "https://api.twitch.tv/helix/"
CLIENT_ID = "4chwl18cmbzrd9mvmvyprbea8fnylx"
CLIENT_SECRET = "6wprijwvszl27hts4jjzlyzml6gbmm"
def get_access_token():
    x = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")
    return json.loads(x.text)["access_token"]

HEADERS = {"Client-ID": CLIENT_ID, 'Authorization': f'Bearer {get_access_token()}',"Accept": "application/vnd.v5+json"}
INDENT = 2

def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers = HEADERS)
    return response

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json, indent = INDENT)
    return print_response

def get_user_streams_query(user_login):
    return "streams?user_login={0}".format(user_login)

def get_user_query(user_login):
    return "users?login={0}".format(user_login)

def get_user_broadcast_query(user_id):
    return "channels?broadcaster_id={0}".format(user_id)

def check_if_online(user_login): #returns "live" if online, "" if not
    try:

        link = "streams?user_login={0}".format(user_login)
        res = get_response(link).json()
        return res["data"][0]["type"]

    except IndexError:
        import into_df
        time.sleep(5)
        os.system('python bot.py')



#getting the id of the channel (used for requesting the name of the game)
query = get_user_streams_query(login)
response = get_response(query)
print_response(response)
data = response.json()
idofuser =("" + data["data"][0]["user_id"])



#storing all the information(messages, dates, usernames, channel names and game names) inside a file "chat.log" mentioned in line 48

while True:
    try:
        if check_if_online(login) == "live":

            query2 = get_user_broadcast_query(idofuser)
            response2 = get_response(query2)
            print_response(response2)
            data2 = response2.json()
            nameofgame = ("" + data2["data"][0]["game_name"])

            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
    
            elif len(resp) > 0:
                logging.info(f"{demojize(resp)}game: {nameofgame}.")

    except IndexError:
        import into_df
        time.sleep(5)
        os.system('python bot.py')


