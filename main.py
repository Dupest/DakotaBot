# This example requires the 'message_content' intent.
import http.client
import json
import os
import random
import re
import urllib
import discord
import requests
from urllib.parse import quote
import interactions
from discord.app_commands import commands
from discord.ext import commands

special_phrases = open("special_phrases.txt", encoding='latin-1').readlines()
intents = discord.Intents.default()
intents.message_content = True
command_prefix = 'DakotaSlave '
bork = "the industrial revolution and its consequences have been a disaster for the human race"
# bot.= discord.bot.intents=intents)
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
LINKS_CHANNEL = 1032111758724304966
insults = open("insults", encoding='latin-1').readlines()
compliments = open("compliments", encoding='latin-1').readlines()
SUGGESTION_FILE = open("suggestions.txt", "a")
# LINK_FILE = open("links.txt", "w")
LINK_REGEX = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))'
ADD_REGEX = r'\/add (.*)'


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def trivia(ctx):
    url = f"https://the-trivia-api.com/api/questions?limit=1"
    data = requests.get(url)
    bot_response = json.loads(data.text)
    bot_response = bot_response[0]
    ans = []
    for incorrect in bot_response['incorrectAnswers']:
        ans.append(incorrect)
    ans.append(bot_response['correctAnswer'])
    random.shuffle(ans)
    answers_string = "  /  ".join(ans)
    formatted_text = f'Category: {bot_response["category"]}\n\nQuestion: {bot_response["question"]}\n\nChoices: {answers_string}'
    await ctx.send(formatted_text)

@bot.command()
async def catgif(ctx):
    url = f"https://cataas.com/cat/gif"
    data = requests.get(url)
    fp = open("image.gif", "wb")
    fp.write(data.content)
    fp.close()
    file = discord.File("image.gif", filename="image.gif")
    embed = discord.Embed()
    embed.set_image(url="attachment://image.gif")
    await ctx.channel.send(file=file, embed=embed)
    os.remove("image.gif")

@bot.command()
async def cat(ctx):
    url = f"https://cataas.com/cat"
    data = requests.get(url)
    fp = open("image.png", "wb")
    fp.write(data.content)
    fp.close()
    file = discord.File("image.png", filename="image.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://image.png")
    await ctx.channel.send(file=file, embed=embed)
    os.remove("image.png")
    #await ctx.send(data.url)

@bot.command()
async def compliment(ctx):
    url = f"https://www.affirmations.dev/"
    data = requests.get(url)
    bot_response = json.loads(data.text)
    await ctx.send(bot_response['affirmation'])

@bot.command()
async def insult(ctx):
    url ="https://evilinsult.com/generate_insult.php"
    data = requests.get(url)
    await ctx.send(data.text)

@bot.command()
async def inspire(ctx):
    url = "https://api.adviceslip.com/advice"
    data = requests.get(url)
    bot_response = json.loads(data.text)
    await ctx.send(bot_response['slip']['advice'])

@bot.command()
async def dad(ctx):
    url = "https://icanhazdadjoke.com/"
    data = requests.get(url,headers={"Accept": "application/json"})
    bot_response = json.loads(data.text)
    await ctx.send(bot_response['joke'])

@bot.command()
async def deep(ctx):
    url ="https://api.fisenko.net/v1/quotes/en/random"
    data = requests.get(url)
    bot_response = json.loads(data.text)
    await ctx.send(f'{bot_response["text"].strip(".")} - _{bot_response["author"]["name"]}, probably_.')

@bot.command()
async def magicball(ctx, *, msg):
    conn = http.client.HTTPSConnection("8ball.delegator.com")
    question = urllib.parse.quote(msg)
    conn.request('GET', '/magic/JSON/' + question)
    response = conn.getresponse()
    message = json.loads(response.read())
    bot_response = message['magic']['answer']
    await ctx.send(bot_response)


@bot.command()
async def jail(ctx):
    attachment = ctx.message.attachments[0]
    url = f"https://api.popcat.xyz/jail?image={attachment.url}"
    data = requests.get(url)
    await ctx.send(data.url)

