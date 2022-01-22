import discord
import os
import asyncio
import random
import yaml
from dotenv import load_dotenv
from discord.ext import commands

with open('img.yaml') as f:
    
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)


# LOAD .ENV FILE
load_dotenv()

# GRAB API TOKEN FROM .ENV
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

# SET BOT COMMAND PREFIX
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    # for guild in bot.guilds:
    #         if guild.name == GUILD:
    #             break

    print('We have logged in as {0.user}'.format(bot))
    # print('Joining {0.id}'.format(guild))

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 927674919737761832:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

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

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 927674919737761832:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)


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
                await member.remove_roles(role)
                print("done")
            else:
                print("Member not found")

        else:
            print("Role not found")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('!ratbastards'):
#         msg = await message.channel.send("""konichiwha @ratbastards!
#             @{0.author} cals for aid!
#             """.format(message))
#         print(msg)

#     if message.content == '!ratbastardsignal':
#         await message.add_reaction('\U0001F987')

#     await bot.process_commands(message)

# rat signal 
@bot.command(pass_context=True)
async def ratsignal(ctx):

    emb_msg = '''
        konichiwha you @ratbastards! {0} calls for aid!
    '''.format(ctx.author.mention)
    
    emb = discord.Embed(title='RATSIGNAL', description=emb_msg, color=16769251)
    # emb.set_thumbnail(url='https://www.anime-planet.com/images/characters/3799.jpg?t=1615919953')
    emb.set_image(url='https://www.anime-planet.com/images/characters/3799.jpg?t=1615919953')

    emb.add_field(name='Ready', value='---', inline=True)
    emb.add_field(name='Not Ready: ', value='---', inline=True)
    emb.add_field(name='Rat Bastards: ', value='HERE ALL USERS WITH ✅', inline=False)


    msg = await ctx.channel.send(embed=emb)    
    # msg = await ctx.channel.send("""konichiwha @ratbastards!
    #     {0} cals for aid!
    #     """.format(ctx.author.mention))
    await msg.add_reaction('✅') # check     
    await msg.add_reaction('❌') # x
    await msg.add_reaction('\U0001F987') # bat


    # create a while loop that will wait for users to react

    # not_ready = 0
    # cnt_ready = 0    

    while True:
        
        users = "" 
        win_probability = random.randint(0, 100)

        if win_probability <= 10:
            win_url = data.get('img').get('img1').get('link')

        elif win_probability <= 20:
            win_url = data.get('img').get('img2').get('link')

        elif win_probability <= 30:
            win_url = data.get('img').get('img3').get('link')                        

        elif win_probability <= 40:
            win_url = data.get('img').get('img4').get('link')

        elif win_probability <= 50:
            win_url = data.get('img').get('img5').get('link')                                                

        elif win_probability <= 60:
            win_url = data.get('img').get('img6').get('link')

        elif win_probability <= 70:
            win_url = data.get('img').get('img7').get('link')

        elif win_probability <= 80:
            win_url = data.get('img').get('img8').get('link')                        

        elif win_probability <= 90:
            win_url = data.get('img').get('img9').get('link')

        elif win_probability <= 100:
            win_url = data.get('img').get('img10').get('link')


        tasks = [
            asyncio.create_task(
                bot.wait_for(
                    'reaction_add',
                     check=lambda reaction, user: reaction.emoji == "✅",
                     timeout=600
                 ), 
                name='radd'
            ),
            asyncio.create_task(
                bot.wait_for(
                    'raw_reaction_remove',
                     timeout=600,
                     check=lambda payload: str(payload.emoji) == "✅" and payload.message_id == msg.id
                 ), 
                name='rrem'
            )            
        ]

        try: 
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            finished: asyncio.Task = list(done)[0]

            action = finished.get_name()
            result = finished.result()

            msg = await ctx.channel.fetch_message(msg.id)

            if action == 'radd':
                reaction, user = result
                
                for i, reactions in enumerate(msg.reactions):
                    print("----add loop '{0}', {1}".format(i, reactions))

                    if str(reactions) == "✅":

                        user_list = [user async for user in reactions.users() if user != bot.user]

                        for user in set(user_list):
                            users = users + user.mention + "\n"

                        cnt_ready = len(user_list)

                # create updated embed
                emb1 = discord.Embed(title='RATSIGNAL', description=emb_msg, color=16769251)
                # emb.set_thumbnail(url='https://www.anime-planet.com/images/characters/3799.jpg?t=1615919953')
                emb1.set_image(url=win_url)
                emb1.add_field(name='Ready', value='({0}/5)'.format(str(cnt_ready)), inline=True)
                emb1.add_field(name='Not Ready: ', value='---', inline=True)
                # emb1.add_field(name='Not Ready', value='({0}/5)'.format(str(not_ready)), inline=True)
                emb1.add_field(name='Rat Bastards: ', value='HERE ALL USERS WITH ✅ \n' + users, inline=False)
                emb1.add_field(name='Win Probability: ', value='{0}%'.format(win_probability), inline=False)

                await msg.edit(embed = emb1)      


            elif action == 'rrem':

                for i, reactions in enumerate(msg.reactions):
                    print("-----remove loop '{0}', {1}".format(i, reactions))

                    if str(reactions) == "✅":
                        user_list = [user async for user in reactions.users() if user != bot.user]
                        
                        for user in set(user_list):
                            users = users + user.mention + "\n"

                        cnt_ready = len(user_list)

                emb1 = discord.Embed(title='RATSIGNAL', description=emb_msg, color=16769251)
                # emb.set_thumbnail(url='https://www.anime-planet.com/images/characters/3799.jpg?t=1615919953')
                emb1.set_image(url=win_url)
                emb1.add_field(name='Ready', value='({0}/5)'.format(str(cnt_ready)), inline=True)
                emb1.add_field(name='Not Ready: ', value='---', inline=True)
                # emb1.add_field(name='Not Ready', value='({0}/5)'.format(str(not_ready)), inline=True)
                emb1.add_field(name='Rat Bastards: ', value='HERE ALL USERS WITH ✅ \n' + users, inline=False)
                emb1.add_field(name='Win Probability: ', value='{0}%'.format(win_probability), inline=False)

                await msg.edit(embed = emb1)

        except asyncio.TimeoutError:
            break



@bot.command(pass_context=True)
async def rename(ctx, member: discord.Member, nick):
    prev = member.nick
    await member.edit(nick=nick)
    await ctx.send('{0} shall henceforward be known as... {1}!!!'.format(prev, nick))
    # await ctx.send(f'Nickname was changed for {member.mention}')

@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")

bot.run(TOKEN)
