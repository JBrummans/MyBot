# MyBot

A simple Discord bot for personal use.

## Why make a bot?

This bot is limited in scope by design. While most bots are aimed at running on a Server (or many Servers) and interacting with many people, this bot is intended to only communicate to the person running the bot with direct messages.

For now the bot is very basic with only a few functions. But it can be used as a template and easily expanded to suit your own needs.

## How to run the bot?

 - Download or clone the repo to your host (Currently only tested on Ubuntu 18.04)
 - Install the requirements by running `pip3 install -r requirements.txt`
 - Create a [Discord bot application](https://discord.com/developers/applications)
 - Once created, create a `.env` file in the folder containing `MyBot.py`
 - Update the `TOKEN` and `OWNER_ID` values with the bots token and your own ID.
    - Update prefix if desired
 - Run the bot using `python3 MyBot.py`

The bot will send a private message to you if it successfully started.

## Contributing

Open an issue or create a pull request!