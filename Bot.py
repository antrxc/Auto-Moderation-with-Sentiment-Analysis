import discord
import random
from discord.ext import commands
import asyncio
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

#bot = commands.Bot(command_prefix='!')
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

#to store number of warnings
warnings = {}

@bot.event
async def on_ready():
  print("I'm ready")


@bot.event
async def on_message(message):
  mute_roles= discord.utils.get(message.guild.roles, name='Timeout')
  moderator=[role for role in message.guild.roles if role.name=="Moderator"]
  mod=random.choice(moderator)
  
   # Ignore messages sent by the bot
  if message.author == bot.user:
    return

  sentiment = sia.polarity_scores(message.content)
  if sentiment['compound'] < -0.5:
    await message.delete()
    await message.channel.send('This message has been deleted for violating the community guidelines.')
    user = message.author
    if user in warnings:
      warnings[user] += 1
      if warnings[user] == 5:
        await user.add_roles(mute_roles)
        await message.channel.send(f"{mod.mention}, {user.name} needs to take a breather ")
        await asyncio.sleep(30)
        await user.remove_roles(mute_roles)
        del warnings[user] #deletes user's warning logs so he can come back if a moderator sees it right 
        
      else:
        print(5 - warnings[user])
    else:
      warnings[user] = 1
      print(5 - warnings[user])


bot.run('MTA2OTEwMzY4Mjg4NjU3ODE5Nw.GSsX5N.eRmS7NXeqmENptldEGcMcYr8QvGxyFhWlIL8OI')
