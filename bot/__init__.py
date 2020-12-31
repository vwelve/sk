from typing import List
from discord.ext import commands
from .models import bind_database
import discord
import yaml
import os

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=0&scope=bot'
DEFAULT_PREFIX = "+"


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_extensions()

        self.prefixes = {}

    def load_extensions(self):
        file_names = [f[:-3] for f in os.listdir('./bot/cogs') if f.endswith('.py')]

        for file_name in file_names:
            self.load_extension(f'cogs.{file_name}')

    @staticmethod
    def get_postgres_login():
        with open("config.yaml") as f:
            postgres_login = yaml.load(f, Loader=yaml.FullLoader)["postgres_login"]

        return postgres_login

    async def on_ready(self):
        await bind_database(self.get_postgres_login())

        print(
            f"""Logged in as {self.user}...
With {len(self.users)} users in {len(self.guilds)} servers
Invite Link: {INVITE_LINK.format(self.user.id)}
            """
        )


def get_prefix(bot: Bot, msg: discord.Message) -> List[str]:
    prefix = bot.prefixes.get(msg.guild.id, DEFAULT_PREFIX)

    return commands.when_mentioned_or(prefix)(bot, msg)


bot = Bot(command_prefix=get_prefix)
