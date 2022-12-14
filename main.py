import http.client
import json
import os
import random
import re
import pdb
from datetime import datetime
import logging
import discord
import requests
from urllib.parse import quote
from discord.ext import commands
import mariadb

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
config = json.load(open("config.json"))
db = json.load(open("mariadb.json"))
#chatbot = Chatbot(config, conversation_id=None)
command_prefix = '!'
bork = "the industrial revolution and its consequences have been a disaster for the human race"
# bot.= discord.bot.intents=intents)
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
LINKS_CHANNEL = 1032111758724304966
compliments = open("compliments", encoding='latin-1').readlines()
# LINK_FILE = open("links.txt", "w")
LINK_REGEX = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))'
ADD_REGEX = r'\/add (.*)'
CONN = None
# Channels bot can talk in
ALLOWED_CHANNELS = [1004907941322821725, 1035372306928779405, 1012129620964945920]
# Allowed users
GOD_USERS = [132323816176091136, 1004897999366922311]
async def simp_for(member):
    cursor = CONN.cursor()
    cursor.execute(f'UPDATE `counter_table` set count=count+1 WHERE id=1')
    CONN.commit()
    cursor.execute('select `count` from `counter_table` where id=1')
    count = cursor.fetchone()
    await bot.get_guild(1004907940626579488).get_channel(1004907941322821725).send(f"{count[0]-1} \
                people have simped for Dakota. {member.mention} is the {count[0]}th.")
def db_connection():
    global CONN
    CONN = mariadb.connect(
                    user= db['user'],
                    password= db['password'],
                    host=db['host'],
                    port=db['port'],
                    database=db['database']
    )
    logging.info("Connected to the database!")
@bot.event
async def on_resumed():
    try:
        channel = bot.get_guild(1004907940626579488).get_channel(1004907941322821725)
        #await channel.send("I'm a simp for Dakota")
        logging.info("Refreshing the database connection")
        CONN.reconnect()
    except:
        logging.info("Could not use reconnect, recreating the connection")
        db_connection()
@bot.event
async def on_member_join(member):
    cursor = CONN.cursor()
    cursor.execute(f'UPDATE `counter_table` set count=count+1 WHERE id=3')
    CONN.commit()
    cursor.execute('select `count` from `counter_table` where id=3')
    count, = cursor.fetchone()
    if count % 15 == 0:
        await simp_for(member)
@bot.event
async def on_ready():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    db_connection()
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
#@bot.command()
# async def trump(ctx):
#     url = "https://api.tronalddump.io/random/quote"
#     data = requests.get(url)
#     message = json.loads(data.text)
#     bot_response = message['value']
#     await ctx.send(f'{bot_response} - _Dakota Trump_')

@bot.command()
async def basically(ctx):
    url = "http://itsthisforthat.com/api.php?text"
    data = requests.get(url)
    await ctx.send(data.text)

@bot.command()
async def boss(ctx):
    url = "https://corporatebs-generator.sameerkumar.website/"
    data = requests.get(url)
    data = json.loads(data.text)
    await ctx.send(data['phrase'])
@bot.command()
async def deletelast(ctx):
    if ctx.author.id in GOD_USERS:
        cursor = CONN.cursor()
        cursor.execute("select * from `dakota_phrases`")
        messages = cursor.fetchall()
        message_id, message = messages[-1]
        #pdb.set_trace()
        cursor.execute(f'delete from `dakota_phrases` where id={message_id}')
        CONN.commit()
        await ctx.send(f'"{message}" was removed from the list.')
    else:
        await ctx.send("Haha, thanks for trying.")
@bot.command()
async def delete_one(ctx):
    if ctx.author.id in GOD_USERS:
        print(ctx.message.content.replace(f'{command_prefix}delete_one', ""))
        try:
            message_id = int(ctx.message.content.replace(f'{command_prefix}delete_one', ""))
        except:
            await ctx.send("Not a valid number!")
            return
        cursor = CONN.cursor()
        cursor.execute(f"select message from `dakota_phrases` where id={message_id}")
        message = cursor.fetchone()
        if message is None:
            await ctx.send("Not a valid index! Please use !list_all and use an exsting one")
        del_message, = message
        #pdb.set_trace()
        cursor.execute(f'delete from `dakota_phrases` where id={message_id}')
        CONN.commit()
        await ctx.send(f'"{del_message}" was removed from the list.')
    else:
        await ctx.send("Haha, thanks for trying.")

@bot.command()
async def list_all(ctx):
    cursor = CONN.cursor()
    cursor.execute("select * from `dakota_phrases`")
    messages = cursor.fetchall()
    print_out = ""
    for message in messages:
        message_id, ind_message = message
        print_out += f'{message_id}: {ind_message}\n'
    await ctx.send(f'Current Phrases:\n{print_out}')

@bot.command()
async def current_suggestions(ctx):
    cursor = CONN.cursor()
    cursor.execute("select * from `suggested_quotes`")
    messages = cursor.fetchall()
    print_out = ""
    for message in messages:
        message_id, ind_message, username, time = message
        print_out += f'{message_id}: {username} suggested: "{ind_message}"\n'
    await ctx.send(f'Current Phrases:\n{print_out}')
@bot.command()
async def ask(ctx, *, msg):
    # conn = http.client.HTTPSConnection("eightballapi.com/api")
    # question = urllib.parse.quote(msg)
    # conn.request('GET', '/magic/JSON/' + question)
    # response = conn.getresponse()
    # message = json.loads(response.read())
    # bot_response = message['magic']['answer']
    # await ctx.send(bot_response)
    url = "https://www.eightballapi.com/api"
    data = requests.get(url)
    data = json.loads(data.text)
    await ctx.send(data['reading'])


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

