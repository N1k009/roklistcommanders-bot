import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA = {
    "piyade": {
        "open-field": [("sun_tzu.png", "bai_qi.png", "piyade_alan_ekipman.png"), ("bai_qi.png", "liu_che.png", "piyade_alan_ekipman.png"), ("sun_tzu.png", "liu_che.png", "piyade_alan_ekipman.png"), ("scipio.png", "liu_che.png", "piyade_alan_ekipman.png"), ("ragnar.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "alexander.png", "piyade_alan_ekipman.png")],
        "rally": [("scipio_aemilianus.png", "ivar.png", "piyade_rally_ekipman.png"), ("scipio_aemilianus.png", "charles_martel.png", "piyade_rally_ekipman.png"), ("charles_martel.png", "harald.png", "piyade_rally_ekipman.png")],
        "garnizon": [("gorgo.png", "tokugawa.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "cheo_yeong.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "heraclius.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "hector.png", "piyade_garnizon_ekipman.png")]
    },
    "suvari": {
        "open-field": [("gang_ghamchan.png", "achilleus.png", "suvari_alan_ekipman.png"), ("arthur.png", "achilleus.png", "suvari_alan_ekipman.png"), ("achilleus.png", "gang_ghamchan.png", "suvari_alan_ekipman.png"), ("arthur.png", "huo_qubing.png", "suvari_alan_ekipman.png"), ("attila.png", "achilleus.png", "suvari_alan_ekipman.png")],
        "rally": [("attila.png", "subutai.png", "suvari_rally_ekipman.png"), ("attila.png", "achilleus.png", "suvari_rally_ekipman.png"), ("attila.png", "charles_martel.png", "suvari_rally_ekipman.png")],
        "garnizon": [("elanor.png", "heraclius.png", "suvari_garnizon_ekipman.png")]
    },
    "okcu": {
        "open-field": [("qin_shi.png", "zhuge.png", "okcu_alan_ekipman.png"), ("alparslan.png", "hermann.png", "okcu_alan_ekipman.png"), ("qin_shi.png", "ysg.png", "okcu_alan_ekipman.png"), ("zhuge.png", "hermann.png", "okcu_alan_ekipman.png")],
        "rally": [("shapur.png", "ashurbanipal.png", "okcu_rally_ekipman.png")],
        "garnizon": [("hayam.png", "heraclius.png", "okcu_garnizon_ekipman.png"), ("hayam.png", "cheo_yeong.png", "okcu_garnizon_ekipman.png"), ("cheo_yeong.png", "heraclius.png", "okcu_garnizon_ekipman.png")]
    },
    "mix": {
        "garnizon": [("lapu_lapu.png", "mathias.png", "mix_garnizon_ekipman.png"), ("mathias.png", "lapu_lapu.png", "mix_garnizon_ekipman.png"), ("mathias.png", "heraclius.png", "mix_garnizon_ekipman.png"), ("heraclius.png", "mathias.png", "mix_garnizon_ekipman.png")]
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
        
        for k1, k2, ekipman in kombinasyonlar:
            mesaj = f"{k1.replace('.png','').replace('_',' ')} + {k2.replace('.png','').replace('_',' ')}"
            files = []
            # 3'lü kontrol: k1, k2 ve ekipman
            for dosya in [ekipman, k1, k2]:
                if os.path.exists(f"gorseller/{dosya}"):
                    files.append(discord.File(f"gorseller/{dosya}"))
            
            if files:
                await interaction.followup.send(content=f"**{mesaj}**", files=files, ephemeral=True)
        
        if self.kategori == "mix":
            await interaction.followup.send("Liderlik komutanları genellikle 2.cil komutanlar, buff için veya garnizon için kullanılıyorlar.\nLeader commanders are generally used as secondary commanders, for buffs or for garrison.", ephemeral=True)

    @discord.ui.button(label="Open-Field", style=discord.ButtonStyle.primary)
    async def open_field(self, i, b): await self.gonder(i, "open-field")
    @discord.ui.button(label="Rally", style=discord.ButtonStyle.danger)
    async def rally(self, i, b): await self.gonder(i, "rally")
    @discord.ui.button(label="Garnizon", style=discord.ButtonStyle.success)
    async def garnizon(self, i, b): await self.gonder(i, "garnizon")

# Komutlar (Buton isimleri güncellendi)
@bot.command()
async def piyade(ctx): 
    await ctx.message.delete()
    await ctx.send("Piyade için seçim yap:", view=StratejiView("piyade"))

@bot.command()
async def okcu(ctx): 
    await ctx.message.delete()
    await ctx.send("Okçu için seçim yap:", view=StratejiView("okcu"))

@bot.command()
async def suvari(ctx): 
    await ctx.message.delete()
    await ctx.send("Süvari için seçim yap:", view=StratejiView("suvari"))

@bot.command()
async def mix(ctx): 
    await ctx.message.delete()
    await ctx.send("Mix için seçim yap:", view=StratejiView("mix"))

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
