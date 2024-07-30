import discord
from discord.ext import commands
from discord import app_commands
import json
import os

try:
    token = open("C:/Users/alexa/OneDrive/Documents/keys/token.txt", "r").read()
    print("Successfully read token")
except Exception as e:
    print(f"Error reading token: {e}")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class Admin(app_commands.Group):
    e = None


admin = Admin(name="admin", description="Admin commands")


@bot.event
async def on_guild_join(guild: discord.Guild):
    try:
        # Gets a list of all admin ids in the guild
        admin_ids = [member.id for member in guild.members if member.guild_permissions.administrator]
        print(f"Admin ids in {guild.name}: {admin_ids}")

        # Make the directory for the new server
        if os.path.exists("./servers/" + guild.name + "/"):
            return
        os.makedirs("./servers/" + guild.name + "/")

        # Create the config.json file
        with open('./servers/' + guild.name + '/config.json', 'w') as config:
            json.dump({}, config)

        with open('./servers/' + guild.name + '/balances.json', 'w') as balances:
            json.dump({}, balances)

        # Create the owners.json file and put the list of admin ids in it
        with open('./servers/' + guild.name + '/owners.json', 'w') as owners:
            json.dump(admin_ids, owners)

    except Exception as e:
        print(f"Failed to create JSON files for {guild.name}: {e}")




@bot.event
async def on_ready(guild: discord.Guild):
    print("Bot is ready!")
    bot.tree.add_command(admin)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    member_ids = [member.id for member in guild.members if not member.bot]
    balances_dict = {member_id: 0 for member_id in member_ids}
    with open('./servers/' + guild.name + '/balances.json', 'w') as balances:
        json.dump(balances_dict, balances)


@bot.tree.command(name="hello", description="Says hello.")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! How are you doing?", ephemeral=False)
    print(f"{interaction.user.name} used the hello command")


@bot.tree.command(name="say", description="Says something that you put in.")
@app_commands.describe(thing="What should I say?")
async def say(interaction: discord.Interaction, thing: str):
    await interaction.response.send_message(f"{interaction.user.display_name} said: `{thing}`")
    print(f"{interaction.user.name} used the say command. Said: \"{thing}\"")


@bot.tree.command(name="pinganyone", description="Pings anyone you choose.")
@app_commands.describe(user="Who should I ping?")
async def ping(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(user.mention)
    print(f"{interaction.user.name} used the pinganyone command. Pinged \"{user.display_name}\"")


@admin.command(name="chnagename", description="Placeholder, chnages the name in the JSON file.")
@app_commands.describe(name="What should I change the name to?")
async def change_name(interaction: discord.Interaction, name: str):
    with open("info.json", "r+") as f:
        try:
            data = json.load(f)
            data["name"] = "" + name + ""
        except Exception as e:
            print(e)
            data = {"name": "unknown"}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    await interaction.response.send_message(f"Name changed to `{name}`")
    print(f"{interaction.user.name} used the chnagename command. Changed to \"{name}\"")


print("bot is about to run (trust)")
bot.run(token)
