import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA = {
    "piyade": {
        "alan": [("sun_tzu.png", "bai_qi.png", "piyade_alan_ekipman.png"), ("bai_qi.png", "liu_che.png", "piyade_alan_ekipman.png"), ("sun_tzu.png", "liu_che.png",  "piyade_alan_ekipman.png"), ("scipio.png", "liu_che.png", "piyade_alan_ekipman.png"), ("ragnar.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "alexander.png", "piyade_alan_ekipman.png")],
        "rally": [("scipio_aemilianus.png", "ivar.png", "piyade_rally_ekipman.png"), ("scipio_aemilianus.png", "charles_martel.png", "piyade_rally_ekipman.png"), ("charles_martel.png", "harald.png", "piyade_rally_ekipman.png")],
        "garnizon": [("gorgo.png", "tokugawa.png", "piyade_garnizon_ekipman"), ("gorgo.png", "cheo_yeong.png", "piyade_garnizon_ekipman"), ("gorgo.png", "heraclius.png", "piyade_garnizon_ekipman"), ("gorgo.png", "hector.png", "piyade_garnizon_ekipman")]
    },
    "suvari": {
        "alan": [("gang_ghamchan.png", "achilleus.png", "suvari_alan_ekipman"), ("arthur.png", "achilleus.png", "suvari_alan_ekipman"), ("achilleus.png", "gang_ghamchan.png", "suvari_alan_ekipman"), ("arthur.png", "huo_qubing.png", "suvari_alan_ekipman"), ("attila.png", "achilleus.png", "suvari_alan_ekipman")],
        "rally": [("attila.png", "subutai.png", "suvari_rally_ekipman"), ("attila.png", "achilleus.png", "suvari_rally_ekipman"), ("attila.png", "charles_martel.png", "suvari_rally_ekipman")],
        "garnizon": [("elanor.png", "heraclius.png", "suvari_garnizon_ekipman")]
    },
    "okcu": {
        "alan": [("qin_shi.png", "zhuge.png", "okcu_alan_ekipman"), ("alparslan.png", "hermann.png", "okcu_alan_ekipman"), ("qin_shi.png", "ysg.png", "okcu_alan_ekipman"), ("zhuge.png", "hermann.png", "okcu_alan_ekipman")],
        "rally": [("shapur.png", "ashurbanipal.png", "okcu_rally_ekipman")],
        "garnizon": [("hayam.png", "heraclius.png", "okcu_garnizon_ekipman"), ("hayam.png", "cheo.png", "okcu_garnizon_ekipman"), ("cheo_yeong.png", "heraclius.png", "okcu_garnizon_ekipman")]
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