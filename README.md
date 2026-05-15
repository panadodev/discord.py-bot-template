# discord.py Bot Template

A minimal, production-ready Discord bot template using [discord.py](https://discordpy.readthedocs.io/) with slash commands, automatic cog loading, and optional Sentry error tracking.

## Features

- Slash command support via `discord.app_commands`
- Automatic extension loading — drop a file in `cogs/` and it's live
- Environment-based configuration via `.env`
- Optional [Sentry](https://sentry.io/) integration for error tracking
- Docker support

## Project Structure

```
├── cogs/                    # Command cogs (auto-loaded on startup)
│   └── discord_commands.py  # Example cog with /ping and /info
├── .env.example             # Environment variable reference
├── Dockerfile
├── main.py                  # Bot entry point
└── requirements.txt
```

## Getting Started

### 1. Prerequisites

- Python 3.11+
- A bot application from the [Discord Developer Portal](https://discord.com/developers/applications) with the **Message Content** intent enabled

### 2. Configure environment

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `DISCORD_TOKEN` | Yes | Bot token from the Discord Developer Portal |
| `GUILD_ID` | No | Guild ID for instant slash command syncing during development |
| `SENTRY_DSN` | No | Sentry DSN for error tracking |

> **Tip:** Set `GUILD_ID` during development. Guild-scoped syncs are instant; global syncs can take up to an hour.

### 3. Install & run

```bash
pip install -r requirements.txt
python main.py
```

### Running with Docker

```bash
docker build -t discord-bot .
docker run --env-file .env discord-bot
```

## Adding Commands

Create a new file in `cogs/` with a `Cog` class and an async `setup` function:

```python
# cogs/my_commands.py
from discord import Interaction, app_commands
from discord.ext import commands


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
```

The file is picked up automatically at next startup — no changes to `main.py` needed.

## License

See [LICENSE](LICENSE).
