from discord.ext import commands
from discord import app_commands
import discord
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


    @app_commands.command(name='say', description="say something")
    async def say(self, interaction: discord.Interaction):
        await interaction.response.send_message(content='hello')


    @app_commands.command(name='identify', description='identify users')
    @app_commands.describe(role='put a role here')
    async def identify(self, interaction: discord.Interaction, role: discord.Role):
        '''
        List out all users with a certain role
        '''

        role_members = [member.display_name for member in interaction.guild.members if role in member.roles]

        embed=discord.Embed(title="The following users belong to the cult of {}".format(role), description='\n'.join(role_members), color=0x109319)

        await interaction.response.send_message(embed=embed, silent=True)


    @app_commands.command(name='rename', description='rename person')
    async def rename(self, interaction: discord.Interaction, person: discord.Member, new_name: str):
        '''
        Rename users in channel
        '''
        prev = person.nick
        try:
            await person.edit(nick=new_name)
            await interaction.response.send_message(f'***{prev}*** shall henceforward be known as... **{new_name}**!!!')

        except discord.Forbidden:
            await interaction.response.send_message(f"Can't let you do StarFox {person.name} is too powerful.")

        except discord.HTTPException:
            await interaction.response.send_message(f"An error occurred while trying to change the nickname.")

        except Exception as err:
            await interaction.response.send_message(f"An unexpected error occurred: {err}")


    @app_commands.command(name='reveal', description='reveal useres in channel')
    async def reveal(self, interaction: discord.Interaction):
        """
        Lists all the users in the channel where the command was sent.
        """
        # Get the text channel where the command was sent
        channel = interaction.channel

        # Get the list of members in the channel
        channel_members = [member.display_name for member in channel.members]

        if channel_members:
            # Create an embed to display the member list
            embed = discord.Embed(title=f"Members in #{channel.name}", description='\n'.join(channel_members), color=discord.Color.red())

            # Send the embed as a message
            await interaction.response.send_message(embed=embed, silent=True)
        else:
            await interaction.response.send_message("No members in the channel.")

    
    async def get_or_create_crown_role(self, ctx):

        crown_role_name = "👑"
        crown_role = discord.utils.get(ctx.guild.roles, name=crown_role_name)        

        await asyncio.sleep(1)

        if crown_role is None:
            crown_role = await ctx.guild.create_role(name=crown_role_name)

        return crown_role
                    

    @app_commands.command(name='crown', description='put a shiny hat on someone')
    async def crown(self, interaction: discord.Interaction, member: discord.Member):
        crown_role = await self.get_or_create_crown_role(interaction)

        if len(crown_role.members) == 0:
            content = 'there are no crowns in this land!'

        else:
            current_crown = crown_role.members[0]
            actions = ['to storm the capital', 'a mutiny', 'to usurp the throne', 'to challenge our dear leader']
            chosen_action = random.choice(actions)
            content = '{0} has proposed {1} and pass the crown from {2} to {3}'.format(interaction.user.mention, chosen_action, current_crown.mention, member.mention)

        view=MyView(interaction, content)
            
        await interaction.response.send_message(content, view=view)
        await asyncio.sleep(20) ## consider adding ability for user to extend the vote
        view.stop()
        await view.wait()

        if len(crown_role.members) > 0:

            if view.yes_count > view.no_count:
                await member.add_roles(crown_role)
                await current_crown.remove_roles(crown_role)
                await interaction.response.send_message.send('👑👑👑 {0} has been CROWNED...so help us all 👑👑👑'.format(member.mention))

            elif view.yes_count == view.no_count:
                await interaction.response.send_message.send('A tie... {0} retains their throne'.format(current_crown.mention))

            elif view.yes_count < view.no_count:    
                await interaction.response.send_message.send('An attempt was made by a loser, but {0} retains their throne'.format(current_crown.mention))

        else:
            if view.yes_count > view.no_count:
                await member.add_roles(crown_role)
                await interaction.response.send_message.send('👑👑👑 {0} first of their name! 👑👑👑'.format(member.mention))

            else:
                await interaction.response.send_message.send('{0} went against no one and still lost!'.format(member.mention))   

    @app_commands.command(name='login', description='get the milkshake')
    async def login(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://imgur.com/a/y0X2OVn')        


    @app_commands.command(name='xxl')
    async def enlarge(self, interaction : discord.Interaction, emoji: str):
        
        try:
            await interaction.response.send_message(discord.PartialEmoji.from_str(emoji).url)
        
        except Exception as e:
            print(f"An error occurred in the enlarger command: {e}")
            await interaction.response.send_message("An error occurred while enlarging the emoji. It's too big.")

async def setup(bot):
    await bot.add_cog(fun(bot))