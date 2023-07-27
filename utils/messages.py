import utils.date_format as date_format

from stats.models import TopUsers, TopChannels


def make_top_users_message(top_users: TopUsers):
    start_str = top_users.start_datetime.strftime("%d/%m/%Y, %H:%M")
    first_entry_str = top_users.first_entry.strftime("%d/%m/%Y, %H:%M")

    text = f'Total time spent in voice chats since {start_str}\n'

    if start_str != first_entry_str:
        text += f'(first entry {first_entry_str})\n'

    for user_info in top_users.users_info:
        status = ' :headphones:' if user_info.is_active else ''
        text += f'- **{user_info.user.name}**{status}: {date_format.strfdelta(user_info.total_time)} '
        text += f'*/ favourite channel:* <#{user_info.top_channel.discord_id}>\n'

    return text


def make_top_channels_message(top_channels: TopChannels):
    start_str = top_channels.start_datetime.strftime("%d/%m/%Y, %H:%M")
    text = f'Messages count since {start_str}\n'

    for channel_info in top_channels.channels_info:
        text += f'- <#{channel_info.channel.id}>: {channel_info.messages_count}\n'

    if len(top_channels.channels_info) < 1:
        text += '  messages not found 😢'

    return text
