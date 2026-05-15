import asyncio
import logging
import os
import sys

import discord
import sentry_sdk
from discord.ext import commands
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import EventHandler

load_dotenv()

# Sentry setup — only initializes when SENTRY_DSN is provided
_sentry_dsn = os.getenv("SENTRY_DSN")
if _sentry_dsn:
    sentry_sdk.init(
        dsn=_sentry_dsn,
        send_default_pii=True,
        traces_sample_rate=1.0,
    )

_sentry_handler = EventHandler(level=logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        _sentry_handler,
    ],
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def load_extensions() -> None:
    """Automatically load all cogs from the ./cogs directory."""
    cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
    for filename in sorted(os.listdir(cogs_dir)):
        if filename.endswith(".py") and not filename.startswith("_"):
            ext = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(ext)
                logger.info(f"Loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Failed to load extension {ext}: {e}", exc_info=True)


@bot.event
async def on_ready() -> None:
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    try:
        # Always sync global commands (no guild decorator) globally
        global_synced = await bot.tree.sync()
        logger.info(f"Synced {len(global_synced)} global command(s)")

        # Sync guild-specific commands (decorated with @app_commands.guilds) to that guild
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            guild_synced = await bot.tree.sync(guild=guild)
            logger.info(
                f"Synced {len(guild_synced)} guild command(s) to guild {guild_id}"
            )
    except Exception as e:
        logger.error(f"Failed to sync application commands: {e}", exc_info=True)


async def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN is not set. Exiting.")
        return

    async with bot:
        await load_extensions()
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
