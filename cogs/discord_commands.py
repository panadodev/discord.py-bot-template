import logging

import discord
from discord import Interaction, app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)


class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            f"Pong! Latency: {self.bot.latency * 1000:.2f}ms", ephemeral=True
        )

    @app_commands.command(
        name="info", description="Display information about this bot."
    )
    async def info(self, interaction: Interaction) -> None:
        embed = discord.Embed(
            title="Bot Info",
            description="A discord.py bot built from template.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")
        embed.add_field(name="Guilds", value=str(len(self.bot.guilds)))
        embed.set_footer(text=f"discord.py {discord.__version__}")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DiscordCommands(bot))