@bot.command()
async def reply(ctx, msg):
    url = f"https://chatbot-api.gq/?message={quote(msg)}"
    data = requests.get(url)
    await ctx.send(data.text)


@bot.command()
async def tell(ctx, name, *, arg):
    await ctx.send(f'@{name} {arg}!')


@bot.command()
async def links(ctx):
    with open("links.txt", "w") as file:
        channel = bot.get_guild(1004907940626579488).get_channel(1032111758724304966)
        async for old_message in channel.history(limit=1000):
            link = re.search(LINK_REGEX, old_message.content)
            if link is not None:
                file.write(link.group(1) + "\n")
    await ctx.send("Ran!")


@bot.event
async def on_message(message):
    if not message.content.startswith(command_prefix):
        if message.channel == bot.get_channel(1011758287982706811):
            if len(message.attachments) == 0:
                return
            await message.add_reaction("😍")
            await message.add_reaction("❤")
        if message.content.lower().startswith("/playlist"):
            with open("links.txt", "w") as file:
                channel = bot.get_guild(1004907940626579488).get_channel(1032111758724304966)
                async for old_message in channel.history(limit=1000):
                    link = re.search(LINK_REGEX, old_message.content)
                    if link is not None:
                        file.write(link.group(1) + "\n")
                return
        if message.channel == bot.get_channel(12324234183172) or message.channel == bot.get_channel(1011778775052206112):
            return
        if message.author == bot.user:
            return
        if message.author.id == 132323816176091136 or message.author.id == 1004897999366922311:
            if message.content.lower().startswith("/add "):
                with open("special_phrases.txt", "a") as file:
                    file.write(message.content.strip("/add ") + "\n")
                await message.channel.send(f'Added "{message.content.strip("/add ")}" to the list.')
            # elif message.content.lower().startswith("mangle") or message.content.lower().startswith("rainbow"):
            #     await message.channel.send(f'<@278393257686335488> 10 page apology for Dakota. Now!')
        if message.content.lower().startswith('/suggest '):
            SUGGESTION_FILE.write(message.content.strip("/suggest "))
        stripped_content = re.sub(r'<[^>]+>', "", message.content.lower())
        stripped_content = re.sub(LINK_REGEX, "", stripped_content)
        numbers = re.findall(r'\d+', stripped_content)
        if len(numbers)>= 1:
            for num in numbers:
                if int(num) > 100 and len(num) != 19:
                    await message.channel.send(f'https://www.youtube.com/watch?v=WFoC3TR5rzI')
        if random.randint(1, 100) == 1:
            index = random.randint(0, len(special_phrases))
            if index == len(special_phrases):
                coin_flip = random.randint(0, 2)
                if coin_flip == 0:
                    await message.channel.send(f'<@278393257686335488> Tearful 10 page apology for Dakota. Now!')
                elif coin_flip == 1:
                    await message.channel.send(f'https://www.youtube.com/watch?v=c4KNd0Yv6d0')
                else:
                    await message.channel.send(f'<@763250505182609440> What up, it\'s yo boy skinny penis')
                return
            await message.channel.send(f'{message.author.mention} {special_phrases[index]}')
        elif "am sad" in message.content.lower() or "is sad" in message.content.lower() or "i\'m sad" in message.content.lower():
            choice = random.randint(0, len(compliments) - 1)
            compliment = compliments[choice].strip("\n")
            await message.channel.send(f'{message.author.mention} {compliment}')
        elif (message.content.lower().startswith('dakota') or str(bot.user).split("#")[
            0].lower() in message.content.lower() or "dakotaslave" in message.content.lower() or bot.user.mentioned_in(
            message)) and "sad" not in message.content.lower():
            choice = random.randint(0, len(insults) - 1)
            insult = insults[choice].strip("\n")
            await message.channel.send(f'{message.author.mention} {insult}')
    await bot.process_commands(message)


# bot.start()

bot.run(open("../DakotaBot/secrets").readline())
