import time
import datetime
import discord.member
import logging

from models import User, Channel, Session, ActiveSession
import configuration

def start_updating_sessions(current_guild_getter):
    logging.debug("Start updating sessions")
    logging.debug("guild: " + str(current_guild_getter()))
    while True:
        try:
            update_sessions(current_guild_getter)
        except Exception as e:
            print(e)
        time.sleep(configuration.CHANNELS_STATS_UPDATE_INTERVAL_S)

def update_sessions(current_guild_getter):
    logging.debug("Updating sessions")
    current_guild = current_guild_getter()
    members = []

    if current_guild is not None:
        for channel in current_guild.voice_channels:
            for member in channel.members:
                members.append((channel, member))

        save_active_sessions(members)
        check_ended_sessions(members)

def save_active_sessions(members: [(discord.channel, discord.member)]):
    for channel, member in members:
        db_user = User.from_discord_member(member)
        db_channel = Channel.from_discord_channel(channel)

        db_user.save()
        db_channel.save()

        active_session = ActiveSession.objects(user=db_user, channel=db_channel).first()
        if active_session is None:
            active_session = ActiveSession(user=db_user, channel=db_channel, start_time=datetime.datetime.utcnow)
            logging.debug("Saving new active session:")
            logging.debug(active_session)
            active_session.save()

def check_ended_sessions(members: [(discord.channel, discord.member)]):
    active_sessions = ActiveSession.objects()
    for active_session in active_sessions:
        session_is_ended = True
        for channel, member in members:
            if member.id == active_session.user.discord_id and channel.id == active_session.channel.discord_id:
                #If there is no such user in channel, then stop active session
                session_is_ended = False
                break
        if session_is_ended:
            logging.debug("Active session ended:")
            logging.debug(active_session)
            end_session(active_session)

def end_session(active_session: ActiveSession):
    logging.debug("Ending session")
    session = Session.from_active_session(active_session, datetime.datetime.utcnow)
    active_session.delete()
    session.save()
