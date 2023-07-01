import discord
from discord.ext import commands

# Check if specified channel exists, if not, create it
async def check_channel(guild, channel_name):
    reports_channel = discord.utils.get(guild.text_channels, name=channel_name)

    if reports_channel is None:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        reports_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
    
    return reports_channel


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reports_channel_name = "reports"  # Change the channel name here

    # New command: !flag <user> <reason>
    @commands.command()
    async def flag(self, ctx, user: discord.Member, *, reason: str):
        guild = ctx.guild
        reports_channel = await check_channel(guild, self.reports_channel_name)

        timestamp = ctx.message.created_at.strftime('%Y %b, %d')  # Get the timestamp of when the report was made

        embed = discord.Embed(title="Report 🚩",
                              color=discord.Color.red())
        embed.add_field(name="Reported Person", value=user.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Reporter", value=ctx.author.mention, inline=False)
        embed.add_field(name="Report Date", value=timestamp, inline=False)

        report_message = f"Reported {user.mention} for {reason} - Reported by {ctx.author.mention} on {timestamp}"

        try: 
            await reports_channel.send(embed=embed) 
            await ctx.message.add_reaction("🚩")
        except discord.Forbidden:
            await ctx.send("I don't have permission to do that")
        except discord.HTTPException:
            await ctx.send('An error occured')
        
    # New command: !flags <user>
    @commands.command()
    async def flags(self, ctx, user: discord.Member):
        guild = ctx.guild
        
        reports_channel = await check_channel(guild, self.reports_channel_name)

        reports = [] 
        counter = 0

        async for message in reports_channel.history(limit=None):

            if len(message.embeds) > 0: 
                embed = message.embeds[0]

                reported_user_id = None
                reported_reason = None
                reporter = None

                for field in embed.fields:
                    if field.name == 'Reported Person':
                        reported_user_id = int(field.value.strip("<@!>"))

                    if field.name == 'Reason':
                        reported_reason = field.value

                    if field.name == 'Reporter':
                        reporter = guild.get_member(int(field.value.strip("<@!>"))).display_name

                    if field.name == 'Report Date':
                        report_date = field.value

                if user.id == reported_user_id:

                    reports.append(f"> {reported_reason} \n *reported by: {reporter} on {report_date}* \n")
                    counter += 1

                    if counter >= 10:
                        break
        if reports:
            embed = discord.Embed(title="Reports 🚩",
                                  color=discord.Color.red()                
                                  )
            embed.add_field(name="Latest Reports", value='\n'.join(reversed(reports)))

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No reports found for {user.display_name}.")


async def setup(bot):
    cog = Report(bot)
    await bot.add_cog(cog)