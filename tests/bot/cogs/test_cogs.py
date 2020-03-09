"""Test suite for general tests which apply to all cogs."""

import typing as t
import unittest
from collections import defaultdict

from discord.ext import commands

from bot.__main__ import bot as discord_bot


class CommandNameTests(unittest.TestCase):
    """Tests for shadowing command names and aliases."""

    @staticmethod
    def get_qualified_names(command: commands.Command) -> t.List[str]:
        """Return a list of all qualified names, including aliases, for the `command`."""
        names = [f"{command.full_parent_name} {alias}" for alias in command.aliases]
        names.append(command.qualified_name)

        return names

    def test_names_dont_shadow(self):
        """Names and aliases of commands should be unique."""
        all_names = defaultdict(list)
        for cmd in discord_bot.commands:
            func_name = f"{cmd.module}.{cmd.callback.__qualname__}"

            for name in self.get_qualified_names(cmd):
                with self.subTest(cmd=func_name, name=name):
                    if name in all_names:
                        conflicts = ", ".join(all_names.get(name) or "")
                        self.fail(
                            f"Name '{name}' of the command {func_name} conflicts with {conflicts}."
                        )

                all_names[name].append(func_name)
