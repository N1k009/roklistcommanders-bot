import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA = {
    "piyade": {
        "alan": [("sun_tzu.png", "bai_qi.png"), ("bai_qi.png", "liu_che.png"), ("sun_tzu.png", "liu_che.png"), ("scipio.png", "liu_che.png"), ("ragnar.png", "scipio.png"), ("liu_che.png", "scipio.png"), ("liu_che.png", "alexander.png")],
        "rally": [("scipio_aemilianus.png", "ivar.png"), ("scipio_aemilianus.png", "charles_martel.png"), ("charles_martel.png", "harald.png")],
        "garnizon": [("gorgo.png", "tokugawa.png"), ("gorgo.png", "cheo_yeong.png"), ("gorgo.png", "heraclius.png"), ("gorgo.png", "hector.png")]
    },
    "suvari": {
        "alan": [("gang_ghamchan.png", "achilleus.png"), ("arthur.png", "achilleus.png"), ("achilleus.png", "gang_ghamchan.png"), ("arthur.png", "huo_qubing.png"), ("attila.png", "achilleus.png")],
        "rally": [("attila.png", "subutai.png"), ("attila.png", "achilleus.png"), ("attila.png", "charles_martel.png")],
        "garnizon": [("elanor.png", "heraclius.png")]
    },
    "okcu": {
        "alan": [("qin_shi.png", "zhuge.png"), ("alparslan.png", "hermann.png"), ("qin_shi.png", "ysg.png"), ("zhuge.png", "hermann.png")],
        "rally": [("shapur.png", "ashurbanipal.png")],
        "garnizon": [("hayam.png", "heraclius.png"), ("hayam.png", "cheo.png"), ("cheo_yeong.png", "heraclius.png")]
    },
    "mix": {
        "garnizon": [("lapu_lapu.png", "mathias.png"), ("mathias.png", "lapu_lapu.png"), ("mathias.png", "heraclius.png"), ("heraclius.png", "mathias.png")]
    }
}

class StratejiView(discord.ui.View):
    def __init__(self, kategori):
        super().__init__(timeout=None)
        self.kategori = kategori

    async def gonder(self, interaction, tip):
        kombinasyonlar = DATA.get(self.kategori, {}).get(tip)
        if not kombinasyonlar: return
        
        await interaction.response.send_message(f"**{self.kategori.upper()} - {tip.upper()} Sıralamanız:**", ephemeral=True)
        
        for komutan1, komutan2 in kombinasyonlar:
            mesaj = f"{komutan1.replace('.png','').replace('_',' ')} + {komutan2.replace('.png','').replace('_',' ')}"
            files = []
            if os.path.exists(f"gorseller/{komutan1}"): files.append(discord.File(f"gorseller/{komutan1}"))
            if os.path.exists(f"gorseller/{komutan2}"): files.append(discord.File(f"gorseller/{komutan2}"))
            
            if files:
                await interaction.followup.send(content=f"**{mesaj}**", files=files, ephemeral=True)
        
        if self.kategori == "mix":
            await interaction.followup.send("Liderlik komutanları genellikle 2.cil komutanlar, buff için veya garnizon için kullanılıyorlar.\nLeader commanders are generally used as secondary commanders, for buffs or for garrison.", ephemeral=True)

    @discord.ui.button(label="Alan", style=discord.ButtonStyle.primary)
    async def alan(self, i, b): await self.gonder(i, "alan")
    @discord.ui.button(label="Rally", style=discord.ButtonStyle.danger)
    async def rally(self, i, b): await self.gonder(i, "rally")
    @discord.ui.button(label="Garnizon", style=discord.ButtonStyle.success)
    async def garnizon(self, i, b): await self.gonder(i, "garnizon")

@bot.command()
async def piyade(ctx): 
    await ctx.message.delete()
    await ctx.send("Seçim yap:", view=StratejiView("piyade"))

@bot.command()
async def okcu(ctx): 
    await ctx.message.delete()
    await ctx.send("Seçim yap:", view=StratejiView("okcu"))

@bot.command()
async def suvari(ctx): 
    await ctx.message.delete()
    await ctx.send("Seçim yap:", view=StratejiView("suvari"))

@bot.command()
async def mix(ctx): 
    await ctx.message.delete()
    await ctx.send("Seçim yap:", view=StratejiView("mix"))

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
