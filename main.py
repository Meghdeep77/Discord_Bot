import discord
import requests
import json
import datetime as dt
from replit import db
from keep_alive import keep_alive

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Analyze sentiment

keep_alive()
db.clear()



intents =discord.Intents.all()
client = discord.Client(intents=intents)
def get_weather(City):
  Base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+City+'?unitGroup=metric&key=JNGM2PPA6W8SXB4H35BX4R2G3&contentType=json'
  response = requests.get(Base_url)
  data = response.json()
  res = 'The weather in your city is '
  for key,value in data['currentConditions'].items():
    res += str(key) + ' : ' + str(value) + '\n'
  return res
def update_database(user, message):
  try:
      if user in db:
          db[user]['Message_count'] += 1
          db[user]['Sentiment_score'] += sia.polarity_scores(message)['compound']
          db[user]['Average_sentiment'] = db[user]['Sentiment_score'] / db[user]['Message_count']
      else:
          db[user] = {'Message_count': 1, 'Sentiment_score': sia.polarity_scores(message)['compound'], 'Average_sentiment': sia.polarity_scores(message)['compound']}
  except Exception as e:
      print("Error updating database:", e)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  
  if message.author == client.user:
    return

  update_database(str(message.author),str(message.content))
  if message.content.startswith('hello') :
    await message.channel.send('Hello!')

  if message.content.startswith('/weather') :
    con = message.content.split(' ')
    await message.channel.send(get_weather(con[1]))
  if message.content.startswith('/stats') :
    for key,value in db[str(message.author)].items():
      await message.channel.send(str(key) + ' : ' + str(value))
  print(str(message.content))
  for key,value in db.items():
    print(key)
    print(value)


client.run('MTI0ODE0NTM5OTczMDkzMzc3Mg.G-zlrQ.JQ7KOm-IIHF6I9FyFKz9XjPwVWwPpkzEx8rA0I')


