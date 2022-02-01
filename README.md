# Description
Discord bot that links cpp documentation to user inputted keywords in a Discord server.

All documentation is from [cppreference](https://en.cppreference.com/w/).

# Bot Link
[Click here to add this bot to your server!](https://discord.com/api/oauth2/authorize?client_id=937797956340449351&permissions=275415026688&scope=bot)

# Usage
The bot has 1 command:
- `!cpp [term]`: takes a single argument which is your term you wish to query [cppreference](https://en.cppreference.com/w/).

Example:
```
!cpp fscanf
```
If the command was successful, the bot will reply to the user who sent the command with a mention and an embedded link to the reference url.

# Development
## Setup
Ignore from here on out if you don't plan on messing with the src at all.

You need to set up your app in [Discord's Developer Portal](https://discord.com/developers/applications). 

Once you've done that, your environment variable(s) should be set accordingly in the generated `.env` file
```python3
TOKEN = os.getenv('DISCORD_TOKEN')        # Discord app key for interfacing with their API
```

## Requirements
- Python 3.8 (possibly lower, but it was built with 3.8)
- discord.py
- python-dotenv (or tweak the code for native env variables)
