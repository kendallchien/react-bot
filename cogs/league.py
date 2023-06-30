import discord
from dotenv import load_dotenv
from discord.ext import commands
import helpers.riot as rt
import helpers.misc as ms


class league(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ratsignal(self, ctx, *tags , case_insensitive=True):
  
        league_role_test = '<@&1075666064349855764>'
        yahallo_guild = 83311868432617472
        bobaverse_guild = 416439957444362253
        bobaverse_league = '<@&842451431403683891>'
        hutco_guild = 102287854901669888
        hutco_league = '<@&951513678929330256>'
                        
        author_id = ctx.author.id

        if ctx.guild.id == bobaverse_guild and len(tags) == 0:
    
            emb_msg1 = '''
                konnichiwa {0}, {1} calls for aid!
            '''.format(bobaverse_league, ctx.author.mention)

        elif ctx.guild.id == hutco_guild and len(tags) == 0:

            emb_msg1 = '''
                konnichiwa {0}, {1} calls for aid!
            '''.format(hutco_league, ctx.author.mention)

        elif len(tags) == 0:

            emb_msg1 = '''
                konnichiwa! {0} calls for aid!
            '''.format(ctx.author.mention)        

        else: 

            emb_msg1 = '''
                konnichiwa {0}, {1} calls for aid!
            '''.format(', '.join(tags), ctx.author.mention)            

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
        # emb.set_footer(text=quote)

        content = ''

        view = ms.View(ctx=ctx, content=content, embed=emb_msg)

        await ctx.send(content, embed=emb, view=view)
        await view.wait()



    # @bot.event
    # async def on_raw_reaction_add(payload):
    #     '''
    #     Assign role to user on react
    #     '''
    #     message_id = payload.message_id
    #     if message_id == 927674919737761832:
    #         guild_id = payload.guild_id
    #         guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

    #         if payload.emoji.name == 'lmao':
    #             role = discord.utils.get(guild.roles, name='inferno SPOILERS')

    #         elif payload.emoji.name == 'emiya':
    #             role = discord.utils.get(guild.roles, name='spiderman SPOILERS')

    #         elif payload.emoji.name == 'janbear':
    #             role = discord.utils.get(guild.roles, name='eternals SPOILERS')            

    #         else:
    #             role = discord.utils.get(guild.roles, name=payload.emoji.name)

    #         if role is not None:
    #             member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
    #             if member is not None:
    #                 await member.add_roles(role)
    #                 print("done")
    #             else:
    #                 print("Member not found")

    #         else:
    #             print("Role not found")

    #     @bot.event
    #     async def on_raw_reaction_remove(payload):
    #         '''
    #         Remove role from user on react
    #         '''
    #         message_id = payload.message_id
    #         if message_id == 927674919737761832:
    #             guild_id = payload.guild_id
    #             guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

    #             if payload.emoji.name == 'lmao':
    #                 role = discord.utils.get(guild.roles, name='inferno SPOILERS')

    #             elif payload.emoji.name == 'emiya':
    #                 role = discord.utils.get(guild.roles, name='spiderman SPOILERS')   

    #             elif payload.emoji.name == 'janbear':
    #                 role = discord.utils.get(guild.roles, name='eternals SPOILERS')                                      

    #             else:
    #                 role = discord.utils.get(guild.roles, name=payload.emoji.name)

    #             if role is not None:
    #                 member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
    #                 if member is not None:
    #                     await member.remove_roles(role)
    #                     print("done")
    #                 else:
    #                     print("Member not found")

    #             else:
    #                 print("Role not found")


# @commands.command(pass_context=True)
# async def ratsignal(self, ctx, *tags , case_insensitive=True):
#     '''
#     Send message poll to users in channel
#     '''

#     quote = random.choice(data.get('emiya'))
#     league_of_l_role = '<@&842451431403683891>'
#     win_probability = random.randint(0, 100)
#     author_id = ctx.author.id
#     coward_users = ''
#     cnt_ready = 0
#     users = ''


#     guild_id = ctx.guild.id


#     if len(tags) != 0:
#         tags = ' '.join(map(str, tags))


#     if guild_id == 83311868432617472 and len(tags) == 0:

#         emb_msg1 = '''
#             konnichiwa {0}, {1} calls for aid!
#         '''.format(league_of_l_role, ctx.author.mention)

#     elif len(tags) == 0:

#         emb_msg1 = '''
#             konnichiwa! {1} calls for aid!
#         '''.format(league_of_l_role, ctx.author.mention)        

#     else: 

#         emb_msg1 = '''
#             konnichiwa {0}, {1} calls for aid!
#         '''.format(tags, ctx.author.mention)            

#     results = rt.get_last_game_summary(author_id)

#     if results: 

#         emb_msg2 = '''
#         *FYI the last time this person played Weeg o Wegends... they picked {0}, had **{1}** kills, **{2}** assists, **{3}** deaths, and **{4}** THE GAME...and they also placed **{5}** wards!*
        
#         '''.format(results['champion'], results['kills'], results['assists'], results['deaths'], 'WON' if results['win'] else 'LOST', results['wards'])

#         emb_msg = emb_msg1 + emb_msg2

#     else:

#         emb_msg = emb_msg1 

#     emb = discord.Embed(
#             title='RATSIGNAL', 
#             description=emb_msg, 
#             color=8388564)
#     emb.add_field(
#             name='**RAT BASTARDS** ✅:', 
#             value='---', 
#             inline=True)
#     emb.add_field(
#             name='**COWARDS** ❌:', 
#             value='---', 
#             inline=True)
#     emb.set_image(url='https://media.giphy.com/media/2y98KScHKeaQM/giphy.gif')    
#     emb.set_footer(text=quote)
    
#     msg = await ctx.channel.send('\u200b', embed=emb)    

#     await msg.add_reaction('✅') # check     
#     await msg.add_reaction('❌') # x
#     await msg.add_reaction('\U0001F987') # bat

#     # create a while loop that will wait for users to react

#     while True:
        
#         users = "" 
#         coward_users = ""

#         emojis = ['✅', '❌']

#         def check(reaction, user):
#             return (reaction.message.id == msg.id) and (user.bot != True) and (str(reaction.emoji) in emojis)

#         tasks = [
#             asyncio.create_task(
#                 bot.wait_for(
#                     'reaction_add',
#                      check = check,
#                      timeout=1800
#                  ),
#                 name='radd'
#             ),
#             asyncio.create_task(
#                 bot.wait_for(
#                     'raw_reaction_remove',
#                     check=lambda payload: str(payload.emoji) in emojis and payload.message_id == msg.id,
#                      timeout=1800
#                  ), 
#                 name='rrem'
#             )            
#         ]

#         try: 
#             done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

#             finished: asyncio.Task = list(done)[0]

#             action = finished.get_name()
#             result = finished.result()

#             msg = await ctx.channel.fetch_message(msg.id)

#             if action == 'radd':
#                 reaction, user = result
                
#                 for i, reactions in enumerate(msg.reactions):

#                     if str(reactions) == "✅":

#                         win_probability =  min(max(win_probability+ random.randint(-10,10), 0), 100)

#                         user_list = [user async for user in reactions.users() if user != bot.user]

#                         for user in set(user_list):
#                             users = users + user.mention + "\n"

#                         cnt_ready = len(user_list)

#                     elif str(reactions) == "❌":

#                         user_list = [user async for user in reactions.users() if user != bot.user]

#                         for user in set(user_list):
#                             coward_users = coward_users + user.mention + "\n"

#                         not_ready = len(user_list)

#                 if users == '':
#                     users = '---'

#                 if coward_users == '':
#                     coward_users = '---'

#                 win_url = get_win_url(win_probability)

#                 # create updated embed
#                 emb1 = discord.Embed(
#                     title='RATSIGNAL', 
#                     description=emb_msg, 
#                     color=8388564)
                
#                 emb1.set_image(url=win_url)
                
#                 emb1.add_field(
#                     name='**RAT BASTARDS** ({0}/5) ✅:'.format(str(cnt_ready)), 
#                     value='\u200b' + users, 
#                     inline=True)
                
#                 emb1.add_field(
#                     name='**COWARDS** ❌:', 
#                     value='\u200b' + coward_users, 
#                     inline=True)
                
#                 emb1.add_field(
#                     name='Win Probability: ', 
#                     value='{0}%'.format(win_probability), 
#                     inline=False)
                
#                 emb1.set_footer(text=quote)

#                 await msg.edit(embed = emb1)

#             elif action == 'rrem':

#                 for i, reactions in enumerate(msg.reactions):

#                     if str(reactions) == "✅":
#                         user_list = [user async for user in reactions.users() if user != bot.user]
                        
#                         for user in set(user_list):
#                             users = users + user.mention + "\n"

#                         cnt_ready = len(user_list)

#                     elif str(reactions) == "❌":

#                         user_list = [user async for user in reactions.users() if user != bot.user]

#                         for user in set(user_list):
#                             coward_users = coward_users + user.mention + "\n"

#                         not_ready = len(user_list)    

#                 if users == '':
#                     users = '---'

#                 if coward_users == '':
#                     coward_users = '---'                        

#                 win_url = get_win_url(win_probability)                        

#                 # create updated embed            
#                 emb1 = discord.Embed(
#                     title='RATSIGNAL', 
#                     description=emb_msg, 
#                     color=8388564)
                
#                 emb1.set_image(url=win_url)
                
#                 emb1.add_field(
#                     name='**RAT BASTARDS** ({0}/5) ✅:'.format(str(cnt_ready)), 
#                     value='\u200b' + users, 
#                     inline=True)
                
#                 emb1.add_field(
#                     name='**COWARDS** ❌:', 
#                     value='\u200b' + coward_users, 
#                     inline=True)
                
#                 emb1.add_field(
#                     name='Win Probability: ', 
#                     value='{0}%'.format(win_probability), 
#                     inline=False)
                
#                 emb1.set_footer(text=quote)

#                 await msg.edit(embed = emb1)

#         except asyncio.TimeoutError:
#             break


    @commands.command()
    async def lastgame(self, ctx, discord_user=None, n_games=1, case_insensitive=True):
        '''
        get last leg of legend game results
        '''

        # fetch puuid of member mentioned

        try:

            # if no user is mentioned, use author's ID
            if discord_user == None:
                first_member_id = ctx.author.id
                print('no author')

            # if discord_user param is passed then use mentioned user
            else:
                # discord id from discord user
                members = ctx.message.mentions
                first_member_id = members[0].id

            puuid = rt.get_most_recent_game_puuid(first_member_id)

            # print(puuid)

            # get puuid of most recent game 

            matches_df = rt.last_n_match_details_df(puuid, n_games)

            # print(matches_df)

            matches_formatted = rt.last_n_match_table(matches_df, puuid, n_games)

            # print(matches_formatted)

            msg = '''```fix
{0}
    ```'''.format(matches_formatted)

            await ctx.send(msg)

        except Exception as e:
            print(e)
            msg = '''
            ```diff
    - Are you sure you belong here?
    ```'''
            await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(league(bot))