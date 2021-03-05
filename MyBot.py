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

# requests.get('https://complimentr.com/api')).json()['compliment']

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
owner_id=os.getenv("OWNER_ID")

""" Owner Check """
async def cog_check(self, ctx):
    # Making sure author of these commands is the bot owner
    return await ctx.bot.is_owner(ctx.author)

@bot.event
async def on_ready():
  print('MyBot has logged with username: {0.user}'.format(bot))
  embed=discord.Embed(
    title = "MyBot is Online!", 
    description = "MyBot has successfully started", 
    color = discord.Color.green()
  )

  # Prev send to channel. Changed to DM instead
  # channel = bot.get_channel(813705175000678423)
  # await channel.send(embed=embed)
  
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
  if isinstance(error, CommandNotFound):
    #There has to be a better way of doing this...
    # commandRun = re.findall(r'"([^"]*)"', str(error))
    # commandRun = commandRun[0]
    
    #Below command will list out all ctx attributes
    # dir(ctx)

    #The better way
    commandRun = ctx.message.content.split(" ")[0][1:]
    for command, value in command_list.items():
      if str(command) == commandRun:
        # print("match found "+ command)
        # print(value)
        output = subprocess.getoutput(value)
        # print(output)
        embed=discord.Embed(
          title = "Command Run: '" + command + "'", 
          description = output, 
          color = discord.Color.green()
        )
        return await ctx.send(embed=embed)

    # print("Did not match " + command)
    embed=discord.Embed(
      title = "No Command Found", 
      description = "Did not match " + command + ". Commands include: " + str(command_list), 
      color = discord.Color.red()
    )
    return await ctx.send(embed=embed)

  embed=discord.Embed(
    title = "Oh snap! An error occured", 
    description = "The error was: " + error, 
    color = discord.Color.red()
  )
  return await ctx.send(embed=embed)

@bot.command(name='test', description="Test command")
async def test_command(ctx):
  # print(secrets['me'])
  if int(ctx.author.id) == int(owner_id):
    await ctx.send("Test command")

@bot.command(name='dmtest', description="Test DM command")
async def dm_test(ctx):
  #The below works to send a message directly to a user by ID. Will re-use for functions not called by a command.
  user = await bot.fetch_user(owner_id)
  await user.send("Your message here")

@bot.command(name='myip', description="Returns public IP")
async def my_ip(ctx):
  ip = get('https://api.ipify.org').text
  # print('My public IP address is: {}'.format(ip))
  embed=discord.Embed(
    title = "Public IP", 
    description = "IP: " + ip, 
    color = discord.Color.green()
  )
  return await ctx.send(embed=embed)

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