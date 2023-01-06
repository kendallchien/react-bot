from discord.ext import commands
import discord
import numpy as np
import asyncio
import random


class MyView(discord.ui.View):

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
        random_int = random.randint(0,10)
        if random_int > 2:
            self.content = self.content + '\n' + '- ⚔️ ' + interaction.user.name
        else: 
            self.content = self.content + '\n' + '- 🍆 ' + interaction.user.name
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


class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def identify(self, ctx, role: discord.Role):
        '''
        List out all users with a certain role
        '''
        role_members = []
        async for member in ctx.guild.fetch_members(limit=None):
            for member_role in member.roles:
                if member_role == role:
                    role_members.append(member.display_name)

        embed=discord.Embed(title="The following users belong to the cult of {}".format(role), description='\n'.join(role_members), color=0x109319)

        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def rename(self, ctx, member: discord.Member, nick):
        '''
        Rename users in channel
        '''
        prev = member.nick
        try:
            await member.edit(nick=nick)
            await ctx.send('***{0}*** shall henceforward be known as... **{1}**!!!'.format(prev, nick))

        except Exception as err:
            await ctx.send('Cant let you do that starfox')
            print(err)


    @commands.command()
    async def crown(self, ctx, member: discord.Member):

        crown_role = ctx.guild.get_role(1036779018785132566)
        # crown_role = ctx.guild.get_role(1036813094749483088) #test server

        if len(crown_role.members) == 0:
            content = 'there are no crowns in this land!'

        else:
            current_crown = crown_role.members[0]
            actions = ['to storm the capital', 'a mutiny', 'to usurp the throne', 'to challenge our dear leader']
            content = '{0} has proposed {1} and pass the crown from {2} to {3}'.format(ctx.author.mention, np.random.choice(actions), current_crown.mention, member.mention)

        view=MyView(ctx, content)
            
        await ctx.send(content, view=view)
        await asyncio.sleep(20) ## consider adding ability for user to extend the vote
        view.stop()
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

    @commands.command()
    async def login(self, ctx):
        await ctx.send('https://imgur.com/a/y0X2OVn')          


async def setup(bot):
    await bot.add_cog(fun(bot))