from multiprocessing import Process
import time
import logging
import threading
import discord
from discord.ext import commands, tasks

import configuration
import database
import sessions
import stats.functions as stats_functions
import stats.text_channels as text_channels_functions

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

def current_guild():
    logging.debug("Guild id: " + str(configuration.GUILD_ID))
    logging.debug("Guilds: " + str(bot.guilds))
    return discord.utils.find(lambda g: g.id == configuration.GUILD_ID, bot.guilds)

def members_str(guild):
    return '\n - '.join([member.name for member in guild.members])

def channels_str(guild):
    text = ''
    for channel in guild.voice_channels:
        text += '\n - '
        text += channel.name
        if len(channel.members) > 0:
            text += '\n   members:'
            for member in channel.members:
                text += '\n    + '
                text += member.name + ' ' + str(member.id)
    return text

def start_updating_sessions():
    sessions.start_updating_sessions(current_guild)


def run():
    # @bot.slash_command(name="z_debug-print-guild-members", guild_ids=[configuration.GUILD_ID])
    # async def debug_print(ctx):
    #     guild = current_guild()
    #     text = f'{bot.user} is connected to the following guild: ' \
    #            + f'{guild.name}(id: {guild.id})\n' \
    #            + f'Guild Members:\n - {members_str(guild)}\n'
    #     await ctx.respond(text)
    #
    # @bot.slash_command(name="z_debug-print-voice-channels", guild_ids=[configuration.GUILD_ID])
    # async def debug_print(ctx):
    #     guild = current_guild()
    #     text = f'Guild Channels:\n - {channels_str(guild)}\n'
    #     await ctx.respond(text)

    @bot.slash_command(name="top-users-day", guild_ids=[configuration.GUILD_ID])
    async def top_users_1(ctx):
        text = stats_functions.get_top_users_days_text(1)
        await ctx.respond(text)

    @bot.slash_command(name="top-users-7-days", guild_ids=[configuration.GUILD_ID])
    async def top_users_7(ctx):
        text = stats_functions.get_top_users_days_text(7)
        await ctx.respond(text)

    @bot.slash_command(name="top-users-30-days", guild_ids=[configuration.GUILD_ID])
    async def top_users_30(ctx):
        text = stats_functions.get_top_users_days_text(30)
        await ctx.respond(text)

    @bot.slash_command(name="top-text-channels-day", guild_ids=[configuration.GUILD_ID])
    async def top_text_channels_1(ctx):
        await ctx.response.defer()
        text = await text_channels_functions.get_top_channels_text(current_guild, 1)
        await ctx.respond(text)

    @bot.slash_command(name="top-text-channels-7-days", guild_ids=[configuration.GUILD_ID])
    async def top_text_channels_7(ctx):
        await ctx.response.defer()
        text = await text_channels_functions.get_top_channels_text(current_guild, 7)
        await ctx.respond(text)

    @bot.slash_command(name="top-text-channels-30-days", guild_ids=[configuration.GUILD_ID])
    async def top_text_channels_7(ctx):
        await ctx.response.defer()
        text = await text_channels_functions.get_top_channels_text(current_guild, 30)
        await ctx.respond(text)

    bot.run(configuration.TOKEN)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(threadName)s %(message)s"
    )
    database.init()
    thread = threading.Thread(target=start_updating_sessions, args=())
    thread.daemon = True
    thread.start()
    run()
