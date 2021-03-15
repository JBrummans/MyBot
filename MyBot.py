#!/usr/bin/python3

import discord
from discord.ext import tasks, commands
import json
import psutil
import time
import os
from dotenv import load_dotenv
from discord.ext.commands import CommandNotFound
import subprocess
from requests import get
from pretty_help import PrettyHelp
import aiocron
import urllib.request
import requests

load_dotenv(dotenv_path=".env")

with open('commands.json') as command_json:
  command_list = json.load(command_json)
  # print(command_list)

bot = commands.Bot(
    command_prefix=os.getenv("PREFIX"),
    owner_id=int(os.getenv("OWNER_ID")),
    case_insensitive=True,
    help_command=PrettyHelp()
)
owner_id = bot.owner_id

""" Owner Check """
async def cog_check(self, ctx):
    # Making sure author of these commands is the bot owner
    return await ctx.bot.is_owner(ctx.author)

@bot.event
async def on_ready():
  # print('MyBot has logged with username: {0.user}'.format(bot))
  embed=discord.Embed(
    title = "MyBot is Online!", 
    description = "MyBot has successfully started", 
    color = discord.Color.green()
  )
  
  user = await bot.fetch_user(owner_id)
  await user.send(embed=embed)

""" Error Check """
async def cog_command_error(ctx, error):
  # Handling any errors within commands
  print(ctx.command.qualified_name)
  embed = discord.Embed(
      title=f"Error in { ctx.command.qualified_name }",
      colour=discord.Color.red(),
      description=dedent(f"""
          { error }
          Use `{ self.bot.command_prefix }help { ctx.command.qualified_name }` for help with the command.
          """)
  )
  return await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
  # Handling any errors when calling a command
  # if isinstance(error, CommandNotFound):
  embed=discord.Embed(
    title = "Oh snap! An error occured", 
    description = "The error was: " + str(error), 
    color = discord.Color.red()
  )
  return await ctx.send(embed=embed)

@bot.command(name='shell', description="Run Shell commands from JSON")
async def run_shell(ctx, message):
  for command, value in command_list.items():
    if str(command) == message:
      output = subprocess.getoutput(value)
      embed=discord.Embed(
        title = "Command Run: '" + command + "'", 
        description = output, 
        color = discord.Color.green()
      )
      return await ctx.send(embed=embed)

  embed=discord.Embed(
    title = "No Shell command found", 
    description = "Did not match " + command + ". Commands include: " + str(command_list), 
    color = discord.Color.red()
  )
  return await ctx.send(embed=embed)


@bot.command(name='test', description="Test DM command")
async def dm_test(ctx):
  user = await bot.fetch_user(owner_id)
  await user.send("Your message here")

@bot.command(name='myip', description="Returns public IP")
async def my_ip(ctx):
  ip = get('https://api.ipify.org').text
  embed=discord.Embed(
    title = "Public IP", 
    description = "IP: " + ip, 
    color = discord.Color.green()
  )
  return await ctx.send(embed=embed)

@bot.command(name='status', description="Host Status command")
async def systemstatus(ctx):
  if int(ctx.author.id) == int(owner_id):
    info={
      'ram':psutil.virtual_memory().percent,
      'cpu':psutil.cpu_percent(),
      'uptime':time.time() - psutil.boot_time(),
      'disk_usage':psutil.disk_usage("/").free
    } 
  embed=discord.Embed(
    title = "System Status", 
    description = "Bot Host System Status", 
    color = discord.Color.green()
  )
  if ((info['ram'] > 90) or (info['cpu'] > 90)):
    embed.color =  discord.Color.red()
  elif ((info['ram'] > 75) or (info['cpu'] > 75)):
    embed.color =  discord.Color.orange()    
    embed.add_field(name="Uptime", value=str(round(info['uptime']/60/60,2))+" Hours", inline=True)
  embed.add_field(name="Memory", value=str(info['ram'])+"%", inline=True)
  embed.add_field(name="CPU", value=str(info['cpu'])+"%", inline=True)
  embed.add_field(name="Storage", value=str(round(info['disk_usage']/1024/1024/1024,0))+"GB free", inline=True)

  return await ctx.send(embed=embed)

# @aiocron.crontab('* * * * *')
@aiocron.crontab('00 13 * * 1-5')
@bot.command(name='spaceship', description="Compares performance of Spaceship over last two days")
async def spaceshipCheck(ctx=False):
  CHECK_SPACESHIP = os.getenv("CHECK_SPACESHIP", 'False').lower() in ['true', '1']
  if CHECK_SPACESHIP is True or ctx is not False:
    data = json.loads(requests.get("https://newwwie.net/datasets/UNIVERSE.json").text)

    length = len(data) -1
    last = data[length]["aud_price"]
    last2 = data[length-1]["aud_price"]
    day = str(data[length]["date"])
    day2 = str(data[length-1]["date"])
    change = ((float(last) - float(last2))/float(last2)) * 100
    rounded = round(change,2)
    message = str("Change between " + day + " and " + day2 + " is " + str(rounded) + "%")
    
    embed=discord.Embed(
      title = "Spaceship Value Change", 
      description = message, 
      color = discord.Color.green()
    )
    embed.add_field(name=day2, value=str(last2), inline=True)
    embed.add_field(name=day, value=str(last), inline=True)
    if change < 0:
      embed.color =  discord.Color.red()

    user = await bot.fetch_user(owner_id)
    await user.send(embed=embed)

bot.run(os.getenv("TOKEN"))