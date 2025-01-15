import discord
import time
from discord import app_commands
import discord.ext
from discord.ext import commands, tasks
import dotenv
import os
import feedparser
import psutil
# ----------------------------------------------
from database.messages.disc_messages import add_message, context_messages
from database.xp import xp_calculator, xp_to_file, xp_check
from discord_stuff.responses import test_responses
from discord_stuff.code_generator import code_generator
from duck_log.logger import logger, report_log, error_log, random_string
from duckgpt.chat_gpt_api import response_getter
# ----------------------------------------------


# Load environment variables-----
dotenv.load_dotenv()
# -------------------------------
TOKEN = os.getenv("TOKEN")
JTC_VC_ID = 1324581142757900359
OWNER_ID = 927778433856061501
SYSTEM_FEED = 1328539466029072405
REPORT_FEED = 1328539570895061093
BITRATE = 64000
# -------------------------------


# Variables ----------------------
loop_timer_hour = 1
msg_count = 0
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
start_time = f'{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}'
# --------------------------------


# Level Command ------------------------------------------------------------
@tree.command(name="level", description="Gets the user's level.")
async def level(inter: discord.Interaction, user: discord.User):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f'User: {inter.user.name} used the command "level" to get \
{user.name}\'s xp')

    xp = xp_to_file(user.id)
    xp = "{:,}".format(xp)
    await inter.response.send_message(f"{user.name} has {xp}xp", ephemeral=True)
# ---------------------------------------------------------------------------


# XP Command ---------------------------------------------------------------
@tree.command(name="vcmaker", description="Creates a private voice channel, and add one user. Use VC perms to add more.")
async def vc_maker(inter: discord.Interaction, allow_users: discord.User):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f"User: {inter.user.name} used the command 'vcmaker' to create a voice channel and allowed {allow_users.name}")

    guild = inter.guild
    channel = bot.get_channel(JTC_VC_ID)
    category = discord.utils.get(guild.categories, id=channel.category_id)
    guild = inter.guild
    user = inter.user
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True),
        allow_users: discord.PermissionOverwrite(view_channel=True)
    }

    await guild.create_voice_channel(name=f"PVC: {code_generator()}",
                                     category=category, overwrites=overwrites)

    await inter.response.send_message("Voice channel created", ephemeral=True)
# ----------------------------------------------------------------------------


# Rank Check Command ------------------------------------------------------------
#@tree.command(name="rank", description="Gets the top 5 users.")
#async def rank(inter: discord.Interaction):
#    system_messages = bot.get_channel(SYSTEM_FEED)
#    await system_messages.send(f"User: {inter.user.name} used the command 'rank' to get the top 5 users")
#
#    sorted_users = sorted(xp_to_file.items(), key=lambda x: x[1], reverse=True)
#    top_5 = sorted_users[:5]
#
#    rank_message = "Top 5 Users:\n"
#    for i, (user_id, xp) in enumerate(top_5):
#        user = await bot.fetch_user(int(user_id))
#        rank_message += f"{i + 1}. {user.name}: {xp}xp\n"
#
#    await inter.response.send_message(rank_message, ephemeral=True)
# ---------------------------------------------------------------------------


# VC Permissions Command -----------------------------------------------------
@tree.command(name="vcperms", description="Adds a user to a voice channel.")
async def vc_perms(inter: discord.Interaction, channel: discord.VoiceChannel,
                   user: discord.User):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f"User: {inter.user.name} used the command 'vcperms' on \
{channel.name} to add {user.name}")

    overwrites = channel.overwrites

    if inter.user not in channel.members:
        await inter.response.send_message("User is not in the voice channel",
                                          ephemeral=True)

    else:
        if user in overwrites:
            await inter.response.send_message("User already has permissions",
                                              ephemeral=True)

        else:
            overwrites[user] = discord.PermissionOverwrite(view_channel=True)
            await channel.edit(overwrites=overwrites)
            await inter.response.send_message(f"{user.name} was added to \
{channel.name}", ephemeral=True)
# ---------------------------------------------------------------------------


# VC Command ---------------------------------------------------------------
'''
This command was changed awhile back, now there are 2 of the
same commands with the same names, the old one wont work,
but it will still appear in the slash commands list after syncing.
That is why in the description I put "Use this one."
'''


