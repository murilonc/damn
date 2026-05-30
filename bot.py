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
mensagens_build = {}

@bot.event
async def on_ready():
    print(f'Bot online como {bot.user}')

# Criar build
@bot.command()
async def criar(ctx, nome):

    await ctx.message.delete()  # apaga o comando

    builds[nome] = "Build vazia."

    nova_msg = await ctx.send(
        f'📌 BUILD: {nome}\n```Build vazia.```'
    )

    mensagens_build[nome] = nova_msg.id


# Editar build
@bot.command()
async def editar(ctx, nome, *, conteudo):

        await ctx.message.delete()  # apaga o comando

    builds[nome] = conteudo

    # Apaga a mensagem antiga desta build
    if nome in mensagens_build:
        try:
            msg_antiga = await ctx.channel.fetch_message(
                mensagens_build[nome]
            )
            await msg_antiga.delete()
        except:
            pass

    txt = io.StringIO(conteudo)

    arquivo = File(
        fp=io.BytesIO(txt.getvalue().encode()),
        filename=f"{nome}.txt"
    )

    nova_msg = await ctx.send(
        f'📌 BUILD: {nome}',
        file=arquivo
    )

    mensagens_build[nome] = nova_msg.id


# Ver build
@bot.command()
async def ver(ctx, nome):

    if nome in builds:
        await ctx.send(f"```{builds[nome]}```")
    else:
        await ctx.send("❌ Build não encontrada.")

import os

bot.run(os.getenv("TOKEN"))