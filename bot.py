import websocket
import json
import requests
import threading
import os
import subprocess
from sys import executable, exit
from pokemon import Pokemon
import os.path

# Heavy inspiration taken from https://github.com/QuiteQuiet/PokemonShowdownBot
# In terms of how PS deals with actions/login and how websocket works

# currently can only do one battle at once - TODO: multiple

DEBUG_MESSAGES = True 
DEBUG_SPLIT_MESSAGES=True

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
        self.pokemonCreated = False
        self.roomCreated = False
        self.room = ""
        self.foundinit = False

    def parse_settings(self, filename):
        if not os.path.isfile(filename):
            return

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

    def chat(self, msg):
        self.send(self.room+"|"+msg)

    def createPokemon(self, requestJSON):
        self.pokemon = []
        for i in range(6):
            self.pokemon.append(Pokemon(requestJSON, i))

        for p in self.pokemon:
            p.dump()

        self.pokemonCreated = True


    def splitmessage(self, ws, message):
        if not message:
            return
        if DEBUG_MESSAGES: print(message)
        lines = message.split("\n")
        splitmsgs = map(lambda x: x.split("|"), lines)
        for splitmsg in splitmsgs:
            if DEBUG_SPLIT_MESSAGES: print(splitmsg)
            if len(splitmsg) == 1 :
                if len(splitmsg[0]) > 1 and splitmsg[0][0] == '>':
                    if not self.roomCreated and self.foundinit:
                        print("Created Room!")
                        self.room=splitmsg[0][1:-1] #dropping \n
                        self.roomCreated = True
                        self.foundinit = False
                else:
                    continue
            elif splitmsg[1] == 'challstr':
                self.login(splitmsg[2], splitmsg[3])
            elif splitmsg[1] == 'init':
                self.foundinit = True
            elif splitmsg[1] == 'request':
                if not self.pokemonCreated:
                    self.createPokemon(splitmsg[2])

            elif splitmsg[1] == "win":
                self.pokemonCreated = False
                self.roomCreated = False
                self.room=""
                print("Reset")


    def on_open(self, message):
        print("Opened: ", message);

    def on_error(self, ws, error):
        print("Errored: ", error)

    def on_close(self, message):
        print("Closed: ", message)

    def send(self, message):
        self.ws.send(message)

    def chat_forever(self):
        while True:
            msg = input()
            if self.roomCreated:
                self.chat(msg)

    def threaded_chat_forever(self):
        threading.Thread(target=self.chat_forever, daemon=False).start()

def open_chat_term():
    os.system("gnome-terminal -e 'bash -c \"python3 chat.py; exec bash\"'")
    
if __name__ == "__main__":
    test = Showdown_Bot()
    #open_chat_term()
    test.threaded_chat_forever()
    test.ws.run_forever()
