from discord.ext import commands
import discord
import asyncio
import random
import requests


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
        random_int = random.randint(0,10)
        if random_int > 2:
            self.content = self.content + '\n' + '- ⚔️ ' + interaction.user.display_name
        else: 
            self.content = self.content + '\n' + '- 🍆 ' + interaction.user.display_name
        await interaction.response.edit_message(content = self.content, view=self)
        
    @discord.ui.button(label="No!", style=discord.ButtonStyle.red, custom_id="danger")
    async def no_button_callback(self, interaction, button):
        self.no_count += 1 
        button.label = "No: {}".format(self.no_count)
        self.content = self.content + '\n' + '- 🛡️ ' + interaction.user.display_name
        await interaction.response.edit_message(content = self.content, view=self)
        
    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
                child.style = discord.ButtonStyle.grey
        self.stop()
        await self.wait()


class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def identify(self, ctx, role: discord.Role):
        '''
        List out all users with a certain role
        '''
        # role_members = []
        # async for member in ctx.guild.fetch_members(limit=None):
        #     for member_role in member.roles:
        #         if member_role == role:
        #             role_members.append(member.display_name)

        role_members = [member.display_name for member in ctx.guild.members if role in member.roles]

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
            await ctx.send(f'***{prev}*** shall henceforward be known as... **{nick}**!!!')

        except discord.Forbidden:
            await ctx.send(f"Can't let you do StarFox {member.name} is too powerful.")

        except discord.HTTPException:
            await ctx.send(f"An error occurred while trying to change the nickname.")

        except Exception as err:
            await ctx.send(f"An unexpected error occurred: {err}")


    @commands.command()
    async def showyourself(self, ctx):
        """
        Lists all the users in the channel where the command was sent.
        """
        # Get the text channel where the command was sent
        channel = ctx.channel

        # Get the list of members in the channel
        channel_members = [member.display_name for member in channel.members]

        if channel_members:
            # Create an embed to display the member list
            embed = discord.Embed(title=f"Members in #{channel.name}", description='\n'.join(channel_members), color=discord.Color.red())

            # Send the embed as a message
            await ctx.send(embed=embed)
        else:
            await ctx.send("No members in the channel.")

    
    async def get_or_create_crown_role(self, ctx):

        crown_role_name = "👑"
        crown_role = discord.utils.get(ctx.guild.roles, name=crown_role_name)        

        await asyncio.sleep(1)

        if crown_role is None:
            crown_role = await ctx.guild.create_role(name=crown_role_name)

        return crown_role
                    

    @commands.command()
    async def crown(self, ctx, member: discord.Member):
        crown_role = await self.get_or_create_crown_role(ctx)

        if len(crown_role.members) == 0:
            content = 'there are no crowns in this land!'

        else:
            current_crown = crown_role.members[0]
            actions = ['to storm the capital', 'a mutiny', 'to usurp the throne', 'to challenge our dear leader']
            chosen_action = random.choice(actions)
            content = '{0} has proposed {1} and pass the crown from {2} to {3}'.format(ctx.author.mention, chosen_action, current_crown.mention, member.mention)

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


    @commands.command()
    async def enlarger(self, ctx, emoji: discord.PartialEmoji):
        
        try:
            await ctx.send(emoji.url)
        
        except Exception as e:
            print(f"An error occurred in the enlarger command: {e}")
            await ctx.send("An error occurred while enlarging the emoji It's too big.")


async def setup(bot):
    await bot.add_cog(fun(bot))