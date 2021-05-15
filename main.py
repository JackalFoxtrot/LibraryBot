import os
from discord import channel
from dotenv import load_dotenv
import discord
import asyncio
from discord.ext import commands
from discord import Color

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True
    )
load_dotenv('.env')

prefix = bot.command_prefix

titleVal = 'Default Title'
descVal = 'Description:\nDefault Description'
urlVal = ''
genreVal = 'Default Genre'
colorVal = 0x00ff00
ratingVal = 0

channelReply = -1

colors = {"fantasy" : 0x1abc9c, "sci-fi" : 0x2ecc71, 
        "mystery" : 0x9b59b6, "thriller" : 0x992d22, 
        "romance" : 0xe91e63, "western" : 0xe67e22,
        "dystopian" : 0x979c9f, "": 0x546e7a
}

def __init__(self, bot):
    self.bot = bot

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(
    name="newbook",
    description="A command that generates an embeded book",
    pass_context = True
)
async def newbook(ctx):
    await ctx.message.delete()
    
    await TitleInput(ctx, 60)
    await DescriptionInput(ctx, 300)
    await URLInput(ctx, 300)
    await GenreInput(ctx, 60)
    await RatingInput(ctx, 60)

    await embedBook(ctx)

@bot.command(
    name="setreplychannel",
    description="Sets the channel a bot will reply to instead of the message's channel",
    pass_context = True
)
async def setreplychannel(ctx):
    global titleVal
    timeWait = 300
    await ctx.message.delete()
    embed = discord.Embed(
        title='Please Enter a Channel Id',
        description='This will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            channelReply = int(msg.content)
            print("New Reply Channel: "+ str(channelReply))
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def TitleInput(ctx, timeWait):
    global titleVal
    embed = discord.Embed(
        title='Please Enter a Title',
        description='This will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            titleVal = msg.content
            print("New Book Title: "+titleVal)
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def DescriptionInput(ctx, timeWait):
    global descVal
    embed = discord.Embed(
        title='Please Enter a Description',
        description='This will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            descVal = msg.content
            print("New Book Description: "+descVal)
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def URLInput(ctx, timeWait):
    global urlVal
    embed = discord.Embed(
        title='Please Enter a URL',
        description='This will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            urlVal = msg.content
            print("New Book URL: "+urlVal)
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def GenreInput(ctx, timeWait):
    global genreVal
    embed = discord.Embed(
        title='Please Enter a Genre',
        description='Supported Genres:\nFantasy, Sci-Fi, Mystery,\nThriller, Romance, Western,\nDystopian\nThis will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            genreVal = msg.content
            print("New Book Genre: "+ genreVal)
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def RatingInput(ctx, timeWait):
    global ratingVal
    embed = discord.Embed(
        title='Please Enter a Rating',
        description='Rating Scale between 0-10\nThis will timeout after ' + str(timeWait/60.0) + ' minute(s)'
    )
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeWait,
            check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            ratingVal = msg.content
            print("New Book Rating: "+ str(ratingVal) + "/10")
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=10)

async def embedBook(message):
    global titleVal, descVal, urlVal, colorVal, genreVal, channelReply
    if not urlVal.startswith('https://'):
        urlVal = ''
    
    GenreColorSetup()
    RatingCheck()
    
    embedObj = discord.Embed(title=titleVal, description=descVal, url=urlVal, color = colorVal)
    embedObj.add_field(name='Genre', value=genreVal)
    embedObj.add_field(name='Rating', value=str(ratingVal)+"/10")

    embedObj.set_author(name = message.author.display_name, icon_url=message.author.avatar_url)
    
    if channelReply != -1:
        channel = bot.get_channel(channelReply)
        bookembed = await channel.send(embed=embedObj)
        print("Printing book to channel: " + str(channelReply))
    else:
        bookembed = await message.channel.send(embed=embedObj)
        print("Printing book to message's channel")

    await bookembed.add_reaction('❤️')
    await bookembed.add_reaction('👍')
    await bookembed.add_reaction('👎')
    await bookembed.add_reaction('💔')
    await resetValues(message)

async def resetValues(message):
    global titleVal, descVal, urlVal, genreVal, colorVal, ratingVal
    titleVal = 'Default Title'
    descVal = 'Description: \nDefault Description'
    urlVal = ''
    genreVal = 'Default Genre'
    colorVal = Color.dark_gray
    ratingVal = 0
    print("Book printed\n\n")

def GenreColorSetup():
    global colorVal, genreVal, colors
    genreTemp = genreVal.lower().split(", ")
    colorInputted = False
    for i in genreTemp:
        if not colorInputted and colors.get(i, -1) != -1:
            colorVal = colors.get(i, 0x546e7a)
            colorInputted = True
            print("Genre Detected: "+ i +"\nColor Value: "+ str(colorVal))
    if not colorInputted:        
        colorVal = 0x546e7a
        print("No Genre Detected - Color Value: "+ str(colorVal))

def RatingCheck():
    global ratingVal
    ratingTemp = int(float(ratingVal))
    if ratingTemp > 10:
        ratingTemp = 10
    if ratingTemp < 0:
        ratingTemp = 0
    ratingVal = str(ratingTemp)

bot.run(os.getenv('LIBRARYBOT_TOKEN'))