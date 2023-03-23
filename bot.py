import os
import feedparser
import discord
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default() # or .all() if you ticked all, that is easier
intents.message_content  = True # If you ticked the SERVER MEMBERS INTENT

# Set up the Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Read the bot token from environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

# Set up the RSS feed
rss_url = 'https://frame.work/blog.rss'

JSON_FILEPATH="data/subscribed_channels.json"


# Initialize the subscribed_channels dictionary
subscribed_channels = {}

# Define a function to check for new posts
@tasks.loop(minutes=10)
async def check_for_new_posts():
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    if len(feed.entries) <= 0:
        logging.info("feed contains no items")
    else:
        # Get the latest post
        latest_post = feed.entries[0]
        logging.info("Found post: " + str(latest_post))


        # Check if the latest post has already been sent
        if latest_post.id != check_for_new_posts.last_post_id:
            # Save the ID of the latest post
            check_for_new_posts.last_post_id = latest_post.id

            # Format the post's title, summary, and URL into a Discord message
            soup = BeautifulSoup(latest_post.summary, 'html.parser')
            summary = soup.get_text().strip()
            message = f'New post on the frame.work blog:\n\n**{latest_post.title}**\n{summary}\n{latest_post.link}'

            # Send the Discord message to all subscribed channels
            for channel_id in subscribed_channels.values():
                channel = bot.get_channel(channel_id)
                await channel.send(message)


# Initialize the last_post_id attribute
check_for_new_posts.last_post_id = None

# Define a subscribe command that adds the current channel to the subscribed_channels dictionary
@bot.command()
@commands.has_permissions(administrator=True)
async def subscribe(ctx):
    server_id = ctx.guild.id
    subscribed_channels[server_id] = ctx.channel.id
    await ctx.send('This channel has been subscribed to the frame.work blog feed.')
    save_subscribed_channels()

# Define a subscribe command that adds the current channel to the subscribed_channels dictionary
@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/MoralCode/framework-discord-feed")

# Define an unsubscribe command that removes the current channel from the subscribed_channels dictionary
@bot.command()
@commands.has_permissions(administrator=True)
async def unsubscribe(ctx):
    server_id = ctx.guild.id
    if server_id in subscribed_channels:
        del subscribed_channels[server_id]
        await ctx.send('This channel has been unsubscribed from the frame.work blog feed.')
        save_subscribed_channels()
    else:
        await ctx.send('This channel is not currently subscribed to the frame.work blog feed.')

# Start the task
@bot.event
async def on_ready():
    print('Bot is ready.')
        # Load the subscribed_channels dictionary from a file
    subscribed_channels = load_subscribed_channels()

    # Start the check_for_new_posts loop
    check_for_new_posts.start()

# Define a function to save the subscribed_channels dictionary to a file
def save_subscribed_channels():
    with open(JSON_FILEPATH, 'w') as f:
        json.dump(subscribed_channels, f)

# Define a function to load the subscribed_channels dictionary from a file
def load_subscribed_channels():
    try:
        with open(JSON_FILEPATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Run the bot
bot.run(DISCORD_BOT_TOKEN)
