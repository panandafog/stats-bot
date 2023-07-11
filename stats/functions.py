import logging

from models import User, Channel, Session, ActiveSession
from stats.models import UserInfo, TopUsers
import utils.messages as messages

def get_top_users_text():
    top_users = _get_top_users()

    return messages.make_top_users_message(top_users)

def _get_top_users():
    users = User.objects()
    users_info = []

    top_users = TopUsers()

    for user in users:
        sessions = Session.objects(user=user)
        active_session = ActiveSession.objects(user=user).first()

        for session in sessions:
            if top_users.start_datetime is None or session.start_time < top_users.start_datetime:
                top_users.start_datetime = session.start_time

        if (not active_session is None) and (top_users.start_datetime is None or active_session.start_time < top_users.start_datetime):
            top_users.start_datetime = active_session.start_time

        user_info = UserInfo.from_user(user, sessions, active_session)
        users_info.append(user_info)

    users_info.sort(key=lambda x: x.total_time, reverse=True)
    top_users.users_info = users_info

    return top_users
