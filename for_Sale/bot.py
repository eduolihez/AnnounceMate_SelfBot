import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
import colorama
from tabulate import tabulate
from colorama import Fore, Style

# Configure your Discord bot token
TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Load configuration from config.json file
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Load announcement messages from announcement_messages.json file
with open('announcement_messages.json', 'r', encoding='utf-8') as messages_file:
    announcement_messages = json.load(messages_file)

# Load announcement channel IDs from announcement_channel_ids.json file
with open('announcement_channel_ids.json', 'r', encoding='utf-8') as channels_file:
    announcement_channel_ids = json.load(channels_file)

# Configure the interval between each announcement (in seconds)
announcement_interval_min = config['announcement_interval_min']
announcement_interval_max = config['announcement_interval_max']

# Initialize colorama
colorama.init()

bot = commands.Bot(command_prefix='$')


def display_records(records):
    headers = [f"{Fore.CYAN}Channel{Style.RESET_ALL}",
               f"{Fore.CYAN}Status{Style.RESET_ALL}"]
    records_table = []

    for channel_id, status in records.items():
        channel = bot.get_channel(channel_id)
        records_table.append([channel.name, status])

    print(tabulate(records_table, headers=headers))


@bot.event
async def on_ready():
    print('Waiting for the bot to be ready...')
    print('The bot is ready')

    channel_records = {}

    # Check if messages can be sent in all channels
    for channel_id in announcement_channel_ids:
        channel = bot.get_channel(channel_id)

        if not channel.permissions_for(channel.guild.me).send_messages:
            channel_records[channel_id] = f"{Fore.RED}Cannot send messages"
        else:
            channel_records[channel_id] = f"{Fore.GREEN}Can send messages"

    display_records(channel_records)

    await send_announcement_loop()


async def check_permissions():
    for channel_id in announcement_channel_ids:
        announcement_channel = bot.get_channel(channel_id)
        if announcement_channel.permissions_for(announcement_channel.guild.me).send_messages:
            print(
                f'{Fore.GREEN}Can send messages in channel: {announcement_channel.name}{Style.RESET_ALL}')
        else:
            print(
                f'{Fore.YELLOW}Cannot send messages in channel: {announcement_channel.name}{Style.RESET_ALL}')
            announcement_channel_ids.remove(channel_id)
            print(
                f'{Fore.RED}Removed channel ID: {channel_id} from announcement_channel_ids.json{Style.RESET_ALL}')

    with open('announcement_channel_ids.json', 'w', encoding='utf-8') as channels_file:
        json.dump(announcement_channel_ids, channels_file, indent=4)


@tasks.loop(seconds=random.randint(announcement_interval_min, announcement_interval_max))
async def send_announcement_loop():
    if len(announcement_channel_ids) == 0:
        print(
            f'{Fore.YELLOW}No available channels to send announcements at the moment.{Style.RESET_ALL}')
        return

    for channel_id in announcement_channel_ids:
        announcement_channel = bot.get_channel(channel_id)

        try:
            if announcement_channel.permissions_for(announcement_channel.guild.me).send_messages:
                announcement_message = random.choice(announcement_messages)
                message = announcement_message['message']
                attached_images = []

                if announcement_message['attach_images']:
                    for image_path in config['image_paths']:
                        with open(image_path, 'rb') as image_file:
                            attached_image = discord.File(image_file)
                            attached_images.append(attached_image)

                await announcement_channel.send(content=message, files=attached_images)
                print(
                    f'{Fore.CYAN}Message sent in channel: {announcement_channel.name}{Style.RESET_ALL}')
            else:
                print(
                    f'{Fore.YELLOW}Cannot send messages in channel: {announcement_channel.name} - Skipping...{Style.RESET_ALL}')
                continue
        except discord.Forbidden:
            print(
                f'{Fore.RED}No permissions to send messages in channel: {announcement_channel.name} - Skipping...{Style.RESET_ALL}')
            continue
        except Exception as e:
            print(
                f'{Fore.RED}Error sending message in channel: {announcement_channel.name} - {e}{Style.RESET_ALL}')
            continue


@bot.command()
async def start(ctx):
    if send_announcement_loop.is_running():
        await ctx.send('The bot is already running.')
    else:
        send_announcement_loop.start()
        await ctx.send('The bot has started sending announcements.')


@bot.command()
async def stop(ctx):
    if send_announcement_loop.is_running():
        send_announcement_loop.cancel()
        await ctx.send('The bot has been stopped.')
    else:
        await ctx.send('The bot is not running.')


@bot.command()
async def status(ctx):
    channel_records = {}

    for channel_id in announcement_channel_ids:
        channel = bot.get_channel(channel_id)

        if not channel.permissions_for(channel.guild.me).send_messages:
            channel_records[channel_id] = f"{Fore.RED}Cannot send messages"
        else:
            channel_records[channel_id] = f"{Fore.GREEN}Can send messages"

    display_records(channel_records)


bot.run(TOKEN, bot=False)
