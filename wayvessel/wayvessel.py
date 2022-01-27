import discord
import pandas as pd
import os
import datetime


class WayVessel:
    def __init__(self, name_1, name_2, normal, goblin_fort, mystic_cave, beast_den, dragon_roost, battlegrounds,
                 underworld, chaos_portal, valley_gods, group_id):
        self.name_1 = name_1
        self.name_2 = name_2
        self.normal = normal
        self.goblin_fort = goblin_fort
        self.mystic_cave = mystic_cave
        self.beast_den = beast_den
        self.dragon_roost = dragon_roost
        self.battlegrounds = battlegrounds
        self.underworld = underworld
        self.chaos_portal = chaos_portal
        self.valley_gods = valley_gods
        self.group_id = group_id

    def listDungeons(self):
        message = "WV: " + self.name_2 + "\n"

        if self.normal != 0:
            message += " <:normal:936020920001257502>- " + str(self.normal)
        if self.goblin_fort != 0:
            message += " <:goblin_fort:936020920210968667>- " + str(self.goblin_fort)
        if self.mystic_cave != 0:
            message += " <:mystic_cave:936020920185806858>- " + str(self.mystic_cave)
        if self.beast_den != 0:
            message += " <:beast_den:936020920257097738>- " + str(self.beast_den)
        if self.dragon_roost != 0:
            message += " <:dragon_roost:936020920152252518>- " + str(self.dragon_roost)
        if self.battlegrounds != 0:
            message += " <:battlegrounds:936020920047378442>- " + str(self.battlegrounds)
        if self.underworld != 0:
            message += " <:underworld:936020920215142420>- " + str(self.underworld)
        if self.chaos_portal != 0:
            message += " <:chaos_portal:936020920303239178>- " + str(self.chaos_portal)
        if self.valley_gods != 0:
            message += " <:valley_gods:936020920064159774>- " + str(self.valley_gods)
        return message


def ListAllEmbed():
    wvembed = discord.Embed()
    df = pd.read_csv('wayvessel/wv_export.csv')
    modTime = os.path.getmtime('wayvessel/wv_export.csv')
    modTime = datetime.datetime.utcfromtimestamp(modTime)

    print(df.to_string())
    print("Export last modified: " + str(modTime))
    for index, row in df.iterrows():
        wv = WayVessel(
            row['name_1'],
            row['name_2'],
            row['normal'],
            row['goblin_fort'],
            row['mystic_cave'],
            row['beast_den'],
            row['dragon_roost'],
            row['battlegrounds'],
            row['underworld'],
            row['chaos_portal'],
            row['valley_gods'],
            row['group_id']
        )
        wvembed.add_field(name=row['name_1'], value=wv.listDungeons() + "\n")
    return wvembed