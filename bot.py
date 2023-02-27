import os
import feedparser
import discord
from discord.ext import tasks, commands
from bs4 import BeautifulSoup

# Set up the Discord bot
bot = commands.Bot(command_prefix='!')

# Read the bot token and channel ID from environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
DISCORD_CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])

# Set up the RSS feed
rss_url = 'https://frame.work/blog/feed.xml'

# Define a function to check for new posts
@tasks.loop(minutes=10)
async def check_for_new_posts():
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Get the latest post
    latest_post = feed.entries[0]

    # Check if the latest post has already been sent
    if latest_post.link != check_for_new_posts.last_post_link:
        # Save the link to the latest post
        check_for_new_posts.last_post_link = latest_post.link

        # Format the post's title, summary, and URL into a Discord message
        soup = BeautifulSoup(latest_post.summary, 'html.parser')
        summary = soup.get_text().strip()
        message = f'New post on the frame.work blog:\n\n**{latest_post.title}**\n{summary}\n{latest_post.link}'

        # Send the Discord message to the designated channel
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        await channel.send(message)

# Initialize the last_post_link attribute
check_for_new_posts.last_post_link = None

# Start the task
@bot.event
async def on_ready():
    print('Bot is ready.')
    check_for_new_posts.start()

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
