import discord
import random
from discord.ext import commands


class louvre(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 636799254152871936
        # self.channel_id = 934888003367764028 # test server
        self.allowed_guild_ids = [83311868432617472, 873243765157032026]

    async def fetch_random_message(self):
        channel = self.bot.get_channel(self.channel_id)
        messages = []
        async for message in channel.history():
            if message.attachments:
                messages.append(message)
        return random.choice(messages) if messages else None

    @commands.command()
    async def louvre(self, ctx, case_insensitive=True):
        '''
        Randomly message channel with an image from louvre channel
        '''
        if ctx.guild and ctx.guild.id in self.allowed_guild_ids:

            random_msg = await self.fetch_random_message()

            if random_msg: 

                emb = discord.Embed(title='A gift from the Louvre', color=8388564)
                emb.set_image(url=random_msg.attachments[0].url)

                message_link = f"https://discord.com/channels/{random_msg.guild.id}/{random_msg.channel.id}/{random_msg.id}"
                emb.add_field(name='🔎', value=message_link)

                emb.set_footer(text='Curated by: {0}, circa {1}'.format(random_msg.author.name, random_msg.created_at.strftime('%Y-%m-%d')))            
            
                await ctx.send(
                    random_msg.content,
                    embed=emb
                )

            else:
                await ctx.send('The louvre has been robbed!')
        else:

            await ctx.send('Not in here o_o')


async def setup(bot):
    cog = louvre(bot)
    await bot.add_cog(cog)
