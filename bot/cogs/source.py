import inspect
import logging
from typing import Optional

from discord import Colour, Embed
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

from bot import constants

logger = logging.getLogger(__name__)


class Source(Cog):
    """Commands for getting the source code for commands in our bot."""

    ORG_URL = "https://github.com/python-discord"
    BASE_URL = "https://github.com/python-discord/bot/tree/master/"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="source", aliases=("src", "getsource",))
    async def source_command(self, ctx: Context, *, cmd_name: Optional[str] = None) -> None:
        """Gets the source for a server command."""
        # No requested command, send project url
        if cmd_name is None:
            embed = Embed(
                title=f":guild_update: Python Discord: Source Code",
                description=(
                    f"\u2022 [Site]({self.ORG_URL}/site)\n"
                    f"\u2022 [Bot]({self.ORG_URL}/bot)\n"
                    f"\u2022 [SeasonalBot]({self.ORG_URL}/seasonalbot)\n"
                ),
                url=self.ORG_URL
            )
            await ctx.send(embed=embed)
            return

        # Allow `otn.add` as a valid input together with `otn add`
        cmd_name = cmd_name.replace(".", " ")

        data = await self.get_command_info(cmd_name)
        if not data:
            await ctx.send(":x: Command not found.")
            return

        embed = self.build_source_embed(**data)
        await ctx.send(embed=embed)

    async def get_command_info(self, cmd_name: str) -> dict:
        """Gets the information of a command."""
        command = self.bot.get_command(cmd_name)
        if command is None:
            return {}

        src = command.callback

        _, cog_lineno = inspect.getsourcelines(command.cog.__class__)
        cog_name = command.cog_name
        module_path = f"{src.__module__.replace('.', '/')}.py"

        lines, start_lineno = inspect.getsourcelines(src)
        end_lineno = start_lineno + len(lines) - 1

        data = {
            "command": command, "module_path": module_path,
            "cog_lineno": cog_lineno, "cog_name": cog_name,
            "lines": lines, "start": start_lineno, "end": end_lineno
        }

        return data

    @staticmethod
    def build_source_embed(
        cog_name: str, cog_lineno: int, command: str, module_path: str, start: int, end: int, **kwargs
    ) -> Embed:
        """Builds a embed representation of a command."""
        command_url = f"{Source.BASE_URL}{module_path}#L{start}-L{end}"
        cog_url = f"{Source.BASE_URL}{module_path}#L{cog_lineno}"

        path_segments = module_path.split("/")
        module_desc = "/".join(
            f"[{segment}]({Source.BASE_URL}{'/'.join(path_segments[:idx])})"
            for idx, segment in enumerate(path_segments, start=1)
        )

        embed = Embed(
            title=f":guild_update: View Source Code",
            description=(
                f"```{constants.Bot.prefix}{command}```\n"
                f"**Cog:** [{cog_name}]({cog_url})\n"
                f"**Module:** {module_desc}\n"
            ),
            colour=Colour.blurple(),
            url=command_url,
        )
        embed.set_footer(
            text=f"{end - start + 1} lines total, (L{start}:L{end})",
        )
        return embed


def setup(bot: Bot) -> None:
    """Loads the Source Cog."""
    bot.add_cog(Source(bot))
    logger.info("Source Cog loaded.")
