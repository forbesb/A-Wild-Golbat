import websocket
import json
import requests

# Heavy inspiration taken from https://github.com/QuiteQuiet/PokemonShowdownBot
# In terms of how PS deals with actions/login and how websocket works

class Showdown_Bot:
    def __init__(self):
        self.settingsfile = "settings.txt"
        self.url = "ws://sim.smogon.com:8000/showdown/websocket"
        self.actionurl = "http://play.pokemonshowdown.com/action.php"
        self.parse_settings(self.settingsfile)
        self.ws = websocket.WebSocketApp(self.url, on_close=self.on_close,
                                         on_message=self.splitmessage,
                                         on_error=self.on_error)
        self.ws.on_open = self.on_open

    def parse_settings(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                splitline = line.split("=")
                if splitline[0] == "username":
                    self.user=splitline[1][1:-2] #dropping quotations
                elif splitline[0] == "password":
                    self.password=splitline[1][1:-2]
                elif splitline[0] == "url":
                    self.url=splitline[1][1:-2]

    def login(self, challkey, challstr):
        data = {
            'act' : 'login',
            'name' : self.user,
            'pass' : self.password,
            'challengekeyid' : challkey,
            'challenge' : challstr
        }

        req = requests.post(self.actionurl, data=data)
        assertion = json.loads(req.text[1:])['assertion']

        if not assertion:
            return False

        self.send(('|/trn '+self.user+',0,'+str(assertion)).encode('utf-8'))
        return True


    def splitmessage(self, ws, message):
        if not message:
            return
        print(message)
        splitmsg = message.split("|")
        if (splitmsg[1] == 'challstr'):
            self.login(splitmsg[2], splitmsg[3])

    def on_open(self, message):
        print("Opened: ", message);

    def on_error(self, ws, error):
        print("Errored: ", error)

    def on_close(self, message):
        print("Closed: ", message)

    def send(self, message):
        self.ws.send(message)

test = Showdown_Bot()
test.ws.run_forever()