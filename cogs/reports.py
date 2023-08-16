import discord
from discord import app_commands
from discord.ext import commands

# Check if specified channel exists, if not, create it
async def check_channel(guild, channel_name):
    try:

        reports_channel = discord.utils.get(guild.text_channels, name=channel_name)

        if reports_channel is None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            reports_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        return reports_channel
    
    except:
        print(f'error checking channel')


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reports_channel_name = "reports"  # Change the channel name here

    # New command: !flag <user> <reason>
    @app_commands.command(name='flag', description='report red flags!!')
    async def flag(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        guild = interaction.guild
        reports_channel = await check_channel(guild, self.reports_channel_name)
        timestamp = interaction.created_at.strftime('%Y %b, %d')  # Get the timestamp of when the report was made
        embed = discord.Embed(title="Report 🚩",
                              color=discord.Color.red())
        embed.add_field(name="Reported Person", value=user.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Reporter", value=interaction.user.mention, inline=False)
        embed.add_field(name="Report Date", value=timestamp, inline=False)

        report_message = f"Reported {interaction.user.mention} for {reason} - Reported by {interaction.user.mention} on {timestamp}"

        try: 
            await reports_channel.send(embed=embed) 
            # print('ok8')
            
            print('ok9')
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to do that")
        except discord.HTTPException:
            await interaction.response.send_message('An error occured')

        await interaction.response.send_message(embed=embed)
        await interaction.message.add_reaction("🚩")
        
    # New command: !flags <user>
    @app_commands.command()
    async def flags(self, interaction:discord.Interaction, user: discord.Member):
        guild = interaction.guild
        
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

            await interaction.response.send_message(content=f"looks like {user.mention} has been a bad gender neutral pronoun", embed=embed)
        else:
            await interaction.response.send_message(f"No reports found for {user.display_name}.")


async def setup(bot):
    cog = Report(bot)
    await bot.add_cog(cog)