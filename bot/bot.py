import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
import colorama
from colorama import Fore, Style

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Carga la configuración desde el archivo configuracion.json
with open('configuracion.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Carga los mensajes de anuncio desde el archivo mensajes_anuncio.json
with open('mensajes_anuncio.json', 'r', encoding='utf-8') as mensajes_file:
    mensajes_anuncio = json.load(mensajes_file)

# Carga las IDs de los canales de anuncio desde el archivo canales_ids_anuncio.json
with open('canales_ids_anuncio.json', 'r', encoding='utf-8') as canales_file:
    canales_ids_anuncio = json.load(canales_file)

# Configura el intervalo de tiempo entre cada anuncio (en segundos)
intervalo_anuncio_min = config['intervalo_anuncio_min']
intervalo_anuncio_max = config['intervalo_anuncio_max']

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print(f'{Fore.GREEN}El bot está listo{Style.RESET_ALL}')
    await check_permissions()


async def check_permissions():
    for canal_id in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)
        if canal_anuncio.permissions_for(canal_anuncio.guild.me).send_messages:
            print(
                f'{Fore.GREEN}Se puede enviar mensajes en el canal: {canal_anuncio.name}{Style.RESET_ALL}')
        else:
            print(
                f'{Fore.YELLOW}No se puede enviar mensajes en el canal: {canal_anuncio.name}{Style.RESET_ALL}')
            canales_ids_anuncio.remove(canal_id)
            print(
                f'{Fore.RED}Eliminada la ID del canal: {canal_id} del archivo canales_ids_anuncio.json{Style.RESET_ALL}')

    with open('canales_ids_anuncio.json', 'w', encoding='utf-8') as canales_file:
        json.dump(canales_ids_anuncio, canales_file, indent=4)

    if len(canales_ids_anuncio) == 0:
        print(f'{Fore.RED}No hay canales disponibles para enviar anuncios. Por favor, añade canales válidos.{Style.RESET_ALL}')


@tasks.loop(seconds=random.randint(intervalo_anuncio_min, intervalo_anuncio_max))
async def enviar_anuncio():
    if len(canales_ids_anuncio) == 0:
        print(f'{Fore.YELLOW}No hay canales disponibles para enviar anuncios en este momento.{Style.RESET_ALL}')
        return

    oleada = random.randint(1, 1000)

    for canal_id in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)

        try:
            if canal_anuncio.permissions_for(canal_anuncio.guild.me).send_messages:
                mensaje_anuncio = random.choice(mensajes_anuncio)
                mensaje = mensaje_anuncio['mensaje']
                imagenes_adjuntas = []

                if mensaje_anuncio['adjuntar_fotos']:
                    for ruta_imagen in config['rutas_imagenes']:
                        with open(ruta_imagen, 'rb') as imagen_file:
                            imagen_adjunta = discord.File(imagen_file)
                            imagenes_adjuntas.append(imagen_adjunta)

                await canal_anuncio.send(content=mensaje, files=imagenes_adjuntas)
                print(
                    f'{Fore.CYAN}Mensaje enviado en el canal: {canal_anuncio.name} - Oleada: {oleada}{Style.RESET_ALL}')
            else:
                print(
                    f'{Fore.YELLOW}No se puede enviar mensajes en el canal: {canal_anuncio.name} - Saltando...{Style.RESET_ALL}')
                continue
        except discord.Forbidden:
            print(f'{Fore.RED}No tengo permisos para enviar mensajes en el canal: {canal_anuncio.name} - Saltando...{Style.RESET_ALL}')
            continue
        except Exception as e:
            print(
                f'{Fore.RED}Error al enviar mensaje en el canal: {canal_anuncio.name} - {e}{Style.RESET_ALL}')
            continue


@enviar_anuncio.before_loop
async def before_enviar_anuncio():
    print(f'{Fore.GREEN}Esperando a que el bot esté listo...{Style.RESET_ALL}')
    await bot.wait_until_ready()

# Guarda la invitación permanente de cada servidor y su nombre en un archivo .txt


async def guardar_invitaciones():
    with open('invitaciones_servidores.txt', 'w', encoding='utf-8') as invitaciones_file:
        for guild in bot.guilds:
            invite = await guild.invites()
            if invite:
                invitacion = invite[0]
                invitaciones_file.write(
                    f'Servidor: {guild.name} - Invitación: {invitacion.url}\n')
                print(
                    f'{Fore.GREEN}Guardada la invitación del servidor: {guild.name}{Style.RESET_ALL}')
            else:
                print(
                    f'{Fore.YELLOW}No se pudo obtener la invitación del servidor: {guild.name}{Style.RESET_ALL}')

# Evento que se ejecuta cuando el bot se conecta a un servidor


@bot.event
async def on_guild_join(guild):
    await guardar_invitaciones()

# Evento que se ejecuta cuando el bot es expulsado de un servidor


@bot.event
async def on_guild_remove(guild):
    await guardar_invitaciones()
    for canal_id in canales_ids_anuncio:
        if bot.get_channel(canal_id).guild == guild:
            canales_ids_anuncio.remove(canal_id)
            print(f'{Fore.RED}Eliminada la ID del canal: {canal_id} del archivo canales_ids_anuncio.json debido a la expulsión del servidor{Style.RESET_ALL}')

# Evento que se ejecuta cuando el bot es baneado de un servidor


@bot.event
async def on_guild_ban(guild, user):
    await guardar_invitaciones()
    for canal_id in canales_ids_anuncio:
        if bot.get_channel(canal_id).guild == guild:
            canales_ids_anuncio.remove(canal_id)
            print(f'{Fore.RED}Eliminada la ID del canal: {canal_id} del archivo canales_ids_anuncio.json debido al banneo del servidor{Style.RESET_ALL}')

# Ejecuta el loop para enviar los anuncios
enviar_anuncio.start()
# Ejecuta la tarea para guardar las invitaciones de los servidores
bot.loop.create_task(guardar_invitaciones())
# Inicia el bot
bot.run(TOKEN, bot=False)
