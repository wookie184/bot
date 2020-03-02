import logging

from discord.ext.commands import Cog

from bot.bot import Bot

log = logging.getLogger(__name__)


class AutoConfig(Cog):
    """Sync development servers with the production server."""


def setup(bot: Bot) -> None:
    """Load the AutoConfig cog."""
    bot.add_cog(AutoConfig(bot))