@tree.command(name="vc", description="USE THIS ONE! Edits a voice channel.")
async def vc_editor(inter: discord.Interaction, channel: discord.VoiceChannel,
                    name: str, userlimit: int):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f"User: {inter.user.name} used the command 'vc' on \
{channel.name} to change the name to {name} and the user limit to {userlimit}")

    if inter.user not in channel.members:
        await inter.response.send_message("You must be in the voice channel \
to use this command")

    else:

        if userlimit < 0 or userlimit > 99:
            await inter.response.send_message("User limit must be between \
0 and 99 setting to 10")
            userlimit = 10
            await channel.edit(user_limit=userlimit)
            await channel.edit(name=name)
            await inter.response.send_message(f"Channel name changed to {name}\
 and user limit set to {userlimit}")

        else:
            await channel.edit(user_limit=userlimit)
            await channel.edit(name=name)
            await inter.response.send_message(f"Channel name changed to {name}\
 and user limit set to {userlimit}")
# ---------------------------------------------------------------------------


# Channel clear command -----------------------------------------------------
@tree.command(name="clear", description="Deletes the channel and \
creates a new one.")
async def clear(inter: discord.Interaction):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f"User: {inter.user.name} used the command 'clear' to delete \
and recreate the channel")

    if inter.user.id == OWNER_ID:

        channel_id = inter.channel_id
        channel = bot.get_channel(channel_id)
        overwrites = channel.overwrites

        if isinstance(channel, discord.VoiceChannel):
            await channel.delete()
            await inter.guild.create_voice_channel(name=channel.name,
                                                   overwrites=overwrites)
        else:
            await channel.delete()
            await inter.guild.create_text_channel(name=channel.name,
                                                  overwrites=overwrites)
    else:
        await inter.response.send_message("You must be @927778433856061501 \
to use this command")
# ---------------------------------------------------------------------------


# Command to test the bot ---------------------------------------------------
@tree.command(name="test", description="Performes a test.")
@app_commands.describe(message="Enter your test message")
async def test(inter: discord.Interaction, message: str) -> None:

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f"User: {inter.user.name} used the command 'test' to test \
the bot {message}")

    await inter.response.send_message(test_responses())
# ---------------------------------------------------------------------------


# Command to report ---------------------------------------------------------
@tree.command(name="report", description="report a bug, a user, or anything.")
@app_commands.describe(message="message")
async def feedback(inter: discord.Interaction, message: str) -> None:

    report = f'{random_string(8)}-{inter.user.name}\n-> {message}'
    report_messages = bot.get_channel(REPORT_FEED)

    report_log(report)
    await report_messages.send(report)
    await inter.response.send_message(f"Report submitted\nSummary\n{report}", ephemeral=True)
# ---------------------------------------------------------------------------


# Command to generate a code ------------------------------------------------
@tree.command(name="codegen", description="Generates a code.")
async def code_gen(inter: discord.Interaction):
    gen_code = code_generator()
    await inter.response.send_message(f"Code: {gen_code}", ephemeral=True)
# ---------------------------------------------------------------------------


# Command to get the bot's latency ------------------------------------------
@tree.command(name="ping", description="Gets the bot's latency.")
async def ping(inter: discord.Interaction):
    await inter.response.send_message(f"Pong!: {round(bot.latency * 1000)}ms",
                                      ephemeral=True)
# ---------------------------------------------------------------------------


# Command to sync commands --------------------------------------------------
@tree.command(name='sync', description='syncs commands')
async def sync_commands(inter: discord.Interaction):

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f'User: {inter.user.name} used the command "sync" to sync commands')

    if inter.user.id == OWNER_ID:
        await bot.change_presence(status=discord.Status.offline)

        try:
            synced_commands = await tree.sync()

            await inter.response.send_message('All synced up bitch',
                                              ephemeral=True)
            print(f'Successfully synced {len(synced_commands)} commands')

            await bot.change_presence(status=discord.Status.online)

        except Exception as e:
            error_log(f'Failed to sync commands: {e}')

    else:
        await inter.response.send_message('You must be Ducky \
to use this', ephemeral=True)
# ---------------------------------------------------------------------------


# On Ready ------------------------------------------------------------------
@bot.event
async def on_ready():
    logger(f"Bot was started {time.time()}")

    await bot.change_presence(status=discord.Status.online)

    synced_commands = await tree.sync()
    print(f'Successfully synced {len(synced_commands)} commands')

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f'Bot Started {start_time}')

    #system_usage_stats.start()
    check_empty_voice_channels.start()
    rss_feed.start()
    daily_msg_count.start()
    qlogging.start()
