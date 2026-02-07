import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
import asyncio
from datetime import datetime
import psutil
import random
import aiohttp
import json

# ---------------- CONFIGURAÇÕES ---------------- #
TOKEN_DISCORD = os.environ.get("DISCORD_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
ADMIN_PASSWORD = ""

# Configuração Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# ---------------- SISTEMA DE DADOS (ECONOMIA/XP/CLÃS) ---------------- #
DATA_FILE = "members_data.json"
CLANS_FILE = "clans_data.json"

def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, 'r') as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, 'w') as f: json.dump(data, f, indent=4)

def update_member(user_id, xp=0, coins=0, win=False):
    data = load_json(DATA_FILE)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 1, "coins": 100, "messages": 0, "wins": 0}
    data[uid]["xp"] += xp
    data[uid]["coins"] += coins
    data[uid]["messages"] += 1
    if win: data[uid]["wins"] += 1
    next_lvl = data[uid]["level"] * 100
    lvl_up = False
    if data[uid]["xp"] >= next_lvl:
        data[uid]["level"] += 1
        data[uid]["xp"] = 0
        lvl_up = True
    save_json(DATA_FILE, data)
    return lvl_up, data[uid]["level"]

# ---------------- KEEP ALIVE ---------------- #
app = Flask('')
@app.route('/')
def home(): return "QG Nerd Bot Online!"
def run(): app.run(host='0.0.0.0', port=5000)
def keep_alive(): Thread(target=run).start()

# ---------------- CATEGORIA: IA (13) ---------------- #
@bot.tree.command(name="chat", description="Converse com a IA Gemini")
async def chat(interaction: discord.Interaction, mensagem: str):
    await interaction.response.defer()
    response = model.generate_content(mensagem)
    update_member(interaction.user.id, xp=5)
    await interaction.followup.send(f"✨ **IA:** {response.text[:1900]}")

@bot.tree.command(name="pergunta", description="Pergunta rápida para a IA")
async def pergunta(interaction: discord.Interaction, questao: str):
    await interaction.response.defer()
    response = model.generate_content(f"Responda de forma curta e nerd: {questao}")
    await interaction.followup.send(f"🤓 **Resposta:** {response.text[:1900]}")

@bot.tree.command(name="conselho", description="Peça um conselho para a IA")
async def conselho(interaction: discord.Interaction):
    await interaction.response.defer()
    response = model.generate_content("Dê um conselho sábio e nerd para o dia de hoje.")
    await interaction.followup.send(f"🧙‍♂️ **Conselho:** {response.text[:1900]}")

@bot.tree.command(name="traduzir", description="Traduz um texto para português via IA")
async def traduzir(interaction: discord.Interaction, texto: str):
    await interaction.response.defer()
    response = model.generate_content(f"Traduza para português brasileiro de forma natural: {texto}")
    await interaction.followup.send(f"🇧🇷 **Tradução:** {response.text[:1900]}")

@bot.tree.command(name="poema", description="IA cria um poema nerd")
async def poema(interaction: discord.Interaction, tema: str):
    await interaction.response.defer()
    response = model.generate_content(f"Escreva um poema curto sobre {tema} no estilo geek.")
    await interaction.followup.send(f"📜 **Poema:**\n{response.text[:1900]}")

@bot.tree.command(name="historia", description="IA conta uma história curta de RPG")
async def historia(interaction: discord.Interaction, tema: str):
    await interaction.response.defer()
    response = model.generate_content(f"Conte uma história curta de RPG sobre {tema}.")
    await interaction.followup.send(f"📖 **História:**\n{response.text[:1900]}")

@bot.tree.command(name="desafio-ia", description="IA gera um desafio de lógica")
async def desafio_ia(interaction: discord.Interaction):
    await interaction.response.defer()
    response = model.generate_content("Gere um desafio de lógica ou enigma nerd curto.")
    await interaction.followup.send(f"🧩 **Desafio:**\n{response.text[:1900]}")

