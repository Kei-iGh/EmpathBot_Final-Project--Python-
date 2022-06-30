import pandas as pd
import regex as re
from datetime import datetime, date
import os
login = "chatbotowner"

#using variable today, so the bot can create files with different names for storing data after each stream 
today = date.today()


#All scraped lines have similar following structure:

#game: Dead by Daylight.
#2021-05-03_22:59:01 — Starting new HTTPS connection (1): api.twitch.tv:443
#2021-05-03_22:59:02 — https://api.twitch.tv:443 "GET /helix/channels?broadcaster_id=153314610 HTTP/1.1" 200 237
#2021-05-03_22:59:02 — :doomtheninja404!doomtheninja404@doomtheninja404.tmi.twitch.tv PRIVMSG #miltontpike1 :MiltonRain our fault 


#Extracting the game name with regex
data1 = []
with open (f"{today}_{login}_chat.log", 'r', encoding='utf-8') as f:
        lines_ = f.read().split(' \n')

        for line_ in lines_:
            game = re.findall('game:(.+)', line_)
            for i in game:
                g = {'game' : i}
                data1.append(g)
df1 = pd.DataFrame().from_records(data1)


#similarly (the same lines from 13-16) extracting the time, username, chnnel name and messages with regex and converting to a dataframe
def get_chat_dataframe(file):
    data = []
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

        for line in lines:
            try:

                time_logged = line.split('—')[0].strip()
                time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                username_message = '—'.join(username_message).strip()

                username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message).groups()

                d = {
                    'dt': time_logged,
                    'channel': channel,
                    'username': username,
                    'message': message
                }

                data.append(d)
            
            except Exception:
                pass

    return pd.DataFrame().from_records(data)
        
    
df = get_chat_dataframe(f'{today}_{login}_chat.log')

new = pd.merge(df, df1, how="outer",left_index=True, right_index=True)

#creating a xlsx file to store the data
new.to_excel(f"{today}_{login}_chat.xlsx")


