import unittest
from unittest.mock import MagicMock
import discord
from discord.ext import commands
from cogs.louvre import louvre

class TestLouvre(unittest.TestCase):
    def setUp(self):
        # Create a mock intents instance
        intents = discord.Intents.default()

        # Create a mock bot instance
        self.bot = commands.Bot(command_prefix='!', intents=intents)

        # Create a Louvre instance
        self.louvre = louvre(self.bot)

    async def test_fetch_random_message_with_attachments(self):
        # Create a mock channel
        channel = MagicMock(spec=discord.TextChannel)
        self.bot.get_channel.return_value = channel

        # Create mock messages with attachments
        attachments = [MagicMock(spec=discord.Attachment) for _ in range(5)]
        messages = [MagicMock(spec=discord.Message, attachments=[attachment]) for attachment in attachments]

        # Patch the channel.history() coroutine to return the mock messages
        channel.history.return_value = messages

        # Call the fetch_random_message() method
        random_message = await self.louvre.fetch_random_message()

        # Assert that the returned message is in the list of messages
        self.assertIn(random_message, messages)

    async def test_fetch_random_message_without_attachments(self):
        # Create a mock channel
        channel = MagicMock(spec=discord.TextChannel)
        self.bot.get_channel.return_value = channel

        # Create mock messages without attachments
        messages = [MagicMock(spec=discord.Message, attachments=[]) for _ in range(5)]

        # Patch the channel.history() coroutine to return the mock messages
        channel.history.return_value = messages

        # Call the fetch_random_message() method
        random_message = await self.louvre.fetch_random_message()

        # Assert that the returned message is None
        self.assertIsNone(random_message)

if __name__ == '__main__':
    unittest.main()
