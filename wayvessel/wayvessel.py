import json
import sqlite3
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import discord
import pandas as pd
import os
import datetime
import yaml

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    colors = config['COLORS']
    token = config['APP']['TOKEN']

# declarative base class
Base = declarative_base()
engine = create_engine('sqlite:///' + config['APP']['DBNAME'], echo=True)


class WayVessel(Base):
    dbcon = sqlite3.connect(config['APP']['DBNAME'])

    __tablename__ = 'wayvessel'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    name_1 = Column(String, nullable=False, unique=True)
    name_2 = Column(String, nullable=False, unique=True)
    normal = Column(Integer, nullable=True, default=0)
    goblin_fort = Column(Integer, nullable=True, default=0)
    mystic_cave = Column(Integer, nullable=True, default=0)
    beast_den = Column(Integer, nullable=True, default=0)
    dragon_roost = Column(Integer, nullable=True, default=0)
    battlegrounds = Column(Integer, nullable=True, default=0)
    underworld = Column(Integer, nullable=True, default=0)
    chaos_portal = Column(Integer, nullable=True, default=0)
    valley_gods = Column(Integer, nullable=True, default=0)

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


Base.metadata.create_all(engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(WayVessel).all()
    return result


def getDungeon(dungeon_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(WayVessel).where(id=dungeon_id)
    return result


def clearWVTable(conn):
    sql = 'DELETE FROM wayvessel'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def saveDungeonsFromExport():
    df = pd.read_csv('wayvessel/wv_export.csv')
    Session = sessionmaker(bind=engine)
    session = Session()
    for index, row in df.iterrows():
        get_or_create(session, WayVessel,
                      group_id=row['group_id'],
                      name_1=row['name_1'],
                      name_2=row['name_2'],
                      normal=row['normal'],
                      goblin_fort=row['goblin_fort'],
                      mystic_cave=row['mystic_cave'],
                      beast_den=row['beast_den'],
                      dragon_roost=row['dragon_roost'],
                      battlegrounds=row['battlegrounds'],
                      underworld=row['underworld'],
                      chaos_portal=row['chaos_portal'],
                      valley_gods=row['valley_gods']
                      )

    return True


def allEmbed():
    wayvessels = getAll()
    wvembed = discord.Embed()
    for wv in wayvessels:
        wvembed.add_field(name=str(wv.name_1) + " - Group:" + str(wv.group_id),
                          value=wv.listDungeons() + "\n")

    return wvembed


def groupEmbed(group_id):
    wvembed = discord.Embed()
    wayvessels = getAll()
    for wv in wayvessels:
        print(wv.group_id)
        if wv.group_id == int(group_id):
            wvembed.add_field(name=wv.name_1, value=wv.listDungeons() + "\n")

    return wvembed


def singleEmbed(wayvessel):
    wvembed = discord.Embed()

    wvembed.add_field(name=str(wayvessel.name_1) + " - Group:" + str(wayvessel.group_id),
                      value=wayvessel.listDungeons() + "\n")
    wvembed.add_field(name="Start Command", value="``` !party " + str(wayvessel.id) + "```")
    return wvembed
