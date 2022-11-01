import discord
import numpy as np
import os
import asyncio
import random
import yaml
import time
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
import riot as rt
import pandas as pd

with open('img.yaml') as f:

    data = yaml.load(f, Loader=yaml.FullLoader)

# LOAD .ENV FILE
load_dotenv()

# GRAB API TOKEN FROM .ENV
TOKEN = os.getenv('DISCORD_TOKEN')
# TOKEN = os.getenv('DISCORD_TOKEN_TEST')
# GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


# SET BOT COMMAND PREFIX
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # for guild in bot.guilds:
    #         if guild.name == GUILD:
    #             break

    print('We have logged in as {0.user}'.format(bot))
    # print('Joining {0.id}'.format(guild))

@bot.event
async def on_raw_reaction_add(payload):
    '''
    Assign role to user on react
    '''
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
    '''
    Remove role from user on react
    '''
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


def get_win_url(win_probability):
    '''
    Return link based on win probability 
    '''
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

    return win_url


@bot.command(pass_context=True)
async def ratsignal(ctx, *tags , case_insensitive=True):
    '''
    Send message poll to users in channel
    '''


    quote = random.choice(data.get('emiya'))
    league_of_l_role = '<@&842451431403683891>'
    win_probability = random.randint(0, 100)
    author_id = ctx.author.id
    coward_users = ''
    cnt_ready = 0
    users = ''


    guild_id = ctx.guild.id


    if len(tags) != 0:
        tags = ' '.join(map(str, tags))


    if guild_id == 83311868432617472 and len(tags) == 0:

        emb_msg1 = '''
            konnichiwa {0}, {1} calls for aid!
        '''.format(league_of_l_role, ctx.author.mention)

    elif len(tags) == 0:

        emb_msg1 = '''
            konnichiwa! {1} calls for aid!
        '''.format(league_of_l_role, ctx.author.mention)        

    else: 

        emb_msg1 = '''
            konnichiwa {0}, {1} calls for aid!
        '''.format(tags, ctx.author.mention)            

    results = rt.get_last_game_summary(author_id)

    if results: 

        emb_msg2 = '''
        *FYI the last time this person played Weeg o Wegends... they picked {0}, had **{1}** kills, **{2}** assists, **{3}** deaths, and **{4}** THE GAME...and they also placed **{5}** wards!*
        
        '''.format(results['champion'], results['kills'], results['assists'], results['deaths'], 'WON' if results['win'] else 'LOST', results['wards'])

        emb_msg = emb_msg1 + emb_msg2

    else:

        emb_msg = emb_msg1 

    emb = discord.Embed(
            title='RATSIGNAL', 
            description=emb_msg, 
            color=8388564)
    emb.add_field(
            name='**RAT BASTARDS** ✅:', 
            value='---', 
            inline=True)
    emb.add_field(
            name='**COWARDS** ❌:', 
            value='---', 
            inline=True)
    emb.set_image(url='https://media.giphy.com/media/2y98KScHKeaQM/giphy.gif')    
    emb.set_footer(text=quote)
    
    msg = await ctx.channel.send('\u200b', embed=emb)    

    await msg.add_reaction('✅') # check     
    await msg.add_reaction('❌') # x
    await msg.add_reaction('\U0001F987') # bat

    # create a while loop that will wait for users to react

    while True:
        
        users = "" 
        coward_users = ""

        emojis = ['✅', '❌']

        def check(reaction, user):
            return (reaction.message.id == msg.id) and (user.bot != True) and (str(reaction.emoji) in emojis)

        tasks = [
            asyncio.create_task(
                bot.wait_for(
                    'reaction_add',
                     check = check,
                     timeout=1800
                 ),
                name='radd'
            ),
            asyncio.create_task(
                bot.wait_for(
                    'raw_reaction_remove',
                    check=lambda payload: str(payload.emoji) in emojis and payload.message_id == msg.id,
                     timeout=1800
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

                    if str(reactions) == "✅":

                        win_probability =  min(max(win_probability+ random.randint(-10,10), 0), 100)

                        user_list = [user async for user in reactions.users() if user != bot.user]

                        for user in set(user_list):
                            users = users + user.mention + "\n"

                        cnt_ready = len(user_list)

                    elif str(reactions) == "❌":

                        user_list = [user async for user in reactions.users() if user != bot.user]

                        for user in set(user_list):
                            coward_users = coward_users + user.mention + "\n"

                        not_ready = len(user_list)

                if users == '':
                    users = '---'

                if coward_users == '':
                    coward_users = '---'

                win_url = get_win_url(win_probability)

                # create updated embed
                emb1 = discord.Embed(
                    title='RATSIGNAL', 
                    description=emb_msg, 
                    color=8388564)
                
                emb1.set_image(url=win_url)
                
                emb1.add_field(
                    name='**RAT BASTARDS** ({0}/5) ✅:'.format(str(cnt_ready)), 
                    value='\u200b' + users, 
                    inline=True)
                
                emb1.add_field(
                    name='**COWARDS** ❌:', 
                    value='\u200b' + coward_users, 
                    inline=True)
                
                emb1.add_field(
                    name='Win Probability: ', 
                    value='{0}%'.format(win_probability), 
                    inline=False)
                
                emb1.set_footer(text=quote)

                await msg.edit(embed = emb1)

            elif action == 'rrem':

                for i, reactions in enumerate(msg.reactions):

                    if str(reactions) == "✅":
                        user_list = [user async for user in reactions.users() if user != bot.user]
                        
                        for user in set(user_list):
                            users = users + user.mention + "\n"

                        cnt_ready = len(user_list)

                    elif str(reactions) == "❌":

                        user_list = [user async for user in reactions.users() if user != bot.user]

                        for user in set(user_list):
                            coward_users = coward_users + user.mention + "\n"

                        not_ready = len(user_list)    

                if users == '':
                    users = '---'

                if coward_users == '':
                    coward_users = '---'                        

                win_url = get_win_url(win_probability)                        

                # create updated embed            
                emb1 = discord.Embed(
                    title='RATSIGNAL', 
                    description=emb_msg, 
                    color=8388564)
                
                emb1.set_image(url=win_url)
                
                emb1.add_field(
                    name='**RAT BASTARDS** ({0}/5) ✅:'.format(str(cnt_ready)), 
                    value='\u200b' + users, 
                    inline=True)
                
                emb1.add_field(
                    name='**COWARDS** ❌:', 
                    value='\u200b' + coward_users, 
                    inline=True)
                
                emb1.add_field(
                    name='Win Probability: ', 
                    value='{0}%'.format(win_probability), 
                    inline=False)
                
                emb1.set_footer(text=quote)

                await msg.edit(embed = emb1)

        except asyncio.TimeoutError:
            break


@bot.command(pass_context=True)
async def rename(ctx, member: discord.Member, nick):
    '''
    Rename users in channel
    '''
    prev = member.nick
    try:
        await member.edit(nick=nick)
        await ctx.send('***{0}*** shall henceforward be known as... **{1}**!!!'.format(prev, nick))

    except Exception as err:
        await ctx.send('Cant let you do that starfox')
        # ctx.send('Unexpected {0}. {1}'.format(err, type(err)))

    # except HTTPException as err:
    #     ctx.send('Unexpected {0}. {1}'.format(err, type(err)))        

    # except TypeError as err:
    #     ctx.send('Unexpected {0}. {1}'.format(err, type(err)))        

    # await ctx.send(f'Nickname was changed for {member.mention}')

@bot.command()
async def identify(ctx, role: discord.Role):
    role_members = []
    async for member in ctx.guild.fetch_members(limit=None):
        for member_role in member.roles:
            if member_role == role:
                role_members.append(member.display_name)

    embed=discord.Embed(title="The following users belong to the cult of {}".format(role), description='\n'.join(role_members), color=0x109319)
    # embed.add_field(value='\n'.join(role_members), inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def louvre(ctx, case_insensitive=True):
    '''
    Randomly message channel with an image from louvre channel
    '''

    channel = bot.get_channel(636799254152871936)
    # channel = bot.get_channel(934888003367764028)

    allmsg = []

    async for msg in channel.history(limit=1000):
        if hasattr(msg, 'attachments'):
            if len(msg.attachments) > 0:
                allmsg.append(msg)

    random_msg = random.choice(allmsg)

    emb = discord.Embed(title='A gift from the Louvre', color=8388564)
    # emb.add_field(name='Curator', value=random_msg.author.mention)
    # emb.add_field(name='Circa', value=random_msg.created_at.strftime('%Y-%m-%d'))
    
    emb.set_image(url=random_msg.attachments[0].url)
    emb.set_footer(text='Curated by: {0}, circa {1}'.format(random_msg.author.name, random_msg.created_at.strftime('%Y-%m-%d')))
    

    await ctx.send(
        random_msg.content,
        embed=emb
        )


@bot.command()
async def lastgame(ctx, discord_user=None, case_insensitive=True):
    '''
    get last leg of legend game results
    '''
    try:

        if discord_user == None:
            first_member_id = ctx.author.id

        else:
            # discord id from discord user
            members = ctx.message.mentions
            first_member_id = members[0].id

        puuid = rt.get_most_recent_game_puuid(first_member_id)

        # get puuid of most recent game 

        last_game_summary = rt.get_matches(puuid)

        msg = '''
```fix
{0}

```
        '''.format(last_game_summary)


        await ctx.send(msg)

    except Exception as e:
        print(e)
        msg = '''
        ```diff
- Are you sure you belong here?
```'''
        await ctx.send(msg)

    # get puuid from discord user name

    # get last game if multiple aliases 

    # return details of last game 


# class GreenButton(Button):
#     def __init__(self, label):
#         super().__init__(label=label, style=discord.ButtonStyle.green)

#     async def callback(self, interaction):
#         nonlocal yes_counter
#         yes_counter +=1
#         await interaction.response.edit_message(content="Touched Me! yes: {0} no: {1}".format(yes_counter, no_counter))

# class RedButton(Button):
#     def __init__(self, label):
#         super().__init__(label=label, style=discord.ButtonStyle.green)

#     async def callback(self, interaction):
#         nonlocal yes_counter
#         yes_counter +=1
#         await interaction.response.edit_message(content="Touched Me! yes: {0} no: {1}".format(yes_counter, no_counter))



    emb = discord.Embed(
            title='RATSIGNAL', 
            description='hi', 
            color=8388564)
    emb.add_field(
            name='✅:', 
            value='---', 
            inline=True)
    emb.add_field(
            name='❌:', 
            value='---', 
            inline=True)


class MyView(View):

    def __init__(self, ctx, content):
        super().__init__(timeout=15)
        self.ctx = ctx
        self.content = content 
        self.yes_count = 0
        self.no_count = 0

    @discord.ui.button(label="Yes!", style=discord.ButtonStyle.green)
    async def yes_button_callback(self, interaction, button):  
        self.yes_count += 1 
        button.label = "Yes: {}".format(self.yes_count)
        # await interaction.response.send_message('{} aids the usurper'.format(self.ctx.author.mention))
        self.content = self.content + '\n' + '- ⚔️ ' + interaction.user.name
        await interaction.response.edit_message(content = self.content, view=self)
        
    @discord.ui.button(label="No!", style=discord.ButtonStyle.red, custom_id="danger")
    async def no_button_callback(self, interaction, button):
        self.no_count += 1 
        button.label = "No: {}".format(self.no_count)
        self.content = self.content + '\n' + '- 🛡️ ' + interaction.user.name
        # await interaction.response.send_message('{} cowers in fear'.format(self.ctx.author.mention))        
        await interaction.response.edit_message(content = self.content, view=self)
        
    async def on_timeout(self) -> None:
        await self.ctx.send("Times up!")
        return 

@bot.command()
async def crown(ctx, member: discord.Member):

    crown_role = ctx.guild.get_role(1036779018785132566) -- yahallo
    # crown_role = ctx.guild.get_role(1036813094749483088)

    if len(crown_role.members) == 0:
        content = 'there are no crowns in this land!'

    else:
        current_crown = crown_role.members[0]
        actions = ['to storm the capital', 'a mutiny', 'to usurp the throne']
        content = '{0} has proposed {1} and pass the crown from {2} to {3}'.format(ctx.author.mention, np.random.choice(actions), current_crown.mention, member.mention)

    view = MyView(ctx, content)
    await ctx.send(content, view=view)
    await view.wait()


    if len(crown_role.members) > 0:

        if view.yes_count > view.no_count:
            await member.add_roles(crown_role)
            await current_crown.remove_roles(crown_role)
            await ctx.send('👑👑👑 {0} has been CROWNED...so help us all 👑👑👑'.format(member.mention))

        elif view.yes_count == view.no_count:
            await ctx.send('A tie... {0} retains their throne'.format(current_crown.mention))

        elif view.yes_count < view.no_count:    
            await ctx.send('An attempt was made by a loser, but {0} retains their throne'.format(current_crown.mention))

    else:
        if view.yes_count > view.no_count:
            await member.add_roles(crown_role)
            await ctx.send('👑👑👑 {0} first of their name! 👑👑👑'.format(member.mention))

        else:
            await ctx.send('{0} went against no one and still lost!'.format(member.mention))            


bot.run(TOKEN)
