import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
import colorama
from tabulate import tabulate
from colorama import Fore, Style

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Carga la configuración desde el archivo configuracion.json
with open('configuracion.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Carga los mensajes de anuncio desde el archivo mensajes_anuncio.json
with open('mensajes_anuncio.json', 'r', encoding='utf-8') as mensajes_file:
    mensajes_anuncio = json.load(mensajes_file)

# Carga las IDs de los servidores desde el archivo servidores_ids.json
with open('servidores_ids.json', 'r', encoding='utf-8') as servidores_file:
    servidores_ids = json.load(servidores_file)

# Carga las IDs de los canales de anuncio desde el archivo canales_ids_anuncio.json
with open('canales_ids_anuncio.json', 'r', encoding='utf-8') as canales_file:
    canales_ids_anuncio = json.load(canales_file)

# Configura el intervalo de tiempo entre cada anuncio (en segundos)
intervalo_anuncio_min = config['intervalo_anuncio_min']
intervalo_anuncio_max = config['intervalo_anuncio_max']

# Configura el intervalo de tiempo entre cada DM (en segundos)
intervalo_dm = config['intervalo_dm']

# Inicializa colorama
colorama.init()

bot = commands.Bot(command_prefix='$')


def mostrar_registros(registros):
    headers = [f"{Fore.CYAN}Canal{Style.RESET_ALL}",
               f"{Fore.CYAN}Estado{Style.RESET_ALL}"]
    registros_table = []

    for canal_id, estado in registros.items():
        canal = bot.get_channel(canal_id)
        registros_table.append([canal.name, estado])

    print(tabulate(registros_table, headers=headers))


# Evento de inicio del bot
@bot.event
async def on_ready():
    print('[+] Esperando a que el bot esté listo...')
    print('[+] El bot está listo')

    registros_canales = {}

    # Comprueba si se pueden enviar mensajes en todos los canales
    for canal_id in canales_ids_anuncio:
        canal = bot.get_channel(canal_id)

        if not canal.permissions_for(canal.guild.me).send_messages:
            registros_canales[canal_id] = f"{Fore.RED}No se pueden enviar mensajes"
        else:
            registros_canales[canal_id] = f"{Fore.GREEN}Se puede enviar mensajes"

    mostrar_registros(registros_canales)

    # Inicia las tareas de envío de anuncios y DMs periódicos
    enviar_anuncio_loop.start()
    enviar_dm_loop.start()


@tasks.loop(hours=1)
async def enviar_anuncio_loop():
    await enviar_anuncio()


@tasks.loop(seconds=intervalo_dm)
async def enviar_dm_loop():
    await enviar_dm()


async def enviar_anuncio():
    if len(canales_ids_anuncio) == 0:
        print(f'{Fore.YELLOW}No hay canales disponibles para enviar anuncios en este momento.{Style.RESET_ALL}')
        return

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
                    f'[+] Mensaje enviado en el canal: {canal_anuncio.name}')
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


async def enviar_dm():
    for server_id in servidores_ids:
        server = bot.get_guild(server_id)

        if server is None:
            print(
                f'{Fore.RED}No se encontró el servidor con ID: {server_id}{Style.RESET_ALL}')
            continue

        users = server.members

        if len(users) < config['num_usuarios_dm']:
            print(
                f'{Fore.YELLOW}No hay suficientes usuarios en el servidor con ID: {server_id}{Style.RESET_ALL}')
            continue

        usuarios_seleccionados = random.sample(
            users, config['num_usuarios_dm'])

        for usuario in usuarios_seleccionados:
            try:
                dm_channel = await usuario.create_dm()
                mensaje_dm = random.choice(config['mensajes_dm'])
                mensaje = mensaje_dm['mensaje']
                imagenes_adjuntas = []

                if mensaje_dm['adjuntar_fotos']:
                    for ruta_imagen in config['rutas_imagenes']:
                        with open(ruta_imagen, 'rb') as imagen_file:
                            imagen_adjunta = discord.File(imagen_file)
                            imagenes_adjuntas.append(imagen_adjunta)

                await dm_channel.send(content=mensaje, files=imagenes_adjuntas)
                print(
                    f'[+] Mensaje enviado a {usuario.name}#{usuario.discriminator}')
            except discord.Forbidden:
                print(
                    f'{Fore.YELLOW}No se puede enviar DM a {usuario.name}#{usuario.discriminator} - Saltando...{Style.RESET_ALL}')
                continue
            except Exception as e:
                print(
                    f'{Fore.RED}Error al enviar DM a {usuario.name}#{usuario.discriminator} - {e}{Style.RESET_ALL}')
                continue


@enviar_anuncio_loop.before_loop
async def before_enviar_anuncio_loop():
    print('[+] Esperando a que el bot esté listo...')
    await bot.wait_until_ready()


@enviar_dm_loop.before_loop
async def before_enviar_dm_loop():
    print('[+] Esperando a que el bot esté listo...')
    await bot.wait_until_ready()


# Inicia el bot
bot.run(TOKEN, bot=False)
