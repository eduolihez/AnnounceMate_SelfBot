import discord
from discord.ext import commands, tasks
import asyncio
import random

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Configura la lista de IDs de servidores donde se seleccionarán los usuarios aleatorios
servidores_ids = [1111023786276442202]  # IDs de los servidores

# Configura la lista de IDs de canales de anuncios
# IDs de los canales para los anuncios
canales_ids_anuncio = [1111039972443693136]

# Configura el intervalo de tiempo entre cada anuncio (en segundos)
intervalo_anuncio = 1800  # 1 hora = 3600 segundos

# Configura las rutas de las imágenes que deseas adjuntar en los anuncios
rutas_imagenes = ['150.jpg', '350.jpg',
                  '900.jpg']  # Rutas de las imágenes

# Configura el intervalo de tiempo entre cada mensaje directo (en segundos)
intervalo_dm = 5400  # 1.5 horas = 5400 segundos

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('El bot está listo')
    enviar_anuncio.start()


@bot.command()
async def ayuda(ctx):
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
    for canal_id in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)
        imagenes_adjuntas = []

        for ruta_imagen in rutas_imagenes:
            with open(ruta_imagen, 'rb') as imagen:
                imagenes_adjuntas.append(discord.File(imagen))

        await canal_anuncio.send('''
**𝐏𝐚𝐲𝐏𝐚𝐥 𝐀𝐜𝐜𝐨𝐮𝐧𝐭𝐬**
```yaml
🔒 150€ Balance ➢ 10€
```
```yaml
🔒 350€ Balance ➢ 20€
```
```yaml
🔒 900€ Balance ➢ 50€
```
:shopping_cart: **Payment Method:** Cryptocurrencies (*ETH, BTC, SOL, etc...*) only.

> **__Purchase here:__ <@1087070994562298006>  (DM)**
> **FAQ: If you have questions drop a message.**
> **Vouches: You can ask for reviews at my DM, also have proofs & can __screenshare__.**
        ''', files=imagenes_adjuntas)

@bot.command()
async def start(ctx):
    enviar_anuncio.start()
    await ctx.send('El envío de anuncios y mensajes directos ha comenzado')

@bot.command()
async def stop(ctx):
    enviar_anuncio.cancel()
    await ctx.send('El envío de anuncios y mensajes directos ha sido detenido')

bot.run(TOKEN, bot=False)
