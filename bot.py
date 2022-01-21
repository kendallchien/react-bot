import discord
import os


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 927674919737761832:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'lmao':
            role = discord.utils.get(guild.roles, name='inferno SPOILERS')

        elif payload.emoji.name == 'emiya':
            role = discord.utils.get(guild.roles, name='spiderman SPOILERS')

        elif payload.emoji.name == 'janbear':
            role = discord.utils.get(guild.roles, name='eternals SPOILERS')            

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("done")
            else:
                print("Member not found")

        else:
            print("Role not found")

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 927674919737761832:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)


        if payload.emoji.name == 'lmao':
            role = discord.utils.get(guild.roles, name='inferno SPOILERS')

        elif payload.emoji.name == 'emiya':
            role = discord.utils.get(guild.roles, name='spiderman SPOILERS')   

        elif payload.emoji.name == 'janbear':
            role = discord.utils.get(guild.roles, name='spiderman SPOILERS')                                      

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("done")
            else:
                print("Member not found")

        else:
            print("Role not found")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ratbastardsignal'):
        await message.channel.send('konichiwha @ratbastards!')

client.run(TOKEN)
