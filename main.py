# -*- coding: utf-8 -*-
import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import asyncio
import music

# Prefixo do bot
bot = commands.Bot(command_prefix=".", intents = discord.Intents.all())

# Remove o comando 'help' padrão do bot
bot.remove_command('help')

### Funções EVENT ###

# Mensagem de inicialização do bot
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="tatu na farofa"))
    print(f"Estou pronto e operando como {bot.user}!")

# Função on_message e suas operações
@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send(f"Olá, {message.author.mention}! Se precisar de algo, pode encontrar utilizando o comando `.ajuda`")
    await bot.process_commands(message)

### Funções personalizadas ###

# Função que retorna o ping do bot em ms
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong!")
    await ctx.send(f"Latência: {round(bot.latency * 1000)}ms")


# Função para kickar alguém do servidor
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):   
    await member.kick(reason=reason)
# Mensagem de erro da função "kick"
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Desculpe {ctx.author.mention}, mas você não tem permissão para isso! :face_with_monocle:")

    
# Função para banir alguém do servidr
@bot.command(name="banir")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
# Mensagem de erro da função "banir"
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Desculpe {ctx.author.mention}, mas você não tem permissão para isso! :face_with_monocle:")


# Função para limpar o chat
@bot.command(name="limpar")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=17):
    await ctx.send(f"Seu pedido é uma ordem, {ctx.author.mention}! :smiley_cat:")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=amount)
# Mensagem de erro da função "limpar"
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"Desculpe {ctx.author.mention}, mas você não tem permissão para isso! :face_with_monocle:")


# Função de ajuda para exibir os comandos
@bot.command(name="ajuda")
async def help(ctx):
    author = ctx.message.author.mention
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name="Comandos do Bot")
    embed.add_field(name=".ping", value="Retorna uma resposta do bot junto à latência.", inline=False)
    embed.add_field(name=".limpar `número`", value="Limpa o as últimas 15 (ou mais) mensagens do canal. Somente quem tem permissão pode usar este comando.", inline=False)
    embed.add_field(name=".kick `@usuário` `motivo`", value="Expulsa o @ marcado do servidor. Somente quem tem permissão pode usar este comando.", inline=False)
    embed.add_field(name=".banir `@usuário` `motivo`", value="Bane o @ marcado do servidor. Somente quem tem permissão pode usar este comando.", inline=False)
    embed.add_field(name=".entrar", value="Conecta o bot ao canal de voz.", inline=False)
    embed.add_field(name=".sair", value="Desconecta o bot do canal de voz", inline=False)
    embed.add_field(name=".tocar `link ou pesquisa do youtube`", value="Toca um link de um vídeo do youtube no canal de voz que se encontra o bot.", inline=False)
    embed.add_field(name=".pausar", value="Pausa o que está tocando no bot.", inline=False)
    embed.add_field(name=".resume", value="Continua tocando o que estava pausado.", inline=False)
    embed.add_field(name=".parar", value="Para a música que está tocando de uma vez.", inline=False)
    await ctx.send(author, embed=embed)


# Música
cogs = [music]
for i in range(len(cogs)):
    cogs[i].setup(bot)

### Token sempre abaixo do código ###

# Token único do bot
bot.run("TOKEN_HERE")