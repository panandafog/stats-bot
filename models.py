from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField
import discord.member, discord.channel

class User(Document):
    discord_id = IntField(required=True, unique=True)
    nick = StringField(max_length=50)
    name = StringField(max_length=50)

    def update_with_discord_member(self, member: discord.member):
        self.nick = member.nick
        self.name = member.name
    @staticmethod
    def from_discord_member(member: discord.member):
        user = User.objects(discord_id=member.id).first()
        if user is None:
            user = User()
            user.discord_id = member.id

        user.update_with_discord_member(member)
        return user

class Channel(Document):
    discord_id = IntField(required=True, unique=True)
    name = StringField(max_length=50)

    def update_with_discord_channel(self, channel: discord.channel):
        self.name = channel.name

    @staticmethod
    def from_discord_channel(discord_channel: discord.channel):
        channel = Channel.objects(discord_id=discord_channel.id).first()
        if channel is None:
            channel = Channel()
            channel.discord_id = discord_channel.id

        channel.update_with_discord_channel(discord_channel)
        return channel

class ActiveSession(Document):
    user = ReferenceField(User)
    channel = ReferenceField(Channel)
    start_time = DateTimeField()

class Session(Document):
    user = ReferenceField(User)
    channel = ReferenceField(Channel)
    start_time = DateTimeField()
    end_time = DateTimeField()

    @staticmethod
    def from_active_session(active_session: ActiveSession, end_time):
        session = Session(
            user=active_session.user,
            channel=active_session.channel,
            start_time=active_session.start_time,
            end_time=end_time
        )
        return session
