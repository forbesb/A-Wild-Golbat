import json


class Pokemon:
    def __init__(self, jsontext, index):
        data = json.loads(jsontext)
        this = data['side']['pokemon'][index]
        stats = this['stats']
        self.name = this['ident']
        self.currentHP=int(this['condition'].split("/")[0])
        self.totalHP = int(this['condition'].split("/")[1])
        self.atk = int(stats['atk'])
        self.df = int(stats['def'])
        self.spa = int(stats['spa'])
        self.spd = int(stats['spd'])
        self.spe = int(stats['spe'])
        #todo moves

    def dump(self):
        print(self.name)
        print(self.currentHP, "/", self.totalHP)
        print("atk: {}, def: {}, spa: {}, spd: {}, spe: {}".format(self.atk, self.df, self.spa, self.spd, self.spe))


