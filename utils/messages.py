import utils.date_format as date_format

from stats.models import TopUsers


def make_top_users_message(top_users: TopUsers):
    start_str = top_users.start_datetime.strftime("%d/%m/%Y, %H:%M")
    first_entry_str = top_users.first_entry.strftime("%d/%m/%Y, %H:%M")

    text = f'Total time spent in voice chats since {start_str}\n'

    if start_str != first_entry_str:
        text += f'(first entry {first_entry_str})\n'

    for user_info in top_users.users_info:
        status = '💡' if user_info.is_active else ''
        text += f'- {user_info.user.name}{status}: {date_format.strfdelta(user_info.total_time)}\n'

    return text