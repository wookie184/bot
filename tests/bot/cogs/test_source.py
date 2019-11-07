import asyncio
import unittest

import discord

from bot.cogs import source
from tests.helpers import AsyncMock, MockBot, MockContext


class SourceTest(unittest.TestCase):
    """Tests the source cog."""

    def setUp(self) -> None:
        """Sets up fresh objects for each test."""
        self.bot = MockBot()
        self.ctx = MockContext()
        self.cog = source.Source(self.bot)

    def test_default_embed(self) -> None:
        """Tests that the bot returns correct project links when no command is passed."""
        return_value = asyncio.run(
            self.cog.source_command.callback(self.cog, self.ctx)
        )

        self.assertIsNone(return_value)
        self.ctx.send.assert_called_once()

        _, kwargs = self.ctx.send.call_args
        embed = kwargs.pop('embed')

        url = "https://github.com/python-discord"
        self.assertEqual(embed.title, ":guild_update: Python Discord: Source Code")
        self.assertEqual(
            embed.description, (
                f"\u2022 [Site]({url}/site)\n"
                f"\u2022 [Bot]({url}/bot)\n"
                f"\u2022 [SeasonalBot]({url}/seasonalbot)\n"
            )
        )
        self.assertEqual(embed.url, url)
        self.assertEqual(embed.colour, discord.Colour.blurple())

    def test_invalid_command(self) -> None:
        """Tests that the bot returns correct message when the specifiied command is not found."""
        self.cog.get_command_info = AsyncMock()
        self.cog.get_command_info.return_value = None

        return_value = asyncio.run(
            self.cog.source_command.callback(self.cog, self.ctx, cmd_name="supercalifragilistic")
        )

        self.assertIsNone(return_value)
        self.ctx.send.assert_called_once()

        args, _ = self.ctx.send.call_args
        self.assertIn(":x: Command not found.", args)
