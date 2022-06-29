import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

import discord
from discord import Embed
from discord.ext import commands
from discord.colour import Colour
from discord.commands import Option

import youtube_dl

import random
import time
import math
from math import pi

import logging
if True == True:
  logging.basicConfig(level=logging.INFO)

import socket



def conServer():
    try:
        server = socket.socket()
        port = int(os.environ.get("PORT", 12345))
        server.bind(("0.0.0.0", port))
        server.listen(5)
    except:
        conServer()
conServer()

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
'format': 'bestaudio[ext=m4a]/best[ext=mp4]/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#####################   ---  Config  ---   #####################


bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=discord.Intents.all())
bot.remove_command("help")
guilds = [int(os.getenv("GUILDS"))]
botVersion = "Version 2.2 - The Amelioration"


#####################   ---  Apps  ---   #####################


@bot.user_command(name="1) Help", guild_ids = guilds)
async def help_app(ctx, user):
    help_em = Embed(title="Help", description="Use '/help <options> <choice>' to get more information.", color=Colour.blue())
    help_em.add_field(name="Music:", value="> join, play, dplay, stop, volume")
    help_em.add_field(name="Fastreplies:", value="> hello, ping, color, id, myid, getid, github, version")
    help_em.add_field(name="Fun:", value="> roll, roulette, mimic, 8ball, vbucks")
    help_em.add_field(name="Maths:", value="> add, sub, mult, div, pow, root, pi")
    help_em.add_field(name="Convert:", value="> cm_inch, km_miles, kmh_mph, mps_kmh, c_f, l_gal")
    help_em.add_field(name="᲼᲼", value="᲼᲼", inline=False)
    help_em.add_field(name="If you want to have a look at the bot's code or set it up yourself, check out it's GitHub:" ,value="https://github.com/Matthaeus07/enhanced-bot", inline=False)
    await ctx.respond(embed = help_em)