@bot.tree.command(name="piada", description="IA conta uma piada nerd")
async def piada(interaction: discord.Interaction):
    await interaction.response.defer()
    response = model.generate_content("Conte uma piada nerd curta.")
    await interaction.followup.send(f"😂 **Piada:** {response.text[:1900]}")

@bot.tree.command(name="curiosidade", description="IA conta uma curiosidade nerd")
async def curiosidade(interaction: discord.Interaction):
    await interaction.response.defer()
    response = model.generate_content("Conte uma curiosidade nerd aleatória.")
    await interaction.followup.send(f"🧐 **Curiosidade:** {response.text[:1900]}")

@bot.tree.command(name="elogio", description="IA gera um elogio nerd")
async def elogio(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.defer()
    response = model.generate_content("Crie um elogio nerd e fofo.")
    await interaction.followup.send(f"💖 {membro.mention}, {response.text[:1800]}")

@bot.tree.command(name="filme-sugestão", description="IA sugere um filme nerd")
async def filme_sugestao(interaction: discord.Interaction, genero: str):
    await interaction.response.defer()
    response = model.generate_content(f"Sugira um filme nerd do gênero {genero} e explique o porquê.")
    await interaction.followup.send(f"🎬 **Sugestão de Filme:**\n{response.text[:1900]}")

@bot.tree.command(name="nome-rpg", description="IA gera um nome épico de RPG")
async def nome_rpg(interaction: discord.Interaction, raca: str):
    await interaction.response.defer()
    response = model.generate_content(f"Gere 5 nomes épicos de RPG para a raça {raca}.")
    await interaction.followup.send(f"🛡️ **Nomes Épicos:**\n{response.text[:1900]}")

@bot.tree.command(name="trivia", description="IA faz uma pergunta de trivia nerd")
async def trivia(interaction: discord.Interaction):
    await interaction.response.defer()
    response = model.generate_content("Faça uma pergunta de trivia nerd com 4 opções de resposta. Não dê a resposta agora.")
    await interaction.followup.send(f"🎮 **Trivia Nerd:**\n{response.text[:1900]}")

# ---------------- CATEGORIA: MODERAÇÃO (18) ---------------- #
@bot.tree.command(name="limpar", description="Limpa mensagens (Requer Senha)")
@app_commands.checks.has_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction, quantidade: int, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=quantidade)
    await interaction.followup.send(f"✅ {len(deleted)} mensagens removidas!", ephemeral=True)

@bot.tree.command(name="kick", description="Expulsa membro (Requer Senha)")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, membro: discord.Member, senha: str, motivo: str = "Não informado"):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await membro.kick(reason=motivo)
    await interaction.response.send_message(f"👢 {membro.name} expulso! Motivo: {motivo}")

@bot.tree.command(name="ban", description="Bane membro (Requer Senha)")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, membro: discord.Member, senha: str, motivo: str = "Não informado"):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await membro.ban(reason=motivo)
    await interaction.response.send_message(f"🔨 {membro.name} banido! Motivo: {motivo}")

@bot.tree.command(name="unban", description="Desbane por ID (Requer Senha)")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, id_membro: str, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    user = await bot.fetch_user(int(id_membro))
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"🔓 {user.name} desbanido!")

@bot.tree.command(name="mute", description="Silencia membro (Requer Senha)")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, membro: discord.Member, minutos: int, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    import datetime as dt
    await membro.timeout(dt.timedelta(minutes=minutos))
    await interaction.response.send_message(f"🤫 {membro.mention} silenciado!")

@bot.tree.command(name="lock", description="Tranca canal (Requer Senha)")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 Canal trancado!")

@bot.tree.command(name="unlock", description="Destranca canal (Requer Senha)")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 Canal destrancado!")

