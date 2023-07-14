import logging
import datetime
import copy

from models import User, Channel, Session, ActiveSession
from stats.models import UserInfo, TopUsers
import utils.messages as messages


def get_top_users_days_text(days):
    top_users = _get_top_users(datetime.datetime.utcnow() - datetime.timedelta(days=days))

    return messages.make_top_users_message(top_users)


def _get_top_users_text(start_datetime: datetime):
    top_users = _get_top_users(start_datetime)

    return messages.make_top_users_message(top_users)


def _get_top_users(start_datetime: datetime):
    users = User.objects()
    users_info = []

    top_users = TopUsers()
    top_users.start_datetime = start_datetime

    for user in users:
        sessions = Session.objects(user=user)
        active_sessions = ActiveSession.objects(user=user)
        all_sessions = list(copy.copy(sessions)) + list(copy.copy(active_sessions))

        for session in all_sessions:
            start_time = None
            end_time = None
            try:
                end_time = session.end_time
            except:
                pass
            if session.start_time < start_datetime:
                if (end_time is not None) and (end_time > start_datetime):
                    start_time = start_datetime
            else:
                start_time = session.start_time

            if (start_time is not None) and (top_users.first_entry is None or start_time < top_users.first_entry):
                top_users.first_entry = start_time

        user_info = UserInfo.from_user(user, sessions, active_sessions.first(), start_datetime)
        users_info.append(user_info)

    users_info.sort(key=lambda x: x.total_time, reverse=True)
    top_users.users_info = users_info

    return top_users
