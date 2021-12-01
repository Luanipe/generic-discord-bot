# -*- coding: utf-8 -*-
import discord
from discord import colour
from discord.ext import commands
from discord.ext.commands.core import command
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
from youtube_search import YoutubeSearch

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
    
    @commands.command(name="entrar")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz! :crying_cat_face:")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(name="sair")
    async def disconnect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz! :crying_cat_face:")
        else:
            await ctx.voice_client.disconnect()

    @commands.command(name="tocar")
    async def play(self, ctx, *text):
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
        YDL_OPTIONS = {'format':'bestaudio'} 
        # Pega a pesquisa em tupla e converte para uma única string, sendo a URL
        link = " ".join(text)
        result = YoutubeSearch(link, max_results=1).to_dict()
        url = f"https://www.youtube.com{result[0]['url_suffix']}"
        
        # Mostra as informações do vídeo que está sendo tocado
        embed = discord.Embed(colour=discord.Colour.green())
        embed.add_field(name="Tocando :notes:", value=f"`{result[0]['title']}`", inline=False)
        
        # Caso o bot esteja fora do canal de voz
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        
        # Ativa as configurações e toca a música da URL
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            await ctx.send(embed=embed)
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS) 
            vc.play(source)

    @commands.command(name="pausar")
    async def pause(sef, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz! :crying_cat_face:")
        else:
            await ctx.send("Pausado! :pause_button:")
            await ctx.voice_client.pause()
        
    @commands.command()
    async def resume(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz! :crying_cat_face:")
        else:
            await ctx.send("Continuando! :arrow_forward:")
            await ctx.voice_client.resume()

    @commands.command(name="parar")
    async def stop(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz! :crying_cat_face:")
        else:            
            await ctx.send("Parou! :stop_button:")
            await ctx.voice_client.stop()

def setup(client):
    client.add_cog(music(client))