import yaml
from discord.ui import Button, View
import discord
import random

with open('img.yaml') as f:

    data = yaml.load(f, Loader=yaml.FullLoader)


class View(discord.ui.View):

    def __init__(self, ctx, content, embed):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.content = content 
        self.embed = embed
        self.yes_count = 0
        self.no_count = 0
        self.responses = {}
        self.win_probability = random.randint(0, 100)
        self.quote = get_quote()
        self.bat_uses = 0 


    def generate_emb_message(self, yes_responders, no_responders):  

        if len(yes_responders) == 0:
            yes_value = '---'

        else: 
            yes_value = '\n'.join(list(yes_responders))

        if len(no_responders) == 0:
            no_value = '---'

        else:
            no_value = '\n'.join(list(no_responders))

        rat_bastard_name = '**RAT BASTARDS** ✅ ({0}/5):'.format(self.yes_count)

        self.win_probability =  min(max(self.win_probability + random.randint(-10,10), 0), 100)
        win_url = get_win_url(self.win_probability)

        emb = discord.Embed(
                title='RATSIGNAL', 
                description=self.embed, 
                color=8388564)
        emb.add_field(
                name=rat_bastard_name, 
                value=yes_value, 
                inline=True)
        emb.add_field(
                name='**COWARDS** ❌:', 
                value=no_value, 
                inline=True)
        emb.add_field(
                name='**Win Probability** 🎲:', 
                value='{0}%'.format(self.win_probability), 
                inline=False)        
        emb.set_image(url=win_url)
        emb.set_footer(text=self.quote)

        return emb        

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji = '✅')
    async def yes_button_callback(self, interaction, button):  
        self.responses[interaction.user.mention] = 'yes'
        
        yes_responders = [response for response in self.responses.keys() if 'yes' in self.responses[response]]
        self.yes_count = len(yes_responders)
        no_responders = [response for response in self.responses.keys() if 'no' in self.responses[response]]
        self.no_count = len(no_responders)

        emb = self.generate_emb_message(yes_responders, no_responders)

        await interaction.response.edit_message(content = self.content, embed = emb, view=self)        

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji= '❌')
    async def no_button_callback(self, interaction, button):
        self.responses[interaction.user.mention] = 'no'
        self.no_count += 1 

        yes_responders = [response for response in self.responses.keys() if 'yes' in self.responses[response]]
        self.yes_count = len(yes_responders)
        no_responders = [response for response in self.responses.keys() if 'no' in self.responses[response]]
        self.no_count = len(no_responders)

        emb = self.generate_emb_message(yes_responders, no_responders)


        await interaction.response.edit_message(content = self.content, embed = emb, view=self)        

    @discord.ui.button(style=discord.ButtonStyle.grey, emoji= '🦇')
    async def rat_button_callback(self, interaction, button):
        self.bat_uses += 1 

        
        yes_responders = [response for response in self.responses.keys() if 'yes' in self.responses[response]]
        if len(yes_responders) > 0:
            content = ', '.join(list(yes_responders))

            await interaction.response.send_message(content)


# class MyView(discord.ui.View):

#     def __init__(self, ctx, content):
#         super().__init__(timeout=None)
#         self.ctx = ctx
#         self.content = content 
#         self.yes_count = 0
#         self.no_count = 0

#     @discord.ui.button(label="Yes!", style=discord.ButtonStyle.green)
#     async def yes_button_callback(self, interaction, button):  
#         self.yes_count += 1 
#         button.label = "Yes: {}".format(self.yes_count)
#         # await interaction.response.send_message('{} aids the usurper'.format(self.ctx.author.mention))
#         self.content = self.content + '\n' + '- ⚔️ ' + interaction.user.name
#         await interaction.response.edit_message(content = self.content, view=self)
        
#     @discord.ui.button(label="No!", style=discord.ButtonStyle.red, custom_id="danger")
#     async def no_button_callback(self, interaction, button):
#         self.no_count += 1 
#         button.label = "No: {}".format(self.no_count)
#         self.content = self.content + '\n' + '- 🛡️ ' + interaction.user.name
#         # await interaction.response.send_message('{} cowers in fear'.format(self.ctx.author.mention))        
#         await interaction.response.edit_message(content = self.content, view=self)
        



def get_quote():
    quote = random.choice(data.get('emiya'))

    return quote


def get_win_url(win_probability):
    '''
    Return link based on win probability 
    '''
    if win_probability <= 10:
        win_url = data.get('img').get('img1').get('link')

    elif win_probability <= 20:
        win_url = data.get('img').get('img2').get('link')

    elif win_probability <= 30:
        win_url = data.get('img').get('img3').get('link')                        

    elif win_probability <= 40:
        win_url = data.get('img').get('img4').get('link')

    elif win_probability <= 50:
        win_url = data.get('img').get('img5').get('link')                                                

    elif win_probability <= 60:
        win_url = data.get('img').get('img6').get('link')

    elif win_probability <= 70:
        win_url = data.get('img').get('img7').get('link')

    elif win_probability <= 80:
        win_url = data.get('img').get('img8').get('link')                        

    elif win_probability <= 90:
        win_url = data.get('img').get('img9').get('link')

    elif win_probability <= 100:
        win_url = data.get('img').get('img10').get('link')    

    return win_url