@bot.command()
async def simp(ctx):
    cursor = CONN.cursor()
    cursor.execute(f'UPDATE `counter_table` set count=count+1 WHERE id=1')
    CONN.commit()
    cursor.execute('select `count` from `counter_table` where id=1')
    count = cursor.fetchone()
    await ctx.send(f"{count[0]-1} people have simped for Dakota. You're the {count[0]}th. Simp.")

@bot.event
async def on_message(message):
    if not message.content.startswith(command_prefix):
        if message.channel == bot.get_channel(1011758287982706811):
            if len(message.attachments) == 0:
                return
            await message.add_reaction("😍")
            await message.add_reaction("❤")
        if message.channel.id not in ALLOWED_CHANNELS:
            return
        if message.content.lower().startswith("/playlist"):
            with open("links.txt", "w") as file:
                channel = bot.get_guild(1004907940626579488).get_channel(1032111758724304966)
                async for old_message in channel.history(limit=1000):
                    link = re.search(LINK_REGEX, old_message.content)
                    if link is not None:
                        file.write(link.group(1) + "\n")
                return
        if message.author.id == 418230537250144257:
            cursor = CONN.cursor()
            cursor.execute(f'INSERT INTO `mangle_comments` (message, time) VALUES (%s, %s)', (message.content, datetime.utcnow()))
            CONN.commit()
        if message.author == bot.user:
            return
        if message.author.id in GOD_USERS:
            if message.content.lower().startswith("/add "):
                #with open("special_phrases.txt", "a") as file:
                    #file.write(message.content.strip("/add ") + "\n")
                cursor = CONN.cursor()
                cursor.execute(f'INSERT INTO `dakota_phrases` (message) VALUES (%s)', (message.content.replace("/add ", ""),))
                CONN.commit()
                await message.channel.send(f'Added "{message.content.replace("/add ", "")}" to the list.')
            # elif message.content.lower().startswith("mangle") or message.content.lower().startswith("rainbow"):
            #     await message.channel.send(f'<@278393257686335488> 10 page apology for Dakota. Now!')
        if message.content.lower().startswith('/suggest '):
            cursor = CONN.cursor()
            cursor.execute(f'INSERT INTO `suggested_quotes` (message, username, time) VALUES (%s,%s,%s)',
                           (message.content.replace("/suggest ", ""), message.author.name, datetime.utcnow()))
            CONN.commit()
            await message.channel.send(f'Added "{message.content.replace("/suggest ", "")}" to the list.')
        stripped_content = re.sub(r'<[^>]+>', "", message.content.lower())
        stripped_content = re.sub(LINK_REGEX, "", stripped_content)
        numbers = re.findall(r'\d+', stripped_content)
        if len(numbers)>= 100:
            for num in numbers:
                if int(num) > 1000000 and len(num) != 19:
                    await message.channel.send(f'https://www.youtube.com/watch?v=WFoC3TR5rzI')
                    return
        if random.randint(1, 100) == 1 or "dakotaslave" in message.content.lower() or (message.content.lower().startswith('dakota') or message.content.lower().startswith(str(bot.user).split("#")[0])):
            cursor = CONN.cursor()
            cursor.execute(f'SELECT `message` FROM dakota_phrases')
            #CONN.commit()
            special_phrases = list(cursor.fetchall())
            index = random.randint(0, len(special_phrases))
            if index == len(special_phrases):
                dice_roll = random.randint(0, 3)
                if dice_roll == 0:
                    await message.channel.send(f'<@418230537250144257>')
                    await message.channel.send(file=discord.File('boomer.jpg'))
                elif dice_roll == 1:
                    await message.channel.send(f'https://www.youtube.com/watch?v=c4KNd0Yv6d0')
                elif dice_roll == 2:
                        await message.channel.send(f'{message.author.mention} I\'m going to spit on you. AAACHK-PTU! That\'s what you get')
                else:
                    await message.channel.send(f'<@763250505182609440> What up, it\'s yo boy skinny penis')
                return
            picked_phrase = special_phrases[index][0]
            await message.channel.send(f'{message.author.mention} {picked_phrase}')
        elif "am sad" in message.content.lower() or "is sad" in message.content.lower() or "i\'m sad" in message.content.lower():
            choice = random.randint(0, len(compliments) - 1)
            compliment = compliments[choice].strip("\n")
            await message.channel.send(f'{message.author.mention} {compliment}')
        # One in a million chance that a user's comment wins something special
        elif random.randint(1,1000000) == 1:
            await message.channel.send(f'{message.author.mention} you just won a month of spicy membership :eyes_shake:')
            await message.channel.send(f'<@1004897999366922311> <@132323816176091136>')
        # elif (message.content.lower().startswith('dakota') or str(bot.user).split("#")[
        #     0].lower() in message.content.lower() or "dakotaslave" in message.content.lower() or bot.user.mentioned_in(
        #     message)) and "sad" not in message.content.lower():
        #     choice = random.randint(0, len(insults) - 1)
        #     insult = insults[choice].strip("\n")
        #     await message.channel.send(f'{message.author.mention} {insult}')
    await bot.process_commands(message)


if __name__ == '__main__':
    bot.run(open("../DakotaBot/secrets").readline())