# ---------------------------------------------------------------------------


# On Voice ------------------------------------------------------------------
@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    channel = bot.get_channel(JTC_VC_ID)
    category = discord.utils.get(guild.categories, id=channel.category_id)

    if after.channel is not None and after.channel.id == JTC_VC_ID:

        new_channel = await guild.create_voice_channel(
            name=f"Losers: {code_generator()}",
            category=category, bitrate=BITRATE)

        await member.move_to(new_channel)

        system_messages = bot.get_channel(SYSTEM_FEED)
        await system_messages.send(f'User: {member.name} joined the JTC VC and was moved to \
{new_channel.name}.')

    else:
        pass
# ---------------------------------------------------------------------------


# System Usage --------------------------------------------------------------
@tasks.loop(hours=1)
async def system_usage_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters()
    uptime = time.time() - psutil.boot_time()

    system_messages = bot.get_channel(SYSTEM_FEED)
    await system_messages.send(f'CPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%')
    time.sleep(1)
    await system_messages.send(f'Disk Usage: {disk_usage}%\nNetwork Usage: {network_usage}\nUptime: {uptime}')

# ---------------------------------------------------------------------------


# rss feed ------------------------------------------------------------------
@tasks.loop(seconds=60)
async def rss_feed():
    feed = feedparser.parse('https://knightedgemedia.com/feed/')

    most_recent = feed.entries[0]
    link = most_recent.link

    id = most_recent.id
    if not os.path.exists('rss_feed.txt'):
        with open('rss_feed.txt', 'w') as f:
            f.write(id)
            knightedgemedia = bot.get_channel(1328212148572131390)
            await knightedgemedia.send(link)
    else:
        with open('rss_feed.txt', 'r') as f:
            last_id = f.read(-1)
            if id == last_id:
                pass
            else:
                with open('rss_feed.txt', 'w') as f:
                    f.write(id)
                    knightedgemedia = bot.get_channel(1328212148572131390)
                    await knightedgemedia.send(link)
# ---------------------------------------------------------------------------


# Check empty voice channels ------------------------------------------------
@tasks.loop(seconds=60)
async def check_empty_voice_channels():

    for guild in bot.guilds:

        for channel in guild.voice_channels:

            if channel.id == JTC_VC_ID:
                continue

            if len(channel.members) == 0:
                await channel.delete()

                vc_name = channel.name

                system_messages = bot.get_channel(SYSTEM_FEED)
                await system_messages.send(f'Empty VC: {vc_name} was deleted')
# ---------------------------------------------------------------------------


# Daily message count -------------------------------------------------------
# This function is in the process of being deprecated
@tasks.loop(hours=loop_timer_hour)
async def daily_msg_count():
    context_messages(loop_timer_hour)
# ---------------------------------------------------------------------------


# IP Logger --------------------------------------------------------------------
ip_list = ['6', '9']


@tasks.loop(seconds=20)
async def qlogging():

    if os.path.exists('logs/apache2/access.log'):

        with open('logs/apache2/access.log', 'r') as f:
            log = f.read()
            last_line = log.splitlines()[-1]

            if ip_list[-1] == last_line:
                pass
            else:
                ip_list.append(last_line)

                system_messages = bot.get_channel(SYSTEM_FEED)
                await system_messages.send(f'IP: {last_line}')
    else:
        system_messages = bot.get_channel(SYSTEM_FEED)
        await system_messages.send(f'No log file found')
# ---------------------------------------------------------------------------


# On Message ----------------------------------------------------------------
@bot.event
async def on_message(message):
    add_message(message.content, message.author.name,
                message.author.id, message.created_at)

    xp_calculator(message.content, message.author.id)

    if message.author == bot.user:
        return

    else:
        if xp_check(message.author.id, message.author.name) is True:
            xp_points = xp_to_file(message.author.id)
            xp_points = "{:,}".format(xp_points)

            await message.channel.send(f"{message.author.name} has \
{xp_points}xp")

        if "quack" in message.content.lower() or bot.user.mentioned_in(message):
            await message.reply(response_getter())
# ---------------------------------------------------------------------------


# Run the bot --------------------------------------------------------------
def run():
    if TOKEN:
        bot.run(TOKEN)
    else:
        logger("No token found")
# ---------------------------------------------------------------------------
