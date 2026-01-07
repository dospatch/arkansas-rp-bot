import discord
from discord.ext import commands
from discord import ui
import os
import asyncio  # Fix 1: Added missing import

# Fix 2: Use the variable NAME from Railway, not the actual token string
TOKEN = os.getenv('MTQ1ODI0NDMxMTM4Nzg2NTE3MA.GnX95G.BhUqp295O6AYr9t43YvI37I2kyDfRnO5UwP53Q')

# Replace these with your actual IDs
CATEGORY_ID = 1301544056975003746  # <--- REPLACE THIS WITH YOUR CATEGORY ID
STAFF_ROLE_ID = 1301544059034406943 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class TicketControl(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketLauncher(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="📩 Open Support Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: ui.Button):
        guild = interaction.guild
        staff_role = guild.get_role(STAFF_ROLE_ID)
        
        channel_name = f"ticket-{interaction.user.name.lower()}"
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if existing_channel:
            return await interaction.response.send_message(f"You already have a ticket open: {existing_channel.mention}", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        category = guild.get_channel(CATEGORY_ID)
        ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)
        
        await interaction.response.send_message(f"Ticket created! {ticket_channel.mention}", ephemeral=True)
        
        embed = discord.Embed(
            title="Support Requested", 
            description=f"Welcome {interaction.user.mention}, staff will be with you shortly.\n\nClick the button below to close this ticket.", 
            color=discord.Color.blue()
        )
        await ticket_channel.send(embed=embed, view=TicketControl())

@bot.event
async def on_ready():
    bot.add_view(TicketLauncher())
    bot.add_view(TicketControl())
    print(f'✅ Ticket Bot is online as {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_tickets(ctx): # Fix 3: Added 'async' before 'def'
    embed = discord.Embed(
        title="Arkansas State RP Support", 
        description="Click the button below to open a ticket with our staff team.", 
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=TicketLauncher())

bot.run(TOKEN)