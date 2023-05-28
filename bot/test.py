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


# Funciones para registrar y cargar usuarios DM enviados previamente
def registrar_usuario_dm_enviado(servidor_id, usuario_id):
    # Carga los usuarios DM enviados previamente desde el archivo
    usuarios_dm_enviados = cargar_usuarios_dm_enviados()

    # Agrega el ID del usuario enviado a la lista
    if servidor_id not in usuarios_dm_enviados:
        usuarios_dm_enviados[servidor_id] = []

    if usuario_id not in usuarios_dm_enviados[servidor_id]:
        usuarios_dm_enviados[servidor_id].append(usuario_id)

    # Guarda los usuarios DM enviados actualizados en el archivo
    guardar_usuarios_dm_enviados(usuarios_dm_enviados)


def cargar_usuarios_dm_enviados():
    try:
        # Abre el archivo JSON de usuarios DM enviados
        with open('usuarios_dm_enviados.json', 'r') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return {}

    return datos


def guardar_usuarios_dm_enviados(usuarios_dm_enviados):
    # Guarda los datos actualizados en el archivo
    with open('usuarios_dm_enviados.json', 'w') as archivo:
        json.dump(usuarios_dm_enviados, archivo, indent=4)


# Evento de inicio del bot
@bot.event
async def on_ready():
    print('Esperando a que el bot esté listo...')
    print('El bot está listo')

    registros_canales = {}

    # Comprueba si se pueden enviar mensajes en todos los canales
    for canal_id in canales_ids_anuncio:
        canal = bot.get_channel(canal_id)

        if not canal.permissions_for(canal.guild.me).send_messages:
            registros_canales[canal_id] = f"{Fore.RED}No se pueden enviar mensajes"
        else:
            registros_canales[canal_id] = f"{Fore.GREEN}Se puede enviar mensajes"

    mostrar_registros(registros_canales)

    await enviar_anuncio_loop()
    await enviar_dm_loop()


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


@tasks.loop(seconds=random.randint(intervalo_anuncio_min, intervalo_anuncio_max))
async def enviar_anuncio_loop():
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
                    f'{Fore.CYAN}Mensaje enviado en el canal: {canal_anuncio.name}{Style.RESET_ALL}')
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


@tasks.loop(seconds=intervalo_dm)
async def enviar_dm_loop():
    if len(servidores_ids) == 0:
        print(f'{Fore.YELLOW}No hay servidores disponibles para enviar DMs en este momento.{Style.RESET_ALL}')
        return

    for servidor_id in servidores_ids:
        servidor = bot.get_guild(servidor_id)

        if not servidor:
            print(
                f'{Fore.RED}No se pudo encontrar el servidor con ID: {servidor_id} - Saltando...{Style.RESET_ALL}')
            continue

        registros_usuarios_dm = {}

        for miembro in servidor.members:
            if miembro.bot:
                continue

            # Verifica si ya se ha enviado un DM a este usuario
            usuarios_dm_enviados = cargar_usuarios_dm_enviados()

            if servidor_id in usuarios_dm_enviados and miembro.id in usuarios_dm_enviados[servidor_id]:
                registros_usuarios_dm[miembro.id] = f"{Fore.YELLOW}DM ya enviado"
                continue

            try:
                mensaje_dm = config['mensaje_dm']
                await miembro.send(mensaje_dm)
                registros_usuarios_dm[miembro.id] = f"{Fore.GREEN}DM enviado"
                # Registra el usuario DM enviado
                registrar_usuario_dm_enviado(servidor_id, miembro.id)
                print(
                    f'{Fore.CYAN}DM enviado a: {miembro.name}#{miembro.discriminator}{Style.RESET_ALL}')
            except discord.Forbidden:
                registros_usuarios_dm[miembro.id] = f"{Fore.RED}No se puede enviar DM"
                print(
                    f'{Fore.RED}No se puede enviar DM a: {miembro.name}#{miembro.discriminator}{Style.RESET_ALL}')
            except Exception as e:
                registros_usuarios_dm[miembro.id] = f"{Fore.RED}Error: {e}"
                print(
                    f'{Fore.RED}Error al enviar DM a: {miembro.name}#{miembro.discriminator} - {e}{Style.RESET_ALL}')

        print(
            f'{Fore.CYAN}Registros de DMs enviados en el servidor: {servidor.name}{Style.RESET_ALL}')
        mostrar_registros(registros_usuarios_dm)


@enviar_anuncio_loop.before_loop
async def before_enviar_anuncio_loop():
    await bot.wait_until_ready()


@enviar_dm_loop.before_loop
async def before_enviar_dm_loop():
    await bot.wait_until_ready()


# Comando para agregar un canal de anuncio
@bot.command()
async def agregar_canal(ctx, canal_id: int):
    if canal_id not in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)

        if canal_anuncio:
            canales_ids_anuncio.append(canal_id)

            with open('canales_ids_anuncio.json', 'w', encoding='utf-8') as canales_file:
                json.dump(canales_ids_anuncio, canales_file, indent=4)

            await ctx.send(f'Se ha agregado el canal de anuncio: {canal_anuncio.name}')
            await check_permissions()
        else:
            await ctx.send('No se encontró el canal en el servidor')
    else:
        await ctx.send('El canal ya está en la lista de canales de anuncio')


# Comando para eliminar un canal de anuncio
@bot.command()
async def eliminar_canal(ctx, canal_id: int):
    if canal_id in canales_ids_anuncio:
        canales_ids_anuncio.remove(canal_id)

        with open('canales_ids_anuncio.json', 'w', encoding='utf-8') as canales_file:
            json.dump(canales_ids_anuncio, canales_file, indent=4)

        await ctx.send(f'Se ha eliminado el canal de anuncio con ID: {canal_id}')
        await check_permissions()
    else:
        await ctx.send('El canal no está en la lista de canales de anuncio')


# Comando para agregar un servidor
@bot.command()
async def agregar_servidor(ctx, servidor_id: int):
    if servidor_id not in servidores_ids:
        servidor = bot.get_guild(servidor_id)

        if servidor:
            servidores_ids.append(servidor_id)

            with open('servidores_ids.json', 'w', encoding='utf-8') as servidores_file:
                json.dump(servidores_ids, servidores_file, indent=4)

            await ctx.send(f'Se ha agregado el servidor: {servidor.name}')
        else:
            await ctx.send('No se encontró el servidor')
    else:
        await ctx.send('El servidor ya está en la lista de servidores')


# Comando para eliminar un servidor
@bot.command()
async def eliminar_servidor(ctx, servidor_id: int):
    if servidor_id in servidores_ids:
        servidores_ids.remove(servidor_id)

        with open('servidores_ids.json', 'w', encoding='utf-8') as servidores_file:
            json.dump(servidores_ids, servidores_file, indent=4)

        await ctx.send(f'Se ha eliminado el servidor con ID: {servidor_id}')
    else:
        await ctx.send('El servidor no está en la lista de servidores')


bot.run(TOKEN, bot=False)
