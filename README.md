# DiscordBotSpells

A Discord bot for fetching and displaying D&D 5e spell descriptions, including homebrew spells, and tracking initiative for combat.

## Features

- Responds to commands starting with `!` followed by a spell name.
- Looks up spells from a local homebrew dictionary (`homebrew.blairs`).
- If not found locally, fetches spell descriptions from [dnd5e.wikidot.com](http://dnd5e.wikidot.com).
- Formats and splits long spell descriptions to fit Discord message limits.
- **Initiative Tracker**: Add, remove, swap, and display initiative order for combat.

## Requirements

- Python 3.8+
- [discord](https://github.com/Rapptz/discord.py)
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup

1. **Clone this repository** and navigate to the project folder.

2. **Install dependencies:**
   ```
   pip install discord requests python-dotenv
   ```

3. **Create a `.env` file** in the project directory with your Discord bot token:
   ```
   TOKEN=your_discord_bot_token_here
   ```

4. **Add your homebrew spells** to `homebrew.py` as a dictionary named `blairs`.

## Usage

Run the bot with:
```
python main.py
```

Invite your bot to your Discord server and use commands like:
```
!fireball
!cure wounds
```
The bot will reply with the spell description.

**Ignore apostrophes; spaces can be kept or replaced with dashes.**

### Initiative Tracker Commands

- `!init <number>`  
  Start a new initiative tracker for `<number>` participants. The bot will collect the next `<number>` valid initiative entries from the channel (ignoring lines starting with `!`).

- `!add <name>: <initiative_value>`  
  Add or update a participant with the given name and initiative value.

- `!remove <name>` or `!rm <name>`  
  Remove a participant by name.

- `!swap <name1> | <name2>` or `!switch <name1> | <name2>`  
  Swap the name placements of two participants.

After each change, the bot will print the current initiative order.

---
