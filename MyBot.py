import discord
from discord.ext import tasks, commands
import json
import psutil
import time
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

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

@bot.command(name='test', description="Test command")
async def test_command(ctx):
  # print(secrets['me'])
  if int(ctx.author.id) == int(owner_id):
    await ctx.send("Test command")

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

