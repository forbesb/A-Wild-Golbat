import websocket

class Showdown_Bot:
    def __init__(self):
        self.settingsfile = "settings.txt"
        self.parse_settings(self.settingsfile)
        self.ws = websocket.WebSocketApp(self.url)


    def parse_settings(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                splitline = line.split("=")
                if splitline[0] == "username":
                    self.user=splitline[1][1:-1] #dropping quotations
                elif splitline[0] == "password":
                    self.password=splitline[1][1:-1]
                elif splitline[0] == "url":
                    self.url=splitline[1][1:-1]

    def splitmessage(self, ws, message):
        if not message:
            return
        print(message)


test = Showdown_Bot()
#test.ws.run_forever()