# Placeholder

Discord bot for playing Youtube music videos on voice channel.

## Requirements

- Docker

## Discord Developer Portal Setup

### Token

Get the bot API Token on the Bot of [Discord Developers Applications](https://discord.com/developers/applications/)
And export as an environment variable API_TOKEN.

### Intents

![Activate the intents](https://discordpy.readthedocs.io/en/stable/_images/discord_privileged_intents.png)

### Invite the bot to a server

Get the bot Application ID on the General Information tab of [Discord Developers Applications](https://discord.com/developers/applications/)

On the browser:

`https://discord.com/oauth2/authorize?scope=bot&permissions=0&client_id=$APPLICATION_ID`


## Running on Docker

``make run``
