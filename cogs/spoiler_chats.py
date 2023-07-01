from discord.ext import commands


class SpoilerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spoiler(self, ctx, channel_name):
        # Check if the category exists, otherwise create it
        spoiler_category = discord.utils.get(ctx.guild.categories, name='Spoilers')
        if spoiler_category is None:
            spoiler_category = await ctx.guild.create_category('Spoilers')

        # Create the spoiler channel under the spoiler category
        spoiler_channel = await spoiler_category.create_text_channel(channel_name)

        # Send a message with buttons to the created channel
        embed = discord.Embed(title='Channel Access', description='Click the buttons below to manage channel access')
        join_button = discord.Button(style=discord.ButtonStyle.green, label='Join', emoji='✅')
        leave_button = discord.Button(style=discord.ButtonStyle.red, label='Leave', emoji='❌')
        archive_button = discord.Button(style=discord.ButtonStyle.grey, label='Archive', emoji='📚')
        action_row = discord.ActionRow(join_button, leave_button, archive_button)

        message = await spoiler_channel.send(embed=embed, components=[action_row])
        await message.add_reaction(join_button.emoji)
        await message.add_reaction(leave_button.emoji)
        await message.add_reaction(archive_button.emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = guild.get_member(payload.user_id)
            emoji = payload.emoji.name

            if emoji == '✅':
                await channel.set_permissions(user, read_messages=True, send_messages=True)
            elif emoji == '❌':
                await channel.set_permissions(user, overwrite=None)
            elif emoji == '📚':
                archive_category = discord.utils.get(guild.categories, name='Archived')
                if archive_category is None:
                    archive_category = await guild.create_category('Archived')
                await channel.edit(category=archive_category)


async def setup(bot):
    cog = SpoilerCog(bot)
    await bot.add_cog(cog)
