import discord
from discord.ext import commands, tasks
import asyncio
import random
import json

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Ruta del archivo de configuración de mensajes de anuncio
ARCHIVO_MENSAJES_ANUNCIO = 'mensajes_anuncio.json'

# Ruta del archivo de configuración de IDs de canales
ARCHIVO_IDS_CANALES = 'ids_canales.json'

# Configura el intervalo de tiempo entre cada anuncio (en segundos)
intervalo_anuncio = 3600  # 1 hora = 3600 segundos

bot = commands.Bot(command_prefix='$')

# Cargar mensajes de anuncio desde archivo JSON


def cargar_mensajes_anuncio():
    with open(ARCHIVO_MENSAJES_ANUNCIO, 'rb') as archivo:
        mensajes_anuncio = json.load(archivo)
    return mensajes_anuncio

# Cargar IDs de canales desde archivo JSON


def cargar_ids_canales():
    with open(ARCHIVO_IDS_CANALES, 'rb') as archivo:
        ids_canales = json.load(archivo)
    return ids_canales


@bot.event
async def on_ready():
    print('El bot está listo')
    enviar_anuncio.start()


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


@tasks.loop(seconds=intervalo_anuncio)
async def enviar_anuncio():
    ids_canales = cargar_ids_canales()
    mensajes_anuncio = cargar_mensajes_anuncio()

    for canal_id in ids_canales:
        canal_anuncio = bot.get_channel(canal_id)

        # Selecciona un mensaje aleatorio
        mensaje_anuncio = random.choice(mensajes_anuncio)

        mensaje = mensaje_anuncio['mensaje']
        adjuntar_fotos = mensaje_anuncio.get('adjuntar_fotos', False)

        if adjuntar_fotos:
            await enviar_anuncio_con_fotos(canal_anuncio, mensaje)
        else:
            await enviar_anuncio_sin_fotos(canal_anuncio, mensaje)


async def enviar_anuncio_con_fotos(canal_anuncio, mensaje):
    # Configura las rutas de las imágenes que deseas adjuntar en los anuncios
    rutas_imagenes = ['fotos/150.jpg', 'fotos/350.jpg',
                      'fotos/750.jpg']  # Rutas de las imágenes

    await canal_anuncio.send(mensaje)

    for ruta_imagen in rutas_imagenes:
        with open(ruta_imagen, 'rb') as imagen:
            await canal_anuncio.send(file=discord.File(imagen))


async def enviar_anuncio_sin_fotos(canal_anuncio, mensaje):
    await canal_anuncio.send(mensaje)


@bot.command()
async def start(ctx):
    enviar_anuncio.start()
    await ctx.send('El envío de anuncios y mensajes directos ha comenzado')


@bot.command()
async def stop(ctx):
    enviar_anuncio.cancel()
    await ctx.send('El envío de anuncios y mensajes directos ha sido detenido')

bot.run(TOKEN, bot=False)
