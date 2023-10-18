import discord
from discord import app_commands
from discord.ext import commands
import json
import openai
from datetime import datetime 
import asyncio
import os 


class Lore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv('OPENAI_API_KEY')
        os.makedirs(os.path.dirname('data/'), exist_ok=True)
        self.prompts = {
            '83311868432617472': """
                Discord server name: Yahallo
                """,
            '416439957444362253': """
                I will send you some information collected from a Discord bot I wrote. This Discord bot has a lore command that allows users to submit information, which is being aggregated here. The JSON file contains user-submitted entries, each formatted as a JSON string that includes the user who submitted the entry and the timestamp.

                I want you to turn the information from these JSON-formatted entries into a short story, just a few paragraphs, written in a fantasy style. Feel free to get creative

                Please keep the response as short as possible but still comprehensive.

                Please use this background to craft a fantastical tale that transports readers to the enchanting realm of "bobaverse."  Keep the response within 500 characters

            """
        }

    @app_commands.command(name='lore')
    async def lore(self, interaction: discord.Interaction, entry: str):
        self.guild_id = interaction.guild_id 
        self.data_file = f'data/{interaction.guild.id}_lore_data.json'

        try:
            """Add a lore entry."""
            # Load existing lore entries
            lore_entries = await self.load_lore_data()

            # Add the new entry with user and timestamp
            user = interaction.user.mention  # Get the username of the user who submitted the lore
            user_tag = interaction.user.display_name  # Get the username of the user who submitted the lore
            timestamp = interaction.created_at.strftime('%Y %b, %d')  # Get the timestamp of when the report was made            
            lore_entries.append({"user": user, "user_tag": user_tag, "timestamp": timestamp, "lore": entry})

            # Save the updated lore data
            await self.save_lore_data(lore_entries)

            await interaction.response.send_message(f"Lore entry added: {entry}")

        except Exception as e:
            print(f"An error occurred: {e}")

    @app_commands.command(name='lore-summary')

    async def lore_summary(self, interaction:discord.Interaction, prompt: str=""):
        try:        
            await interaction.response.defer()
            self.guild_id = interaction.guild_id 
            self.data_file = f'data/{interaction.guild.id}_lore_data.json'

            """Generate a lore summary."""
            # Load existing lore entries
            lore_entries = await self.load_lore_data()

            # Generate a summary (you can replace this with your AI-based summary generation)

            summary = await self.generate_fantasy_story(lore_entries, prompt)
            await asyncio.sleep(delay=3)

            # await interaction.response.send_message()
            
            await interaction.followup.send(f">>> {summary}")            
            # await interaction.response.send_message(summary)
        except Exception as e:
            print(f"An error occured {e}")

    async def load_lore_data(self):
        try:
            with open(self.data_file, 'r') as file:
                lore_entries = json.load(file)
        except FileNotFoundError:
            lore_entries = []

        return lore_entries

    async def save_lore_data(self, lore_entries):
        with open(self.data_file, 'w') as file:
            json.dump(lore_entries, file, indent=4)

    async def generate_fantasy_story(self, lore_entries, additional_context):
        try:
            openai.api_key = self.token

            # Base Prompt
            base_prompt = '''
                You are a Discord server bot that shares snippets of lore based on user-submitted entries.
                Your role is to craft these pieces of information into a captivating short story written in a fantasy style.
                You do not need to use all the information that's available to you. Put more consideration to the more recent entries. 
                If there is "High Priority Context", prioritize that when responding.
                Please keep the response within 700 characters. 
                At the end of this response is a string converted to JSON that contains the user that submitted the lore entry, the date of the submission, and the submission
            '''

            # Server-specific content
            
            guild_context = self.prompts.get(str(self.guild_id), "")

            # Combine base, server-specific, and additional context
            prompt = base_prompt
            if guild_context:
                prompt += f'\nServer Specific Context:" {guild_context}'
            
            if additional_context:
                prompt += f'\High Priority Context:" {additional_context}'

            # Convert lore entries to JSON string
            lore_entries_json = json.dumps(lore_entries)

            # Assemble final prompt
            lore_text = prompt + "\n\nUser-Submitted Entries:\n" + lore_entries_json

            # Generate the story using GPT-3
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=lore_text,
                max_tokens=300,  # Adjust to control the length of the story
                temperature=0.7  # Adjust to control the creativity of the output
            )

            return response.choices[0].text
        
        except Exception as e:
            print(f"An error occurred: {e}")          

async def setup(bot):
   await bot.add_cog(Lore(bot))
