import discord
import random
from discord.ext import commands

class louvre(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def louvre(self, ctx, case_insensitive=True):
        '''
        Randomly message channel with an image from louvre channel
        '''
        channel = self.bot.get_channel(636799254152871936)
        # channel = self.bot.get_channel(934888003367764028) # test server

        allmsg = []

        async for msg in channel.history(limit=1000):
            if hasattr(msg, 'attachments'):
                if len(msg.attachments) > 0:
                    allmsg.append(msg)

        random_msg = random.choice(allmsg)

        emb = discord.Embed(title='A gift from the Louvre', color=8388564)
        
        emb.set_image(url=random_msg.attachments[0].url)
        emb.set_footer(text='Curated by: {0}, circa {1}'.format(random_msg.author.name, random_msg.created_at.strftime('%Y-%m-%d')))
        

        await ctx.send(
            random_msg.content,
            embed=emb
            )    
  
async def setup(bot):
    await bot.add_cog(louvre(bot))