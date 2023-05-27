import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
import colorama
from colorama import Fore, Style

TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Cargar configuración desde archivo
with open('configuracion.json', 'rb') as file:
    configuracion = json.load(file)

# Cargar mensajes de anuncio desde archivo
with open('mensajes_anuncio.json', 'rb') as file:
    mensajes_anuncio = json.load(file)

# Cargar IDs de canales de anuncio desde archivo
with open('canales_ids_anuncio.json', 'rb') as file:
    canales_ids_anuncio = json.load(file)

bot = commands.Bot(command_prefix='$')

intervalo_anuncio = configuracion['intervalo_anuncio']

# Inicializar colorama para los colores de la consola
colorama.init()


@bot.event
async def on_ready():
    print('El bot está listo')
    enviar_anuncio.current_oleada = 0
    enviar_anuncio.start()


@tasks.loop(seconds=intervalo_anuncio)
async def enviar_anuncio():
    enviar_anuncio.current_oleada += 1
    for canal_id in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)
        mensaje_anuncio = random.choice(mensajes_anuncio)
        mensaje = mensaje_anuncio['mensaje']
        enviar_fotos = mensaje_anuncio['enviar_fotos']

        if enviar_fotos:
            imagenes_adjuntas = []
            for ruta_imagen in configuracion['rutas_imagenes']:
                with open(ruta_imagen, 'rb') as imagen:
                    imagenes_adjuntas.append(discord.File(imagen))
            await canal_anuncio.send(content=mensaje, files=imagenes_adjuntas)
        else:
            await canal_anuncio.send(content=mensaje)

        registrar_envio(canal_id, enviar_anuncio.current_oleada)


def registrar_envio(canal_id, oleada):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mensaje_log = f"[{timestamp}] Mensaje enviado al canal {canal_id} en la oleada {oleada}"

    # Colores y decoración para el registro de log
    color = Fore.GREEN
    estilo = Style.BRIGHT

    # Imprimir registro de log con colores y decoración
    print(f"{color}{estilo}{mensaje_log}{Style.RESET_ALL}")


@bot.command()
async def ayuda(ctx):
    print('[?] Mensaje de ayuda enviado')
    embed = discord.Embed(
        title="Bot de Ayuda", description="¡Hola! Soy el bot de ayuda.", color=discord.Color.blue())
    embed.add_field(name="Instrucciones:",
                    value="Para usar este bot, sigue los siguientes pasos:")
    embed.add_field(name="1. Iniciar envío de anuncios y mensajes directos:",
                    value="Usa el comando `!start`.", inline=False)
    embed.add_field(name="2. Detener envío de anuncios y mensajes directos:",
                    value="Usa el comando `!stop`.", inline=False)

    await ctx.author.send(embed=embed)


@bot.command()
async def start(ctx):
    enviar_anuncio.current_oleada = 0
    enviar_anuncio.start()
    await ctx.send('El envío de anuncios y mensajes directos ha comenzado')


@bot.command()
async def stop(ctx):
    enviar_anuncio.cancel()
    await ctx.send('El envío de anuncios y mensajes directos ha sido detenido')

bot.run(TOKEN, bot=False)