@bot.tree.command(name="slowmode", description="Define slowmode (Requer Senha)")
async def slowmode(interaction: discord.Interaction, segundos: int, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.channel.edit(slowmode_delay=segundos)
    await interaction.response.send_message(f"🐢 Slowmode: {segundos}s")

@bot.tree.command(name="nuke-canal", description="Recria canal (Requer Senha)")
async def nuke_canal(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    pos = interaction.channel.position
    new = await interaction.channel.clone(); await interaction.channel.delete()
    await new.edit(position=pos); await new.send("☢️ Canal resetado!")

@bot.tree.command(name="limpar-bot", description="Limpa msgs de bots (Requer Senha)")
async def limpar_bot(interaction: discord.Interaction, quantidade: int, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=quantidade, check=lambda m: m.author.bot)
    await interaction.followup.send(f"🤖 {len(deleted)} msgs limpas!", ephemeral=True)

@bot.tree.command(name="lock-all", description="Tranca tudo (Requer Senha)")
async def lock_all(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for c in interaction.guild.text_channels: await c.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.followup.send("🔒 Canais trancados!", ephemeral=True)

@bot.tree.command(name="set-slow", description="Slowmode global (Requer Senha)")
async def set_slow_all(interaction: discord.Interaction, segundos: int, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for c in interaction.guild.text_channels: await c.edit(slowmode_delay=segundos)
    await interaction.followup.send("🐢 Slowmode global aplicado!", ephemeral=True)

@bot.tree.command(name="votação", description="Cria votação (Requer Senha)")
async def votacao(interaction: discord.Interaction, questao: str, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    embed = discord.Embed(title="🗳️ VOTAÇÃO", description=questao, color=0x00ff00)
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response(); await msg.add_reaction("✅"); await msg.add_reaction("❌")

@bot.tree.command(name="aviso-global", description="Aviso geral (Requer Senha)")
async def aviso_global(interaction: discord.Interaction, mensagem: str, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for c in interaction.guild.text_channels:
        try: await c.send(f"📢 **AVISO GLOBAL:** {mensagem}")
        except: continue
    await interaction.followup.send("✅ Enviado!", ephemeral=True)

@bot.tree.command(name="limpar-tudo", description="Limpa TUDO (Requer Senha)")
async def limpar_tudo(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge()
    await interaction.followup.send("🧹 Limpeza total concluída!", ephemeral=True)

@bot.tree.command(name="role-add", description="Adiciona cargo (Requer Senha)")
async def role_add(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha!", ephemeral=True)
    await membro.add_roles(cargo); await interaction.response.send_message(f"✅ +{cargo.name}")

@bot.tree.command(name="role-remove", description="Remove cargo (Requer Senha)")
async def role_remove(interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha!", ephemeral=True)
    await membro.remove_roles(cargo); await interaction.response.send_message(f"❌ -{cargo.name}")

@bot.tree.command(name="warn", description="Avisa membro (Requer Senha)")
async def warn(interaction: discord.Interaction, membro: discord.Member, motivo: str, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha!", ephemeral=True)
    await interaction.response.send_message(f"⚠️ {membro.mention} avisado: {motivo}")

# ---------------- CATEGORIA: UTILITÁRIOS (18) ---------------- #
@bot.tree.command(name="perfil", description="Veja suas estatísticas")
async def perfil(interaction: discord.Interaction, membro: discord.Member = None):
    membro = membro or interaction.user
    data = load_json(DATA_FILE)
    u = data.get(str(membro.id), {"xp": 0, "level": 1, "coins": 100, "wins": 0})
    embed = discord.Embed(title=f"👤 Perfil: {membro.name}", color=0x3498db)
    embed.add_field(name="Level", value=f"⭐ {u['level']}"); embed.add_field(name="Vitórias", value=f"🏆 {u.get('wins', 0)}")
    embed.add_field(name="Moedas", value=f"💰 {u['coins']}"); embed.set_thumbnail(url=membro.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Mostra avatar")
async def avatar(interaction: discord.Interaction, membro: discord.Member = None):
    membro = membro or interaction.user; await interaction.response.send_message(membro.avatar.url)

@bot.tree.command(name="serverinfo", description="Info servidor")
async def serverinfo(interaction: discord.Interaction):
    g = interaction.guild; await interaction.response.send_message(f"🏰 **{g.name}**\nMembros: {g.member_count}")

@bot.tree.command(name="ping", description="Ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="uptime", description="Uptime")
async def uptime(interaction: discord.Interaction):
    delta = datetime.now() - start_time; await interaction.response.send_message(f"⏰ Online: {str(delta).split('.')[0]}")

@bot.tree.command(name="status", description="Status host")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(f"🖥️ CPU: {psutil.cpu_percent()}%")

@bot.tree.command(name="ajuda", description="Ajuda")
async def ajuda(interaction: discord.Interaction):
    await interaction.response.send_message("📚 Use `/` para ver todos os comandos!")

@bot.tree.command(name="calculadora", description="Calc")
async def calc(interaction: discord.Interaction, conta: str):
    try: await interaction.response.send_message(f"🧮 {eval(conta, {'__builtins__': None}, {})}")
    except: await interaction.response.send_message("❌ Erro!")

@bot.tree.command(name="id", description="ID")
async def mostrar_id(interaction: discord.Interaction, alvo: str = None):
    await interaction.response.send_message(f"🆔 ID: {alvo or interaction.user.id}")

@bot.tree.command(name="membros-count", description="Count")
async def membros_count(interaction: discord.Interaction):
    await interaction.response.send_message(f"👥 Membros: {interaction.guild.member_count}")

@bot.tree.command(name="tempo", description="Hora")
async def tempo(interaction: discord.Interaction):
    await interaction.response.send_message(f"🕒 Hora: {datetime.now().strftime('%H:%M:%S')}")

@bot.tree.command(name="clima", description="Clima")
async def clima_nerd(interaction: discord.Interaction):
    await interaction.response.send_message("☁️ Clima gamer!")

@bot.tree.command(name="versão", description="Versão")
async def versao(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 Versão 3.0.0")

@bot.tree.command(name="site", description="Site")
async def site(interaction: discord.Interaction):
    await interaction.response.send_message("🌐 Site: https://qg-nerd.lovable.app")

@bot.tree.command(name="regras", description="Regras")
async def regras(interaction: discord.Interaction):
    await interaction.response.send_message("📜 Respeito!")

@bot.tree.command(name="invite", description="Convite bot")
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message("🔗 Convide-me para seu servidor!")

@bot.tree.command(name="botinfo", description="Info bot")
async def botinfo(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 Sou o QG Nerd Bot, seu assistente gamer!")

@bot.tree.command(name="top-xp", description="Ranking de XP")
async def top_xp(interaction: discord.Interaction):
    data = load_json(DATA_FILE)
    sorted_data = sorted(data.items(), key=lambda x: x[1]['xp'], reverse=True)[:5]
    res = "\n".join([f"#{i+1} - ID {uid}: {d['xp']} XP" for i, (uid, d) in enumerate(sorted_data)])
    await interaction.response.send_message(f"🏆 **Top 5 XP:**\n{res}")

# ---------------- CATEGORIA: DIVERSÃO / GAME ACTIONS (40+) ---------------- #
@bot.tree.command(name="game-actions", description="Jogos grátis")
async def free_games(interaction: discord.Interaction):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as s:
        async with s.get("https://www.gamerpower.com/api/giveaways?platform=pc") as r:
            if r.status == 200:
                data = await r.json(); embed = discord.Embed(title="🎮 Jogos Grátis", color=0x00ff00)
                for g in data[:3]: embed.add_field(name=g['title'], value=f"🔗 [Pegar]({g['open_giveaway_url']})", inline=False)
                await interaction.followup.send(embed=embed)
            else: await interaction.followup.send("❌ Erro!")

@bot.tree.command(name="dado", description="Dado")
async def dado(interaction: discord.Interaction, lados: int = 20):
    await interaction.response.send_message(f"🎲 Resultado: {random.randint(1, lados)}")

@bot.tree.command(name="moeda", description="Moeda")
async def moeda(interaction: discord.Interaction):
    await interaction.response.send_message(f"🪙 {random.choice(['Cara', 'Coroa'])}")

@bot.tree.command(name="abraço", description="Abraço com gif")
async def abraco(interaction: discord.Interaction, membro: discord.Member):
    embed = discord.Embed(description=f"🤗 {interaction.user.mention} abraçou {membro.mention}!", color=0xff69b4)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2o0eXN4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/PHZ7v9tfQu0o0/giphy.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="beijo", description="Beijo com gif")
async def beijo(interaction: discord.Interaction, membro: discord.Member):
    embed = discord.Embed(description=f"💋 {interaction.user.mention} beijou {membro.mention}!", color=0xff1493)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2o0eXN4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/K7I83F28mX7Qk/giphy.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="tapa", description="Tapa com gif")
async def tapa(interaction: discord.Interaction, membro: discord.Member):
    embed = discord.Embed(description=f"🖐️ {interaction.user.mention} deu um tapa em {membro.mention}!", color=0xff0000)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2o0eXN4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/tX29JK3EOnAs/giphy.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="comer", description="Comer com gif")
async def comer(interaction: discord.Interaction):
    embed = discord.Embed(description=f"😋 {interaction.user.mention} está comendo!", color=0xffa500)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2o0eXN4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4eXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/11pxf84G6Wb7P2/giphy.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="café", description="Café")
async def cafe(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"☕ {interaction.user.mention} deu um café para {membro.mention}!")

@bot.tree.command(name="meme", description="Meme")
async def meme(interaction: discord.Interaction):
    await interaction.response.send_message(f"🤡 {random.choice(['Enfim.', 'É isso.'])}")

@bot.tree.command(name="sorte", description="Sorte")
async def sorte(interaction: discord.Interaction):
    await interaction.response.send_message(f"🔮 Sorte: {random.randint(0, 100)}%")

@bot.tree.command(name="8ball", description="8Ball")
async def ball8(interaction: discord.Interaction, pergunta: str):
    await interaction.response.send_message(f"🎱 Pergunta: {pergunta}\n✨ Resposta: {random.choice(['Sim', 'Não', 'Talvez'])}")

@bot.tree.command(name="ship", description="Ship")
async def ship(interaction: discord.Interaction, m1: discord.Member, m2: discord.Member):
    await interaction.response.send_message(f"❤️ Amor entre {m1.name} e {m2.name}: {random.randint(0, 100)}%")

@bot.tree.command(name="clap", description="Palmas")
async def clap(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"👏 Aplausos para {membro.mention}!")

@bot.tree.command(name="dance", description="Dança")
async def dance(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"💃 Dançando com {membro.mention}!")

@bot.tree.command(name="roleta-russa", description="Roleta")
async def roleta(interaction: discord.Interaction):
    if random.randint(1, 6) == 1: await interaction.response.send_message(f"💥 {interaction.user.mention} morreu!")
    else: await interaction.response.send_message(f"🔫 {interaction.user.mention} sobreviveu!")

@bot.tree.command(name="chutar", description="Chute")
async def chutar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"🦵 {interaction.user.mention} chutou {membro.mention}!")

@bot.tree.command(name="murro", description="Murro")
async def murro(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"👊 {interaction.user.mention} socou {membro.mention}!")

@bot.tree.command(name="atirar", description="Atirar")
async def atirar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"🔫 {interaction.user.mention} atirou em {membro.mention}!")

@bot.tree.command(name="carinho", description="Carinho")
async def carinho(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"🐱 {interaction.user.mention} fez carinho em {membro.mention}!")

@bot.tree.command(name="dormir", description="Zzz")
async def dormir(interaction: discord.Interaction):
    await interaction.response.send_message(f"😴 {interaction.user.mention} dormiu!")

@bot.tree.command(name="acordar", description="Acordar")
async def acordar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"⏰ Acordando {membro.mention}!")

@bot.tree.command(name="beber", description="Beber")
async def beber(interaction: discord.Interaction):
    await interaction.response.send_message(f"🍹 Bebeu poção!")

@bot.tree.command(name="assustar", description="Susto")
async def assustar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"👻 BÚ {membro.mention}!")

@bot.tree.command(name="vômito", description="Nojo")
async def vomito(interaction: discord.Interaction):
    await interaction.response.send_message(f"🤮 Que nojo!")

@bot.tree.command(name="chorar", description="Choro")
async def chorar(interaction: discord.Interaction):
    await interaction.response.send_message(f"😭 Buááá!")

@bot.tree.command(name="abraçar-todos", description="Abraça todo mundo")
async def abraca_geral(interaction: discord.Interaction):
    await interaction.response.send_message("🫂 O bot deu um abraço coletivo em todo mundo! Que amor!")

@bot.tree.command(name="morrer", description="Faleça")
async def morrer(interaction: discord.Interaction):
    await interaction.response.send_message(f"💀 {interaction.user.mention} faleceu. RIP.")

@bot.tree.command(name="ressuscitar", description="Reviva alguém")
async def ressuscita(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"😇 {interaction.user.mention} usou uma Fênix em {membro.mention}! Ele reviveu!")

@bot.tree.command(name="gritar", description="Grite bem alto")
async def gritar(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message(f"🗣️ {interaction.user.mention} GRITOU: **{msg.upper()}**")

@bot.tree.command(name="medo", description="Sinta medo")
async def medo(interaction: discord.Interaction):
    await interaction.response.send_message(f"😨 {interaction.user.mention} está com muito medo!")

@bot.tree.command(name="irritar", description="Irrite alguém")
async def irritar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"💢 {interaction.user.mention} está irritando {membro.mention}! Parem!")

@bot.tree.command(name="festa", description="Festa!")
async def festa(interaction: discord.Interaction):
    await interaction.response.send_message(f"🥳 {interaction.user.mention} começou uma festa! Uhuuu!")

@bot.tree.command(name="ataque-nerd", description="Ataque geek")
async def ataque_nerd(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"⚔️ {interaction.user.mention} atacou {membro.mention} com um d20!")

@bot.tree.command(name="casar", description="Peça em casamento")
async def casar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"💍 {interaction.user.mention} pediu {membro.mention} em casamento!")

@bot.tree.command(name="divorciar", description="Divórcio")
async def divorciar(interaction: discord.Interaction, membro: discord.Member):
    await interaction.response.send_message(f"💔 {interaction.user.mention} se divorciou de {membro.mention}!")

@bot.tree.command(name="trabalhar", description="Trabalhe para moedas")
async def trabalhar(interaction: discord.Interaction):
    ganho = random.randint(10, 50); update_member(interaction.user.id, coins=ganho)
    await interaction.response.send_message(f"💼 Você trabalhou e ganhou {ganho} moedas!")

@bot.tree.command(name="roubar", description="Tente roubar alguém")
async def roubar(interaction: discord.Interaction, membro: discord.Member):
    if random.choice([True, False]):
        update_member(interaction.user.id, coins=20); await interaction.response.send_message(f"💰 Você roubou 20 moedas de {membro.mention}!")
    else: await interaction.response.send_message(f"👮 Você foi pego tentando roubar {membro.mention}!")

@bot.tree.command(name="pagar", description="Dê moedas")
async def pagar(interaction: discord.Interaction, membro: discord.Member, quantia: int):
    update_member(interaction.user.id, coins=-quantia); update_member(membro.id, coins=quantia)
    await interaction.response.send_message(f"💸 Você pagou {quantia} moedas para {membro.mention}!")

@bot.tree.command(name="slot", description="Cassino slots")
async def slot(interaction: discord.Interaction):
    icons = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    res = [random.choice(icons) for _ in range(3)]
    msg = " | ".join(res)
    if res[0] == res[1] == res[2]: await interaction.response.send_message(f"{msg}\n🏆 GANHOU!")
    else: await interaction.response.send_message(f"{msg}\n❌ PERDEU!")

# ---------------- CATEGORIA: CLÃS E BATALHAS ---------------- #
@bot.tree.command(name="clã-criar", description="Crie um clã (500 moedas)")
async def clan_create(interaction: discord.Interaction, nome: str):
    data = load_json(DATA_FILE); clans = load_json(CLANS_FILE); uid = str(interaction.user.id)
    if data.get(uid, {}).get("coins", 0) < 500: return await interaction.response.send_message("❌ Saldo insuficiente!", ephemeral=True)
    data[uid]["coins"] -= 500; clans[uid] = {"name": nome, "leader": interaction.user.name, "members": [uid], "wins": 0}
    save_json(DATA_FILE, data); save_json(CLANS_FILE, clans); await interaction.response.send_message(f"🚩 Clã **{nome}** criado!")

class BattleView(discord.ui.View):
    def __init__(self, p1, p2):
        super().__init__(timeout=60); self.p1, self.p2 = p1, p2; self.h1, self.h2 = 100, 100; self.turn = p1
    def get_embed(self, action="Duelo!"):
        e = discord.Embed(title="⚔️ BATALHA", description=action, color=0xff0000)
        e.add_field(name=f"👤 {self.p1.name}", value=f"HP: {self.h1}%\n{'🟩'*(self.h1//10)}{'🟥'*(10-self.h1//10)}", inline=False)
        e.add_field(name=f"👤 {self.p2.name}", value=f"HP: {self.h2}%\n{'🟩'*(self.h2//10)}{'🟥'*(10-self.h2//10)}", inline=False)
        return e
    @discord.ui.button(label="Atacar", style=discord.ButtonStyle.danger)
    async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.turn: return await interaction.response.send_message("Vez do outro!", ephemeral=True)
        dmg = random.randint(10, 30)
        if self.turn == self.p1: self.h2 = max(0, self.h2 - dmg); self.turn = self.p2
        else: self.h1 = max(0, self.h1 - dmg); self.turn = self.p1
        if self.h1 <= 0 or self.h2 <= 0:
            winner = self.p1 if self.h2 <= 0 else self.p2; update_member(winner.id, xp=100, coins=200, win=True); self.clear_items()
            return await interaction.response.edit_message(embed=self.get_embed(f"🏆 {winner.name} VENCEU!"), view=self)
        await interaction.response.edit_message(embed=self.get_embed(f"💥 Dano: {dmg}%"))

@bot.tree.command(name="batalha", description="Inicia duelo")
async def battle(interaction: discord.Interaction, oponente: discord.Member):
    if oponente == interaction.user: return await interaction.response.send_message("Lute consigo mesmo não!")
    view = BattleView(interaction.user, oponente); await interaction.response.send_message(embed=view.get_embed(), view=view)

# ---------------- ADMIN & SETUP (Senha: 030912) ---------------- #
@bot.tree.command(name="qg-admin", description="Admin Panel (Senha: 030912)")
async def qg_admin(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.send_message("🛡️ Admin Logged!", ephemeral=True)

@bot.tree.command(name="setup-qg", description="Setup (Senha: 030912)")
async def setup(interaction: discord.Interaction, senha: str):
    if senha != ADMIN_PASSWORD: return await interaction.response.send_message("❌ Senha incorreta!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for c in ["📢-avisos", "📜-regras", "💬-chat-geral", "🤖-ia-chat"]:
        if not discord.utils.get(interaction.guild.channels, name=c): await interaction.guild.create_text_channel(c)
    await interaction.followup.send("✅ Canais criados!", ephemeral=True)

# ---------------- EVENTOS ---------------- #
@tasks.loop(seconds=1)
async def status_loop():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="QG Nerd! 🤓"))

@bot.event
async def on_message(message):
    if not message.author.bot: update_member(message.author.id, xp=1, coins=1)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    global start_time; start_time = datetime.now(); await bot.tree.sync(); status_loop.start(); print("✅ ONLINE")

if __name__ == "__main__":
    keep_alive(); bot.run(TOKEN_DISCORD)
