#!pip install irc
from irc.bot import SingleServerIRCBot
from requests import get
from lib import cmds

NAME = "EmpathBot"
OWNER = "chatbotowner"

class Bot(SingleServerIRCBot):
    #Getting the channel ID and logging in the account
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = "4chwl18cmbzrd9mvmvyprbea8fnylx"
        self.TOKEN = "omq73dclve4qehac8nfmtfg3jlb7p0"
        self.CHANNEL = f"#{OWNER}"
        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.CHANNEL_ID = resp["users"][0]["_id"]

        #connecting to the channel
        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")
            
        cxn.join(self.CHANNEL)
        self.send_message("Now online.")

    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        if user['name'] != NAME:
            cmds.process(bot, user, message)


    def send_message(self, message):
	    self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
	bot = Bot()
	bot.start()
