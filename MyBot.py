import discord
from discord.ext import tasks, commands
import json
import psutil
import time
import os
from dotenv import load_dotenv
from discord.ext.commands import CommandNotFound

# requests.get('https://complimentr.com/api')).json()['compliment']

load_dotenv(dotenv_path=".env")

with open('commands.json') as command_json:
  command_list = json.load(command_json)

bot = commands.Bot(
    command_prefix=os.getenv("PREFIX"),
    owner_id=os.getenv("OWNER_ID"),
    case_insensitive=True,
    help_command=None
)
owner_id=os.getenv("OWNER_ID")

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  embed=discord.Embed(
    title = "MyBot is Online!", 
    description = "MyBot has successfully started", 
    color = discord.Color.green()
  )
  channel = bot.get_channel(813705175000678423)
  await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      # commandrun = bot.get_command()
      # print(commandrun)
      # for command in command_list:
      #   print(command)
      embed=discord.Embed(
        title = "No Command", 
        description = "Command not found", 
        color = discord.Color.green()
      )
      print(command_list)

      return await ctx.send(embed=embed)
    raise error

@bot.command(name='test', description="Test command")
async def test_command(ctx):
  # print(secrets['me'])
  if int(ctx.author.id) == int(owner_id):
    await ctx.send("Test command")

@bot.command(name='dmtest', description="Test command")
async def dm_test(ctx):
  #The below works to send a message directly to a user by ID. Will re-use for functions not called by a command.
  user = await bot.fetch_user(owner_id)
  await user.send("Your message here")

@bot.command(name='status', description="status command")
async def systemstatus(ctx):
  if int(ctx.author.id) == int(owner_id):
    info={}
    info['ram']=psutil.virtual_memory().percent
    info['cpu']=psutil.cpu_percent()
    info['uptime']=time.time() - psutil.boot_time()    
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
  
  return await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))