@bot.user_command(name="2) Say Hello", guild_ids = guilds)
async def hi_app(ctx, user):
    send = Embed(description=f"{ctx.author.mention} says hello to {user.name}!", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.user_command(name="3) GitHub", guild_ids = guilds)
async def github_app(ctx, user):
    send = Embed(description=f"If you want to have a look at the bot's code or set it up yourself, check out it's GitHub:\nhttps://github.com/Matthaeus07/enhanced-bot", color=Colour.blurple())
    send.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/25/25231.png")
    await ctx.respond(embed = send)


#####################   ---  Music Commands  ---   #####################


@bot.slash_command(guild_ids = guilds)
async def join(ctx, *, channel: Option(discord.VoiceChannel, "The channel the bot should join:", required = True)):
    """Joins a voice channel."""

    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    send = Embed(description=f"Successfully connected to *{channel}*", color=Colour.blurple())
    await ctx.respond(embed = send)
    await channel.connect()

@bot.slash_command(guild_ids = guilds)
async def play(ctx, *, title: Option(str, "URL or title of the song:", required = True)):
    """Streams from Youtube.com."""

    send=Embed(description=f'Search started. Please wait!', color=Colour.blurple())
    await ctx.respond(embed = send)

    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(title, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        
        send = Embed(description=f'Now streaming: *{player.title}*', color=Colour.blurple())
        await ctx.send(embed = send)
    except:
        error = Embed(title="Error", description="Couldn't get video data. - *HTTP Error 403: Forbidden*", color=Colour.brand_red())
        await ctx.respond(embed=error)

@bot.slash_command(guild_ids = guilds)
async def dplay(ctx, *, title: Option(str, "URL or title of the song:", required = True)):
    """Downloads and plays music from youtube.com in high quality."""

    send=Embed(description=f'Search and Download started. Please wait!', color=Colour.blurple())
    await ctx.respond(embed = send)

    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(title, loop=bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        send=Embed(description=f'Now playing:\n*{player.title}*', color=Colour.blurple())
        await ctx.send(embed = send)
    except:
        error = Embed(title="Error", description="Couldn't download video data. - *HTTP Error 403: Forbidden*", color=Colour.brand_red())
        await ctx.respond(embed=error)


@bot.slash_command(guild_ids = guilds)
async def volume(ctx, volume: Option(int, "The volume for the player:", required = True)):
    """Changes the player's volume (standard volume = 50%)."""

    if ctx.voice_client is None:
        error = Embed(title="Error", description="Not connected to a voice channel.", color=Colour.brand_red())
        return await ctx.send(embed=error)

    ctx.voice_client.source.volume = volume / 100
    send = Embed(description = f"Changed volume to {volume}%", color=Colour.blurple())
    await ctx.respond(embed=send)

@bot.slash_command(guild_ids = guilds)
async def stop(ctx):
    """Stops and disconnects the bot from voice."""

    send = Embed(description="Stopped and disconnected from voice.", color=Colour.blurple())
    await ctx.respond(embed=send)
    await ctx.voice_client.disconnect()

@play.before_invoke
@dplay.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            error = Embed(title="Error", description="You are not connected to a voice channel.", color=Colour.brand_red())
            await ctx.respond(embed=error)
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


#####################   ---  Fast Replies  ---   #####################


@bot.slash_command(guild_ids = guilds)
async def hello(ctx, name: Option(str, "The name of the person you want to say hello to:", required = False, default = None)):
    """Greets a user."""
    if name == None:
        name = ctx.author.mention
    send = Embed(description=f'Hello {name}!', color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def ping(ctx):
    """Checks the bot's latency."""
    send = Embed(description=f"Pong! {round(bot.latency * 1000)}ms", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def version(ctx):
    """Displays version info."""
    myid = '<@886986392310255617>'
    send = Embed(description=f"The current version of the {myid} is:  _**{botVersion}**_", color=Colour.blurple())
    await ctx.respond(embed = send)
        
@bot.slash_command(guild_ids = guilds)
async def color(ctx, colorcode: Option(str, "A hexadecimal colour code:", required = True)):
    """Diplays the entered hexadecimal color code."""
    colorhex = colorcode
    if "#" in colorhex:
        colorhexreadable = colorhex.replace("#", "")
        colorhex = colorhex.replace("#", "")
    else:
        colorhexreadable = colorhex
    if not '0x' in colorhexreadable:
        colorhexreadable = ''.join(('0x', colorhexreadable))
    try:
        readableHex = int(colorhexreadable, 0)
    except:
        await ctx.respond(f'{colorhex} is not a valid color code')

    embed = Embed(description = '', color = readableHex)
    embed.set_author(name = f'#{colorhex}')
    if '0x' in colorhex:
        colorhex = colorhex.replace("0x", "")
    embed.set_thumbnail(url = f'https://www.colorhexa.com/{colorhex}.png')
    embed.add_field(name = 'looks like', value='this -->', inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = guilds)
async def publish(ctx, heading: Option(str, "Heading for your message:", required = True), 
                        message: Option(str, "The message you want to publish:", required = True),
                        author: Option(str, "The name of the author:", required = False, default = None),
                        footer: Option(str, "The footer for your message:", required = False, default = None),
                        image: Option(str, "An image URL:", required = False, default = None),
                        thumbnail: Option(str, "A thumbnail URL:", required = False, default = None)):
    """Publishes an embeded message to the channel."""
    
    send = Embed(color=Colour.blurple())
    send.title = heading
    send.description = message

    if author != None:
        send.set_author(name = author)
    if footer != None:
        send.set_footer(text = footer)
    if image != None:
        send.set_image(url = image)
    if thumbnail != None:
        send.set_thumbnail(url = thumbnail)
    
    await ctx.respond(embed = send)
        
@bot.slash_command(guild_ids = guilds)
async def id(ctx, id: Option(str, "Choose what id you want to get displayed", choices = ["myid", "botid"], required = True)):
    """Let the bot display the id of different things."""
    if id == "myid":
        send = Embed(description=f'Your user id is: ***{ctx.author.id}***', color=Colour.blurple())
        await ctx.respond(embed = send)

    if id == "botid":
        send = Embed(description=f'My bot id is ***{bot.user.id}***', color=Colour.blurple())
        await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def getid(ctx, getid: Option(str, "Mention a user:", required = True)):
    """Get the id of the mentioned user."""
    if "@" in getid:
        mentionID = getid.replace("<","")
        mentionID = mentionID.replace(">","")
        mentionID = mentionID.replace("@","")
        mentionID = mentionID.replace("!","")
        send = Embed(description=f"{getid}'s user id is: ***{mentionID}***", color=Colour.blurple())
        await ctx.respond(embed = send)
    else:
        error = Embed(title="Error", description="You have to mention a user!", color=Colour.brand_red())
        await ctx.respond(embed = error)

@bot.slash_command(guild_ids = guilds)
async def github(ctx):
    """Displays info about the bot's GitHub."""
    send = Embed(description=f"If you want to have a look at the bot's code or set it up yourself, check out it's GitHub:\n\nhttps://github.com/Matthaeus07/enhanced-bot", color=Colour.blurple())
    send.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/25/25231.png")
    await ctx.respond(embed = send)


#####################   ---  Admin Commands  ---   #####################


@bot.slash_command(guild_ids = guilds)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: Option(int, "The amount of messages to delete:", required = True)):
    """Deletes given amount of messages."""
    await ctx.channel.purge(limit=amount)
    send = Embed(description=f"Deleted {amount} messages!", color=Colour.blurple())
    await ctx.respond(embed = send)
    time.sleep(3)
    await ctx.channel.purge(limit=1)


#####################   ---  Math Commands  ---   #####################


@bot.slash_command(guild_ids = guilds)
async def add(ctx, first_number: Option(float, "Enter the first number.", required = True), second_number: Option(float, "Enter the second number.", required = True)):
    """Adds two numbers numbers together."""
    send = Embed(description=f"{first_number} + {second_number} = {first_number + second_number}", color=Colour.blurple())
    await ctx.respond(embed = send)
    
@bot.slash_command(guild_ids = guilds)
async def mult(ctx, first_number: Option(float,"Enter the first number.", required = True), second_number: Option(float, "Enter the second number.", required = True)):
    """Multiplies two numbers numbers together."""
    send = Embed(description=f"{first_number} × {second_number} = {first_number * second_number}", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def sub(ctx, first_number: Option(float, "Enter the minuend.", required = True), second_number: Option(float, "Enter the subtrahend.", required = True)):
    """Subtracts the 2nd number from the 1st."""
    result = first_number - second_number
    send = Embed(description=f"{first_number} - {second_number} = {first_number - second_number}", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def div(ctx, first_number: Option(float, "Enter the dividend.", required = True), second_number: Option(float, "Enter the divisor.", required = True)):
    """Divides the 2nd number from the 1st."""
    result = first_number / second_number
    send = Embed(description=f"{first_number} / {second_number} = {first_number / second_number}", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def pow(ctx, first_number: Option(float, "Enter the base number.", required = True), second_number: Option(float, "Enter the exponent (default is 2).", required = False, default = 2)):
    """Raises the 1st number to the powrer of the 2nd number."""
    if first_number > 500 or second_number > 100:
        send = Embed(title="Error", description="Sorry, the entered numbers are too high.", color=Colour.brand_red())
        await ctx.respond(embed = send)
    else:
        send = Embed(description=f"{first_number}^{second_number} = {math.pow(first_number, second_number)}", color=Colour.blurple())
        await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def root(ctx, first_number: Option(float, "Enter the radicand.", required = True), second_number: Option(float, "Enter the degree (default is 2).", required = False, default = 2)):
    """Returns the root of the entered number."""
    if first_number > 500 or second_number > 100 or first_number < 0 or second_number < 0:
        send = Embed(title="Error", description="Sorry, the entered numbers are too high / too low.", color=Colour.brand_red())
        await ctx.respond(embed = send)
    else:
        send = Embed(description=f"{first_number}^(1 / {second_number}) = {first_number ** (1 / second_number)}", color=Colour.blurple())
        await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def pi(ctx):
    """Displays the number pi."""
    send = Embed(description=f"Pi = {pi}", color=Colour.blurple())
    await ctx.respond(embed = send)


#####################   ---  Convert Commands  ---   #####################


@bot.slash_command(guild_ids = guilds)
async def km_miles(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts kilometres to miles / miles to kilometres."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="Kilometres", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 1.609344
            send = Embed(description=f"{number} miles are {result} kilometres.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="Miles", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 0.621371
            send = Embed(description=f"{number} kilometres are {result} miles.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()

@bot.slash_command(guild_ids = guilds)
async def cm_inch(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts centimetres to inch / inch to centimetres."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="Centimetres", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 2.54
            send = Embed(description=f"{number} inch are {result} centimetres.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="Inch", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number / 2.54
            send = Embed(description=f"{number} centimetres are {result} inch.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()

@bot.slash_command(guild_ids = guilds)
async def mps_kmh(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts metre per second to kilometres per hour / kilometres per hour to metre per second."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="Metres per second", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 0.277778
            send = Embed(description=f"{number} kilometres per hour are {result} metres per second.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="Kilometres per hour", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 3.6
            send = Embed(description=f"{number} metres per second are {result} kilometres per hour.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()

@bot.slash_command(guild_ids = guilds)
async def kmh_mph(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts kilometres per hour to miles per hour / miles per hour to kilometres per hour."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="Kilometres per hour", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 1.609344
            send = Embed(description=f"{number} miles per hour are {result} kilometres per hour.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="Miles per hour", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number / 1.609344
            send = Embed(description=f"{number} kilometres per hour are {result} miles per hour.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()

@bot.slash_command(guild_ids = guilds)
async def c_f(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts celsius to fahrenheit / fahrenheit to celsius."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="°Celsius", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = (number - 32) * 5/9
            send = Embed(description=f"{number} °F are {result} °C.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="°Fahrenheit", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = (number * 9 / 5) + 32
            send = Embed(description=f"{number} °C are {result} °F.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()

@bot.slash_command(guild_ids = guilds)
async def l_gal(ctx, number: Option(float, "Number you want to convert:", required = True)):
    """Converts litres to gallons / gallons to litres."""
    class ConvertTo(discord.ui.View):
        def __init__(self):
            super().__init__()
        @discord.ui.button(label="Litres", style=discord.ButtonStyle.primary)
        async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number * 4.54609
            send = Embed(description=f"{number} gallons are {result} litres.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
        @discord.ui.button(label="Gallons (UK)", style=discord.ButtonStyle.primary)
        async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
            result:float = number / 4.54609
            send = Embed(description=f"{number} litres are {result} gallons.", color=Colour.blurple())
            await interaction.response.send_message(embed = send)
            self.stop()
    view = ConvertTo()
    ask = Embed(description=f"To what do you want to convert it to?", color=Colour.blurple())
    await ctx.respond(embed = ask, view=view)
    await view.wait()


#####################   ---  Fun Commands  ---   #####################


@bot.slash_command(guild_ids = guilds)
async def roll(ctx, ndn: Option(str, "(n = amount of dice; d = seperator; n = amount of sides    -->    zb: '.roll 5d6')", required = True)):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, ndn.split('d'))
    except Exception:
        send = Embed(description=f"Format has to be in NdN!", color=Colour.blurple())
        await ctx.respond(embed = send)
        return
    if rolls > 100 or limit > 1000:
        send = Embed(description=f"Entered numbers are too high!", color=Colour.blurple())
        await ctx.respond(embed = send)
        return
    elif rolls < 0 or limit < 0:
        send = Embed(description=f"Entered numbers are too low!", color=Colour.blurple())
        await ctx.respond(embed = send)
        return
    else:
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        send = Embed(description=result, color=Colour.blurple())
        await ctx.respond(embed = send)
    
@bot.slash_command(guild_ids = guilds)
async def roulette(ctx):
    """Play russian roulett with the bot. You have a 1:6 chance to loose."""
    result = str(random.randint(1, 6))
    if result == "1":
        send = Embed(description="*Pow!!!*\nSorry you died.", color=Colour.blurple())
        await ctx.respond(embed = send)
    else:
        send = Embed(description="*Click*\nYay you live", color=Colour.blurple())
        await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def mimic(ctx, words: Option(str, "Words the bot should mimic:", required = True)):
    """Mimics the entered words."""
    output = ""
    prefix = ["", "", "", "", "", "", "", "I just said: ", f"Hey, I am {ctx.author.mention} and I just said: ", "`Initialising mimic process...\nProcess complete.\nI just said:` "]
    random_prefix = random.choice(prefix)
    send = Embed(description=f"{random_prefix}{words}", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds, name="8ball")
async def _8ball(ctx, question: Option(str, "Ask the bot a question.", required = True)):
    """Play 8ball with an enhanced fortune teller."""
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", #Good answers
                    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", #neutral answers
                    "Don’t count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."] #bad answers
    send = Embed(description=f"Processing question: '{question}'\nAwnser: '||{random.choice(responses)}||'", color=Colour.blurple())
    await ctx.respond(embed = send)

@bot.slash_command(guild_ids = guilds)
async def vbucks(ctx):
    """Do you want V-Bucks?"""
    view = Confirm()
    send = Embed(description="Do you want free V-Bucks?", color=Colour.blurple())
    await ctx.respond(embed = send, view=view)
    await view.wait()
    outcome_yes = ["Yayy, have your V-Bucks.", "Here you go: 2000 V-Bucks!", "Haha you got bamboozled! I don't have any V-Bucks.", "Sorry you got kidnapped!"]
    outcome_no = ["Why don't you like my V-Bucks?", "What is wrong with you?", "What are you doing? I would have given you 2000 V-Bucks."]
    if view.value is None:
        send = Embed(description=f"Why don't you say anything {ctx.author.mention}?", color=Colour.blurple())
        await ctx.respond(embed = send)
    elif view.value:
        send = Embed(description=random.choice(outcome_yes), color=Colour.blurple())
        await ctx.respond(embed = send)
    else:
        send = Embed(description=random.choice(outcome_no), color=Colour.blurple())
        await ctx.respond(embed = send)



class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.primary)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()
        

#####################   ---  Help Commands  ---   #####################


HELP_MUSIC_CHOICES = ["● Music", "▸ join", "▸ play", "▸ stream", "▸ stop", "▸ volume"]
HELP_FASTREPLIES_CHOICES = ["● FastReplies", "▸ hello", "▸ ping", "▸ publish", "▸ color", "▸ id", "▸ getid", "▸ version"]
HELP_ADMIN_CHOICES = ["● Admin", "▸ clear"]
HELP_FUN_CHOICES = ["● Fun", "▸ roll", "▸ roulette", "▸ mimic", "▸ 8ball", "▸ vbucks"]
HELP_MATHS_CHOICES = ["● Maths", "▸ add", "▸ mult", "▸ sub", "▸ div", "▸ pow", "▸ root", "▸ pi"]
HELP_CONVERT_CHOICES = ["● Convert", "▸ cm_inch", "▸ km_miles", "▸ kmh_mph", "▸ mps_kmh", "▸ c_f", "▸ l_gal"]


@bot.slash_command(guild_ids = guilds)
async def help(ctx, music: Option(str, "Get help about the commands in the 'Music' group.", choices = HELP_MUSIC_CHOICES, required = False),
                    fastreplies: Option(str, "Get help about the commands in the 'FastReplies' group.", choices = HELP_FASTREPLIES_CHOICES, required = False),
                    admin: Option(str, "Get help about the commands in the 'Admin' group.", choices = HELP_ADMIN_CHOICES, required = False),
                    fun: Option(str, "Get help about the commands in the 'Fun' group.", choices = HELP_FUN_CHOICES, required = False),
                    maths: Option(str, "Get help about the commands in the 'Maths' group.", choices = HELP_MATHS_CHOICES, required = False),
                    convert: Option(str, "Get help about the commands in the 'Convert' group.", choices = HELP_CONVERT_CHOICES, required = False)):
    """Get help here!"""

    if music == None and fastreplies == None and admin == None and fun == None and maths == None and convert == None:
        help_em = Embed(title="Help", description="Use '/help <options> <choice>' to get more information.", color=Colour.blue())
        help_em.add_field(name="Music:", value="> join, play, dplay, stop, volume")
        help_em.add_field(name="Fastreplies:", value="> hello, ping, publish, color, id, myid, getid, github, version")
        help_em.add_field(name="Fun:", value="> roll, roulette, mimic, 8ball, vbucks")
        help_em.add_field(name="Maths:", value="> add, sub, mult, div, pow, root, pi")
        help_em.add_field(name="Convert:", value="> cm_inch, km_miles, kmh_mph, mps_kmh, c_f, l_gal")
        help_em.add_field(name="᲼᲼", value="᲼᲼", inline=False)
        help_em.add_field(name="If you want to have a look at the bot's code or set it up yourself, check out it's GitHub:" ,value="https://github.com/Matthaeus07/enhanced-bot", inline=False)
        await ctx.respond(embed = help_em)

    if music == "● Music":
        help_em = Embed(title="Music", description="Use these commands to control the music part of the bot.", color=Colour.blue())
        help_em.add_field(name="join", value="> Joins a voice channel.")
        help_em.add_field(name="play", value="> Streams music from youtube.com.")
        help_em.add_field(name="dplay", value="> Downloads and plays music from youtube.com.")
        help_em.add_field(name="stop", value="> Disconnects the bot from voice.")
        help_em.add_field(name="volume", value="> Changes the player's volume (strd: 50%).")
        await ctx.respond(embed = help_em)
    if music == "▸ join":
        help_em = Embed(title="Join", description="Joins a voice channel.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/join <voice cannel>`")
        await ctx.respond(embed = help_em)
    if music == "▸ play":
        help_em = Embed(title="Play", description="Joins and plays music that got downloaded in the author's voice channel from youtube.com.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/play <youtube url / video  name>`")
        await ctx.respond(embed = help_em)
    if music == "▸ dplay":
        help_em = Embed(title="D-Play", description="Downloads and plays music from youtube.com in high quality. The Download could take some time.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/dplay <youtube url / video  name>`")
        await ctx.repond(embed = help_em)
    if music == "▸ stop":
        help_em = Embed(title="Stop", description="Stops playing and disconnects from voice channel.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/stop`")
        await ctx.respond(embed = help_em)
    if music == "▸ volume":
        help_em = Embed(title="Volume", description="Changes the volume of the bot. (standart volume = 50)", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/volume <percentage of volume>`")
        await ctx.respond(embed = help_em)

    if fastreplies == "● FastReplies":
        help_em = Embed(title="FastReplies", description="Use these commands to let the bot reply with fast and effective answers.", color=Colour.blue())
        help_em.add_field(name="hello", value="> Greets the user.")
        help_em.add_field(name="ping", value="> Checks the bot's latency.")
        help_em.add_field(name="publish", value="> Publishes an embeded message.")
        help_em.add_field(name="color", value="> Diplays the entered hexadecimal color code.")
        help_em.add_field(name="id", value="> Displays your or the bot's id.")
        help_em.add_field(name="getid", value="> Displays user id of the mentioned user.")
        help_em.add_field(name="github", value="> Displays info about the bot's GitHub.")
        help_em.add_field(name="version", value="> Displays version info.")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ hello":
        help_em = Embed(title="Hello", description="Greets the user.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/hello <(optional) name>`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ ping":
        help_em = Embed(title="Ping", description="Checks the bot's latency.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/ping`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ publish":
        help_em = Embed(title="Publish", description="Publishes an embeded message to the channel.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/publish <heading> <message> <(optional) author> <(optional) footer> <(optional) image> <(optional) thumbnail>`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ color":
        help_em = Embed(title="Color", description="Displays an entered hexadecimal color code as a png.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/color <hex color code>`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ id":
        help_em = Embed(title="Id", description="Displays your or the bot's id.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/id`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ getid":
        help_em = Embed(title="GetId", description="Displays the id of the mentioned user.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/getid <mention user>`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ github":
        help_em = Embed(title="Github", description="Displays info about the bot's GitHub.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/github`")
        await ctx.respond(embed = help_em)
    if fastreplies == "▸ version":
        help_em = Embed(title="Version", description="Displays info about the bot's current version.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/version`")
        await ctx.respond(embed = help_em)
    
    if admin == "● Admin":
        help_em = Embed(title="Admin", description="Use these commands to administrate the server with bot.", color=Colour.blue())
        help_em.add_field(name="clear", value="> Deletes given amount of messages.")
        await ctx.respond(embed = help_em)
    if admin == "▸ clear":
        help_em = Embed(title="Clear", description="Deletes given amount of messages.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/clear <amount of messages>`")
        await ctx.respond(embed = help_em)

    if fun == "● Fun":
        help_em = Embed(title="Fun", description="Use these commands to have fun with the bot.", color=Colour.blue())
        help_em.add_field(name="roll", value="> Rolls a dice in NdN format.")
        help_em.add_field(name="roulette", value="> Play russian roulett with the bot.")
        help_em.add_field(name="mimic", value="> Mimics you.")
        help_em.add_field(name="8ball", value="> Play 8ball with an enhanced fortune teller..")
        help_em.add_field(name="vbucks", value="> Do you want V-Bucks?.")
        await ctx.respond(embed = help_em)
    if fun == "▸ roll":
        help_em = Embed(title="Roll", description="Rolls a dice in NdN format.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/roll <amount of dice>d<amount of sides>`")
        await ctx.respond(embed = help_em)
    if fun == "▸ roulette":
        help_em = Embed(title="Roulette", description="Play russian roulett with the bot. You have a 1:6 chance to loose..", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/roulette`")
        await ctx.respond(embed = help_em)
    if fun == "▸ mimic":
        help_em = Embed(title="Mimic", description="Mimics the entered words.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/mimic <something>`")
        await ctx.respond(embed = help_em)
    if fun == "▸ 8ball":
        help_em = Embed(title="8ball", description="Play 8ball with an enhanced fortune teller.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/8ball <question>`")
        await ctx.respond(embed = help_em)
    if fun == "▸ vbucks":
        help_em = Embed(title="V-Bucks", description="If you want free V-Bucks, you should use that command.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/vbucks`")
        await ctx.respond(embed = help_em)

    if maths == "● Maths":
        help_em = Embed(title="Maths", description="With these commands you can use the bot like an advanced calculator.", color=Colour.blue())
        help_em.add_field(name="add", value="> Adds the first number to the second.")
        help_em.add_field(name="sub", value="> Subtracts the 2nd number from the 1st.")
        help_em.add_field(name="mult", value="> Multiplies the first number with the second.")
        help_em.add_field(name="div", value="> Divides the 2nd number from the 1st.")
        help_em.add_field(name="pow", value="> Raises the 1st number to the powrer of the 2nd number.")
        help_em.add_field(name="root", value="> Returns the root of the entered number.")
        help_em.add_field(name="pi", value="> Displays the number pi.")
        await ctx.respond(embed = help_em)
    if maths == "▸ add":
        help_em = Embed(title="Add", description="Adds the first number to the second.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/add <number 1> <number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ sub":
        help_em = Embed(title="Sub", description="Subtracts the 2nd number from the 1st.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/sub <number 1> <number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ mult":
        help_em = Embed(title="Mult", description="Multiplies the first number with the second.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/mult <number 1> <number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ div":
        help_em = Embed(title="Div", description="Divides the 2nd number from the 1st.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/div <number 1> <number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ pow":
        help_em = Embed(title="Pow", description="Raises the 1st number to the powrer of the 2nd number.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/pow <number 1> <number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ root":
        help_em = Embed(title="Root", description="Returns the root of the entered number.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/root <number 1> <(optional) number 2>`")
        await ctx.respond(embed = help_em)
    if maths == "▸ pi":
        help_em = Embed(title="Pi", description="Displays the number pi.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/pi`")
        await ctx.respond(embed = help_em)


    if convert == "● Convert":
        help_em = Embed(title="Convert", description="Use this commands to convert stuff.", color=Colour.blue())
        help_em.add_field(name="cm_inch", value="> Converts centimeter to inch / inch to centimeter.")
        help_em.add_field(name="km_miles", value="> Converts kilometres to miles / miles to kilometres.")
        help_em.add_field(name="kmh_mph", value="> Converts kilometres per hour to miles per hour / miles per hour to kilometres per hour.")
        help_em.add_field(name="mps_kmh", value="> Converts metre per second to kilometres per hour / kilometres per hour to metre per second.")
        help_em.add_field(name="c_f", value="> Converts celsius to fahrenheit / fahrenheit to celsius.")
        help_em.add_field(name="l_gal", value="> Converts litres to galleons / galleons to litres.")
        await ctx.respond(embed = help_em)
    if convert == "▸ cm_inch":
        help_em = Embed(title="cm_inch", description="Converts centimeter to inch / inch to centimeter.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/cm_inch <number>`")
        await ctx.respond(embed = help_em)
    if convert == "▸ km_miles":
        help_em = Embed(title="km_miles", description="Converts kilometres to miles / miles to kilometres.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/km_miles <number>`")
        await ctx.respond(embed = help_em)
    if convert == "▸ kmh_mph":
        help_em = Embed(title="kmh_mph", description="Converts kilometres per hour to miles per hour / miles per hour to kilometres per hour.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/kmh_mph <number>`")
        await ctx.respond(embed = help_em)
    if convert == "▸ mps_kmh":
        help_em = Embed(title="mps_kmh", description="Converts metre per second to kilometres per hour / kilometres per hour to metre per second.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/mps_kmh <number>`")
        await ctx.respond(embed = help_em)
    if convert == "▸ c_f":
        help_em = Embed(title="c_f", description="Converts celsius to fahrenheit / fahrenheit to celsius.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/c_f <number>`")
        await ctx.respond(embed = help_em)
    if convert == "▸ l_gal":
        help_em = Embed(title="l_gal", description="Converts litres to galleons / galleons to litres.", color=Colour.blue())
        help_em.add_field(name="Usage:", value="`/l_gal <number>`")
        await ctx.respond(embed = help_em)


print("                                                                                  ")
print("  $$$$$$$$\           $$\                                                     $$\ ")
print("  $$  _____|          $$ |                                                    $$ |")
print("  $$ |      $$$$$$$\  $$$$$$$\   $$$$$$\  $$$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$$ |")
print("  $$$$$\    $$  __$$\ $$  __$$\  \____$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$ |")
print("  $$  __|   $$ |  $$ |$$ |  $$ | $$$$$$$ |$$ |  $$ |$$ /      $$$$$$$$ |$$ /  $$ |")
print("  $$ |      $$ |  $$ |$$ |  $$ |$$  __$$ |$$ |  $$ |$$ |      $$   ____|$$ |  $$ |")
print("  $$$$$$$$\ $$ |  $$ |$$ |  $$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ \$$$$$$$ |")
print("  \________|\__|  \__|\__|  \__| \_______|\__|  \__| \_______| \_______| \_______|")
print("                                                                                  ")
print("  Github: https://github.com/Matthaeus07/enhanced-bot                             ")
print("                                                                                  ")
print("                                                                                  ")

@bot.event
async def on_ready():
    # Logging the bot status
    print('\nLogged in as {0} ({0.id})'.format(bot.user))
    print('------')
    # Setting `Watching ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help for help"))

bot.run(os.getenv("TOKEN"))
