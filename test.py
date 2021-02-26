import json
# json from here: https://newwwie.net/datasets/UNIVERSE.json
with open ("UNIVERSE.json") as jsonData:
    data = json.load(jsonData)

# print(json.dumps(data, indent = 4, sort_keys=True))
# print len(data)
# print ("last"+ str(data[length][aud_price]))
# print ("second last "+ str(data[length -1]))
# print ("data " + str(data[0]))

length = len(data) -1
last = data[length]["aud_price"]
last2 = data[length-1]["aud_price"]
day = str(data[length]["date"])
day2 = str(data[length-1]["date"])
change = str(round(((float(last) - float(last2))/float(last2)) * 100))
print("Change between " + day + " and " + day2 + " is " + change + "%")

# schedule send to discord
# https://stackoverflow.com/questions/60719186/how-do-i-make-my-discord-bot-run-a-function-every-sunday-at-000
# import aiocron

# CHANNEL_ID=1234

# @aiocron.crontab('0 * * * *')
# async def cornjob1():
#     channel = bot.get_channel(CHANNEL_ID)
#     await channel.send('Hour Cron Test')