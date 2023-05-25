import discord
from discord.ext import commands, tasks
import random
import asyncio

# Configura tu token de bot de Discord
TOKEN = 'MTA4NzA3MDk5NDU2MjI5ODAwNg.GAV8SV.ydnomqsVQa-pICYTaJEHsQq15dlth3zKF28dzs'

# Configura el ID del servidor donde se seleccionarán los usuarios aleatorios
servidor_id = 1111023786276442202  # ID del servidor

# Configura el intervalo de tiempo entre cada mensaje directo (en segundos)
intervalo_dm = 5400  # 1.5 horas = 5400 segundos

# Configura las rutas de las imágenes que deseas adjuntar en los mensajes directos
rutas_imagenes = ['150.jpg', '350.jpg',
                  '900.jpg']  # Rutas de las imágenes

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('El bot está listo')
    enviar_dm.start()


@tasks.loop(seconds=intervalo_dm)
async def enviar_dm():
    servidor = bot.get_guild(servidor_id)
    if servidor is None:
        print(f"No se encontró el servidor con ID {servidor_id}")
        return

    usuarios = servidor.members
    usuarios_disponibles = []

    for usuario in usuarios:
        if not usuario.bot and usuario.status != discord.Status.offline and not usuario.dm_channel:
            usuarios_disponibles.append(usuario)

    usuarios_seleccionados = random.sample(usuarios_disponibles, 3)
    mensaje = '''
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
        '''
    imagenes_adjuntas = []

    for ruta_imagen in rutas_imagenes:
        with open(ruta_imagen, 'rb') as imagen:
            imagenes_adjuntas.append(discord.File(imagen))

    for usuario in usuarios_seleccionados:
        try:
            dm_channel = usuario.dm_channel
            if dm_channel is None:
                dm_channel = await usuario.create_dm()

            await dm_channel.send(content=mensaje, files=imagenes_adjuntas)
            print(f"Mensaje enviado a {usuario.name}")
        except discord.Forbidden:
            print(
                f"No se puede enviar un mensaje a {usuario.name}. El DM está cerrado.")


@enviar_dm.before_loop
async def before_enviar_dm():
    await bot.wait_until_ready()

bot.run(TOKEN, bot=False)
