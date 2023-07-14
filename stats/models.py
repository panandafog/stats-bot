import datetime

from models import User, Session, ActiveSession, Channel


def _calculate_channel_time(channels_time, session, delta):
    channel_time = channels_time.get(session.channel.discord_id)
    if channel_time is None:
        channels_time[session.channel.discord_id] = {
            'channel': session.channel,
            'time': delta
        }
    else:
        spent_time = channel_time['time']
        if spent_time is None: spent_time = 0

        channel_time['time'] = spent_time + delta

class UserInfo:
    user = None
    total_time = None
    top_channel = None
    is_active = False

    @staticmethod
    def from_user(user: User, sessions: [Session], active_session: ActiveSession, start_datetime: datetime):
        user_info = UserInfo()
        user_info.user = user
        user_info.total_time = datetime.timedelta()

        channels_time = {}

        for session in sessions:
            delta = datetime.timedelta()
            if session.end_time > start_datetime:
                if session.start_time > start_datetime:
                    delta = session.end_time - session.start_time
                else:
                    delta = session.end_time - start_datetime
            user_info.total_time += delta

            _calculate_channel_time(channels_time, session, delta)

        if active_session is not None:
            user_info.is_active = True

            delta = datetime.timedelta()
            if datetime.datetime.utcnow() > start_datetime:
                if active_session.start_time > start_datetime:
                    delta = datetime.datetime.utcnow() - active_session.start_time
                else:
                    delta = datetime.datetime.utcnow() - start_datetime
            user_info.total_time += delta

            _calculate_channel_time(channels_time, active_session, delta)

        channels_time_list = list(channels_time.values())
        channels_time_list.sort(key=lambda x: x['time'], reverse=True)
        user_info.top_channel = channels_time_list[0]['channel']
        return user_info


class TopUsers:
    users_info = []
    start_datetime = None
    first_entry = None
