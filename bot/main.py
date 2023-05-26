import discord
from discord.ext import commands, tasks
import asyncio
import random

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Configura la lista de IDs de canales de anuncios
# IDs de los canales para los anuncios
canales_ids_anuncio = [1088487226628919326, 1088487283717586994,
                       1090227243017572373, 1090227291981889606, 1090227324756168756,
                       1107023909599051796, 1107023998426038423, 1107023980071763968, 1107024015652036680]

# Configura el intervalo de tiempo entre cada anuncio (en segundos)
intervalo_anuncio = 3600  # 1 hora = 3600 segundos

# Configura las rutas de las imágenes que deseas adjuntar en los anuncios
rutas_imagenes = ['150.jpg', '350.jpg', '750.jpg']  # Rutas de las imágenes

bot = commands.Bot(command_prefix='$')


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
    for canal_id in canales_ids_anuncio:
        canal_anuncio = bot.get_channel(canal_id)
        imagenes_adjuntas = []

        for ruta_imagen in rutas_imagenes:
            with open(ruta_imagen, 'rb') as imagen:
                imagenes_adjuntas.append(discord.File(imagen))
        await canal_anuncio.send('''
**:lock: Premium Account Access! Get Instant Balances! :lock:**

:moneybag: **Balance Options:**
- **150€ Balance** :arrow_right: **Only 10€!**
- **350€ Balance** :arrow_right: **Just 20€!**
- **500€ Balance** :arrow_right: **Special Offer at 30€!**
- **750€ Balance** :arrow_right: **Limited Time Deal at 40€!**
- **900€ Balance** :arrow_right: **Amazing Deal at 50€!**
- **1200€ Balance** :arrow_right: **Exclusive Offer at 60€!**

:shopping_cart: **Payment Method:** Cryptocurrencies (*ETH, BTC, SOL, and more*) accepted!

:white_check_mark: **Secure and Reliable Service:**
```
- Purchase directly from a trusted seller.
- Guaranteed instant delivery of account balances.
- Verified vouches and reviews available upon request.
- Proofs and screen sharing for your peace of mind.
```
:warning: **Note: The seller NEVER goes first in the transaction.**

:inbox_tray: **How to Purchase:**
```yaml
1️⃣ Contact us via DM for payment details.
2️⃣ Receive a secure payment address for your chosen cryptocurrency.
3️⃣ Make the payment and provide confirmation.
4️⃣ Enjoy instant access to your premium account balances!
```
:question: **Have questions? We're here to help!**
```yaml
- Reach out to us for any inquiries or concerns.
- FAQ available for quick reference.
```
:fire: Don't miss out on this exclusive opportunity! Get premium account balances at unbeatable prices today! :fire:''', files=imagenes_adjuntas)

@bot.command()
async def start(ctx):
    enviar_anuncio.start()
    await ctx.send('El envío de anuncios y mensajes directos ha comenzado')

@bot.command()
async def stop(ctx):
    enviar_anuncio.cancel()
    await ctx.send('El envío de anuncios y mensajes directos ha sido detenido')

bot.run(TOKEN, bot=False)
