import discord
from discord import app_commands
import random
from discord.ext import commands


class louvre(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 636799254152871936
        self.allowed_guild_ids = [83311868432617472, 873243765157032026]

    async def fetch_random_message(self):
        channel = self.bot.get_channel(self.channel_id)

        if channel is None:
            print(f"Channel with ID {self.channel_id} not found")

        messages = []
        try:
            async for message in channel.history():
                if message.attachments:
                    messages.append(message)
        
        except Exception as e:
            print(f"An error occured while fetching messages")
            return None
        
        return random.choice(messages) if messages else None

    @app_commands.command(name='louvre', description='extract the greatest treasures')
    async def louvre(self, interaction:discord.Interaction):
        '''
        Randomly message channel with an image from louvre channel
        '''
        if interaction.guild and interaction.guild.id in self.allowed_guild_ids:

            random_msg = self.fetch_random_message()

            if random_msg: 

                emb = discord.Embed(title='A gift from the Louvre', color=8388564)
                emb.set_image(url=random_msg.attachments[0].url)

                message_link = f"https://discord.com/channels/{random_msg.guild.id}/{random_msg.channel.id}/{random_msg.id}"
                emb.add_field(name='🔎', value=message_link)

                emb.set_footer(text='Curated by: {0}, circa {1}'.format(random_msg.author.name, random_msg.created_at.strftime('%Y-%m-%d')))            
            
                await interaction.response.send_message(
                    content=random_msg.content,
                    embed=emb
                )

                await interaction.response.send_message(
                                random_msg.content
                            )            
            else:
                await interaction.response.send_message('The louvre has been robbed!')
        
        else:

            await interaction.response.send_message('Not in here o_o')


async def setup(bot):
    cog = louvre(bot)
    await bot.add_cog(cog)
