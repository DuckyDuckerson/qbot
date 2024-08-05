import discord
import time
from discord import app_commands
import discord.ext
from discord.ext import commands, tasks
import dotenv
import os
# ----------------------------------------------
from database.messages.disc_messages import add_message
from database.messages.disc_messages import remove_old_data
from database.xp import xp_calculator, level_calculator, xp_check
from discord_stuff.responses import test_responses, quack_responses
from discord_stuff.code_generator import code_generator
from duck_log.logger import logger, report_log, error_log
# ----------------------------------------------


# Load environment variables-----
dotenv.load_dotenv()
# -------------------------------


user_input = input("\nWould you like to start as Production? (y/N): ")
if user_input == "y":
    GUILD_ID = 1104991679716532233
    JTC_VC_ID = 1267181492656930916
    TOKEN = os.getenv("MAIN_TOKEN")
else:
    TOKEN = os.getenv("TOKEN")
    GUILD_ID = 993318419258691635
    JTC_VC_ID = 1269409554890756157

# -------------------------------
OWNER_ID = 927778433856061501
BITRATE = 64000
# --------------------------------
# Variables ----------------------
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
# --------------------------------


@tree.command(name="level", description="Gets the user's level.")
async def level(inter: discord.Interaction, user: discord.User):
    logger(f'User: {inter.user.name} used the command "level" to get \
{user.name}\'s level')

    level = level_calculator(user.id)
    await inter.response.send_message(f"{user.name} is level {level}")


@tree.command(name="vcmaker", description="Creates a private voice channel.")
async def vc_maker(inter: discord.Interaction, allow_users: discord.User):

    logger(f'User: {inter.user.name} used the command "vcmaker" to \
create a voice channel and allowed {allow_users.name}')

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


@tree.command(name="vcperms", description="Adds a user to a voice channel.")
async def vc_perms(inter: discord.Interaction, channel: discord.VoiceChannel,
                   user: discord.User):

    logger(f'User: {inter.user.name} used the command "vcperms" on \
{channel.name} to add {user.name}')

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


@tree.command(name="vc", description="*USE THIS ONE* Edits a voice channel.")
async def vc_editor(inter: discord.Interaction, channel: discord.VoiceChannel,
                    name: str, userlimit: int):

    logger(f'User: {inter.user.name} used the command "vc" on {channel.name} \
to change the name to {name} and the user limit to {userlimit}')

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

        else:
            await channel.edit(user_limit=userlimit)
            await channel.edit(name=name)


@tree.command(name="clear", description="Deletes the channel and \
creates a new one.")
async def clear(inter: discord.Interaction):

    logger(f'User: {inter.user.name} used the command "clear" to delete \
and recreate the channel')

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
        await inter.response.send_message("You must be Ducky \
to use this command")


@tree.command(name="test", description="Performes a test.")
@app_commands.describe(message="Enter your test message")
async def test(inter: discord.Interaction, message: str) -> None:

    logger(f'User: {inter.user.name} used the command "test" to test \
the bot {message}')

    await inter.response.send_message(test_responses())


@tree.command(name="report", description="report a bug, a user, or anything.")
@app_commands.describe(message="message")
async def feedback(inter: discord.Interaction, message: str) -> None:
    report_log(f'{message}')

    await inter.response.send_message("Report submitted", ephemeral=True)


@tree.command(name="codegen", description="Generates a code.")
async def code_gen(inter: discord.Interaction):
    gen_code = code_generator()
    await inter.response.send_message(f"Code: {gen_code}", ephemeral=True)


@tree.command(name="ping", description="Gets the bot's latency.")
async def ping(inter: discord.Interaction):
    await inter.response.send_message(f"Pong!: {round(bot.latency * 1000)}ms",
                                      ephemeral=True)


@tree.command(name='sync', description='syncs commands')
async def sync_commands(inter: discord.Interaction):
    logger(f'User: {inter.user.name} used the command "sync" to sync commands')

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


@bot.event
async def on_ready():
    logger(f"Bot was started {time.time()}")

    await bot.change_presence(status=discord.Status.online)

    synced_commands = await tree.sync()
    print(f'Successfully synced {len(synced_commands)} commands')

    check_empty_voice_channels.start()


@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    channel = bot.get_channel(JTC_VC_ID)
    category = discord.utils.get(guild.categories, id=channel.category_id)

    if after.channel is not None and after.channel.id == JTC_VC_ID:

        new_channel = await guild.create_voice_channel(
            name=f"Lily Pad: {code_generator()}",
            category=category, bitrate=BITRATE)

        await member.move_to(new_channel)

        logger(f'User: {member.name} joined the JTC VC and was moved to \
{new_channel.name}')

    else:
        pass


@tasks.loop(seconds=60)
async def check_empty_voice_channels():

    for guild in bot.guilds:

        for channel in guild.voice_channels:

            if channel.id == JTC_VC_ID:
                continue

            if len(channel.members) == 0:
                await channel.delete()
                logger(f'Empty VC: {channel.name} was deleted')


@bot.event
async def on_message(message):
    remove_old_data()
    add_message(message.content, message.author.name,
                message.author.id, message.created_at)

    xp_calculator(message.content, message.author.id)

    if message.author == bot.user:
        return

    else:
        if xp_check(message.author.id, message.author.name) is True:
            level = level_calculator(message.author.id)
            await message.channel.send(f"{message.author.name} is now level \
{level}")

        if "ping" in message.content.lower():
            await message.channel.send("pong")

        if "test" in message.content.lower():
            await message.channel.send(test_responses())

        if "quack" in message.content.lower():
            await message.channel.send(quack_responses())


def run():
    if TOKEN:
        bot.run(TOKEN)
    else:
        logger("No token found")
