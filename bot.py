import discord
from discord.ext import commands
from discord import File
import io

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Banco simples
builds = {}

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}')

# Criar build
@bot.command()
async def criar(ctx, nome):
    builds[nome] = "Build vazia."
    await ctx.send(f'✅ Build "{nome}" criada.')


# Editar build
@bot.command()
async def editar(ctx, nome, *, conteudo):

    builds[nome] = conteudo

    # Apaga mensagens antigas do canal
    await ctx.channel.purge(limit=100)

    txt = io.StringIO(conteudo)

    arquivo = File(
        fp=io.BytesIO(txt.getvalue().encode()),
        filename=f"{nome}.txt"
    )

    await ctx.send(
        f'✅ Build "{nome}" atualizada.',
        file=arquivo
    )


# Ver build
@bot.command()
async def ver(ctx, nome):

    if nome in builds:
        await ctx.send(f"```{builds[nome]}```")
    else:
        await ctx.send("❌ Build não encontrada.")

import os

bot.run(os.getenv("TOKEN"))