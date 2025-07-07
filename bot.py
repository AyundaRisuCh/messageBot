import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class KirimView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Kirim ke Channel", style=discord.ButtonStyle.success)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.client.get_channel(TARGET_CHANNEL_ID)
        if channel:
            await channel.send(f"📨 {interaction.user.mention} menekan tombol!")
            await interaction.response.send_message("✅ Pesan dikirim!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Channel tidak ditemukan.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Command disinkronkan: {len(synced)}")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.tree.command(name="kirimembed", description="Kirim embed dengan tombol")
async def kirimembed(interaction: discord.Interaction):
    embed = discord.Embed(title="🔔 Notifikasi", description="Klik tombol untuk kirim pesan ke channel khusus.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=KirimView())

bot.run(TOKEN)
