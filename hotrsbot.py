import random
from distutils.log import info

import discord
import yaml
from discord.ext import commands

from wayvessel import wayvessel

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    colors = config['COLORS']
    token = config['APP']['TOKEN']
    print('config.yaml: ' + str(config))
    print('config colors: ' + str(colors))


class MyClient(discord.Client):

    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}'.format(self.user))


class MyContext(commands.Context):
    async def tick(self, value):
        # reacts to the message with an emoji
        # depending on whether value is True or False
        # if its True, it'll add a green check mark
        # otherwise, it'll add a red cross mark
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            # this will react to the command author's message
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            # sometimes errors occur during this, for example
            # maybe you dont have permission to do that
            # we dont mind, so we can just ignore them
            pass


class MyBot(commands.Bot):
    async def get_context(self, message, *, cls=MyContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        return await super().get_context(message, cls=cls)


bot = MyBot(command_prefix='!')


@bot.event
async def on_ready():
    print("Ready when you are")
    print("I am running on: " + bot.user.name)
    print("With the ID: " + str(bot.user.id))


@bot.command()
async def guess(ctx, number: int):
    """ Guess a random number from 1 to 6. """
    # explained in a previous example, this gives you
    # a random number from 1-6
    value = 4
    # with your new helper function, you can add a
    # green check mark if the guess was correct,
    # or a red cross mark if it wasnt
    await ctx.tick(number == value)


@bot.command()
async def hello(ctx):
    await ctx.channel.send('Hello World!')


@bot.command('list')
async def ListAllEmbed(ctx):
    wvembed = wayvessel.ListAllEmbed()
    await ctx.channel.send("This weeks dungeons")
    wvembed.color = colors['PRIMARY']
    await ctx.channel.send(embed=wvembed)


@bot.command()
async def dungeons(ctx, *arg1):
    if arg1 == ():
        await ctx.channel.send("Usage ```!dungeon <group_id> or all```")
    elif arg1.__contains__('all'):
        wvembed = wayvessel.ListAllEmbed()
        await ctx.channel.send("This weeks dungeons...")
        wvembed.color = colors['PRIMARY']
        await ctx.channel.send(embed=wvembed)
    else:
        try:
            int(arg1[0])
            await ctx.channel.send('Group {} has the following dungeons this week...'.format(arg1[0]))
        except ValueError:
            await ctx.channel.send('{} is not a valid argument'.format(arg1[0]))


bot.run(token)
