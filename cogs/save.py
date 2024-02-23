from discord.ext import commands
from discord.ui import Button, View 
import discord
import traceback

class ReactionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_guild_ids = [416439957444362253, 873243765157032026]  # List of allowed guild IDs
        self.excluded_channel_ids = [1024037669212258304]  # List of excluded channel IDs
        # Mapping of guild IDs to their respective saved channel IDs
        self.guild_to_saved_channel = {
            416439957444362253: 1209756849835085895,  # Example: Guild ID 123456789 saves to Channel ID 111111111
            873243765157032026: 1124526379132792854
        }    

    class DeleteButton(View):
        def __init__(self, bot, original_message_id, saved_message_id, *args, **kwargs):
            super().__init__(*args, **kwargs, timeout=None)
            self.bot = bot
            self.original_message_id = original_message_id
            self.saved_message_id = saved_message_id

        @discord.ui.button(label='Remove', style=discord.ButtonStyle.gray) #emoji="❌",
        async def delete_button(self, button: Button, interaction: discord.Interaction):
            try:
            # Send a simple response
                await interaction.response.send_message("Button clicked.")
            except Exception as e:
                print(f"An error occurred in delete_button: {e}", exc_info=True)


            # # Defer the interaction
            # await interaction.response.defer(ephemeral=True)

            # # Fetch and delete the saved message
            # channel = interaction.channel
            # try:
            #     # Remove the star reaction from the original message
            #     original_message = await channel.fetch_message(self.original_message_id)
            #     for reaction in original_message.reactions:
            #         if str(reaction.emoji) == "⭐":
            #             await reaction.remove(self.bot.user)

            #     # Fetch and delete the saved message
            #     saved_message = await channel.fetch_message(self.saved_message_id)
            #     await saved_message.delete()

            # except Exception as e:
            #     print(f"An error occurred in delete_button: {e}")
            #     traceback.print_exc()  # This will print the full traceback to the console
            #     await interaction.followup.send("An unexpected error occurred.", ephemeral=True)



            #     await interaction.response.send_message("Message removed.", ephemeral=True)
            # except discord.NotFound:
            #     await interaction.response.send_message("Message not found.", ephemeral=True)
            # except discord.Forbidden:
            #     await interaction.response.send_message("I don't have permissions to delete messages.", ephemeral=True)
            # except discord.HTTPException as e:
            #     await interaction.response.send_message(f"Failed to delete message: {e}", ephemeral=True)



    async def is_message_already_saved(self, saved_channel, original_channel_id, message_id):
        # Fetch a certain number of recent messages to check
        async for message in saved_channel.history(limit=300):
            if message.embeds:
                for embed in message.embeds:
                    # Construct the URL of the original message
                    original_message_url = f"https://discord.com/channels/{saved_channel.guild.id}/{original_channel_id}/{message_id}"

                    for field in embed.fields:
                        if original_message_url in field.value:
                            return True
        return False



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        saved_channel_id = self.guild_to_saved_channel[payload.guild_id]
        saved_channel = self.bot.get_channel(saved_channel_id)

        # Fetch the member from the guild
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)        

        # Check if the reaction is in an allowed guild and has a saved channel
        if payload.guild_id not in self.allowed_guild_ids or payload.guild_id not in self.guild_to_saved_channel:
            return

        # Fetch the channel and message
        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return
        
        # Get the original sender of the message
        original_sender = message.author
        sender_name = original_sender.display_name  # Display name of the sender

        # Check if the reaction is not in an excluded channel
        if message.channel.id in self.excluded_channel_ids:
            return

        # Check if the message is already saved
        if await self.is_message_already_saved(saved_channel, payload.channel_id, payload.message_id):
            return

        # Check the emoji and the user who reacted (not the bot itself)
        if str(payload.emoji) == "⭐" and payload.user_id != self.bot.user.id:
            user = self.bot.get_user(payload.user_id)

            # Fetch the saved channel using the guild_to_saved_channel mapping
            saved_channel_id = self.guild_to_saved_channel[payload.guild_id]
            saved_channel = self.bot.get_channel(saved_channel_id)
            if not saved_channel:
                return
            
            # Create an embed object
            embed = discord.Embed(color=8388564)
            # embed.add_field(name="Author", value=sender_name, inline=False)

            # Check for attachments and add them to the embed
            if message.content: 
                embed.add_field(name='Author', value=sender_name, inline=False)
                embed.add_field(name='Message', value=message.content, inline=False)
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
            message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}" 
            
            embed.add_field(name="", value=message_link, inline=True)

            # Set the footer to include the username of the user who added the reaction
            embed.set_footer(text="Saved by: {}".format(member.display_name))

            # Send the embed to the saved channel
            sent_message = await saved_channel.send(embed=embed)

            # Create the delete button view with the correct saved_message_id
            # view = self.DeleteButton(self.bot, original_message_id=message.id, saved_message_id=sent_message.id)
            # await sent_message.edit(view=view)                

async def setup(bot):
    cog = ReactionHandler(bot)
    await bot.add_cog(cog)
