import logging

import datetime
import discord.guild
import utils.messages as messages

from stats.models import TopChannels, ChannelMessagesCountInfo


async def get_top_channels_text(current_guild_getter, days, limit=10):
    top_channels = await _get_top_channels_info(
        current_guild_getter,
        datetime.datetime.utcnow() - datetime.timedelta(days=days),
        limit
    )
    return messages.make_top_channels_message(top_channels)


async def _get_top_channels_info(current_guild_getter, after: datetime.datetime, limit):
    guild = current_guild_getter()
    text_channels = _get_all_text_channels(guild)
    channels_info = []

    for channel in text_channels:
        messages_count = await _get_messages_count(channel, after)
        if messages_count > 0:
            info = ChannelMessagesCountInfo(channel, messages_count)
            channels_info.append(info)

    channels_info.sort(key=lambda x: x.messages_count, reverse=True)
    channels_info = channels_info[:limit]
    return TopChannels(channels_info, after)


def _get_all_text_channels(guild: discord.guild):
    text_channel_list = []
    for channel in guild.channels:
        if str(channel.type) == 'text':
            text_channel_list.append(channel)
    return text_channel_list


async def _get_messages_count(channel: discord.channel, after: datetime.datetime):
    messages = await channel.history(after=after).flatten()
    return len(messages)
