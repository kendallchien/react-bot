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