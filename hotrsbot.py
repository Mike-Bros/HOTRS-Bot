import json
import os
import datetime
import discord
import asyncio

import pandas as pd
import yaml
from discord.ext import commands
from wayvessel import wayvessel

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    colors = config['COLORS']
    token = config['APP']['TOKEN']


class MyClient(discord.Client):

    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}'.format(self.user))


class MyBot(commands.Bot):
    async def foo(self):
        return True



bot = MyBot(command_prefix='!')


@bot.event
async def on_ready():
    print('config.yaml: ' + str(config))
    print('config colors: ' + str(colors))
    print("I am running on: " + bot.user.name)
    print("With the ID: " + str(bot.user.id))
    print("Ready when you are!")


@bot.command(help='Lists the dungeons available this week, you pull all or specify the group number')
async def dungeons(ctx, *arg1):
    if arg1 == ():
        await ctx.channel.send("Usage ```!dungeon <group_id> or all```")
    elif arg1.__contains__('all'):
        await ctx.channel.send("This weeks dungeons...")
        wvembed = wayvessel.ListAllEmbed()
        wvembed.color = colors['PRIMARY']
        await ctx.channel.send(embed=wvembed)
    else:
        try:
            int(arg1[0])
            await ctx.channel.send('Group {} has the following dungeons this week...'.format(arg1[0]))
            wvembed = wayvessel.ListEmbed(arg1[0])
            wvembed.color = colors['SECONDARY']
            await ctx.channel.send(embed=wvembed)
        except ValueError:
            await ctx.channel.send('{} is not a valid argument'.format(arg1[0]))


@bot.command(name='reload',
             help='this command will clear msgs in the #dungeon-list channel and update with the most recent dungeons')
async def reloadDungeonsList(ctx):
    if ctx.channel.name == "dungeon-list":
        await ctx.channel.purge()

        df = pd.read_csv('wayvessel/wv_export.csv')
        modTime = os.path.getmtime('wayvessel/wv_export.csv')
        modTime = datetime.datetime.utcfromtimestamp(modTime)

        info = discord.Embed(title="Click here to update spreadsheet",
                             url="https://docs.google.com/spreadsheets/d/1uUdIfWMNmsegoWrZA7Ftd8XK3ipNrIrMmV3wdKl4-W8/edit?usp=sharing",
                             colour=colors['INFO'],
                             description="Dungeon List Refreshed based on export last modified: " + str(modTime)
                                         + "\n Once the spreadsheet is updated, please use ``` !reload ```", )
        await ctx.channel.send(embed=info)
        await ctx.channel.send("***This weeks dungeons...***")
        for index, row in df.iterrows():
            wvembed = wayvessel.ListAllEmbedHelper(row)
            if row['group_id'] % 2 == 0:
                wvembed.color = colors['SECONDARY']
            else:
                wvembed.color = colors['PRIMARY']
            await ctx.channel.send(embed=wvembed)


    else:
        await ctx.channel.send("You can only use this in #dungeon-list")


@bot.command(name='p', help='this command will create a part event for a specified dungeon')
async def partyStart(ctx, dungeon_id, time_utc):
    if len(time_utc) == 4:
        try:
            dungeon_id = int(dungeon_id)
            time_utc = int(time_utc)
            df = pd.read_csv('wayvessel/wv_export.csv')
            if dungeon_id in df['id']:
                await ctx.message.add_reaction('✅')
                partyEmbed = discord.Embed(title="Sample")
                msg = await ctx.channel.send(embed=partyEmbed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')

                await ctx.message.delete()
            else:
                await ctx.channel.send(
                    '{} is not a valid dungeon id, please check #dungeon-list for valid ids'.format(dungeon_id))
        except ValueError:
            print(ValueError.with_traceback())
            await ctx.channel.send('{} and/or {} are not a valid arguments'.format(dungeon_id, time_utc))
    else:
        await ctx.channel.send('{} is not a valid time, please use UTC 24-Hour format, ex: 2pm = 1400'.format(time_utc))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 938469347360382996:
        member = payload.member
        emoji = payload.emoji.name
        if emoji == '✅':
            await bot.get_channel(payload.channel_id).send('Checked by: `' + member.name + '`')
        elif emoji == '❌':
            await bot.get_channel(payload.channel_id).send('Xed by: `' + member.name + '`')


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 938469347360382996:
        guild = await(bot.fetch_guild(payload.guild_id))
        member = await (guild.fetch_member(payload.user_id))
        emoji = payload.emoji.name
        if emoji == '✅':
            await bot.get_channel(payload.channel_id).send('Check removed by: `' + member.name + '`')
        elif emoji == '❌':
            await bot.get_channel(payload.channel_id).send('X removed by: `' + member.name + '`')


bot.run(token)
