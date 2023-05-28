# 🌟 DiscordAdvertiseBot 🌟

## Descripción

DiscordAdvertiseBot es un bot especializado en anuncios que te permite enviar mensajes promocionales a múltiples canales en Discord de manera automática y eficiente. Con DiscordAdvertiseBot, podrás personalizar tus anuncios, incluir imágenes atractivas y establecer intervalos de tiempo para su envío.

## Requisitos

- Python 3.5 o superior
- Biblioteca Discord.py
- Biblioteca Colorama

## Configuración

1. Clona este repositorio en tu máquina local o descarga los archivos del programa.

2. Abre el archivo `configuracion.json` y configura los siguientes parámetros:

   - `token`: Inserta aquí el token de tu bot de Discord. Puedes obtenerlo creando una aplicación de bot en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).

   - `correo`: Inserta aquí tu dirección de correo electrónico asociada a tu cuenta de Discord.

   - `adjuntar_fotos`: Establece esta opción a `true` si deseas adjuntar imágenes a tus anuncios. Si no deseas adjuntar imágenes, establece esta opción a `false`.

   - `imagenes`: Si has habilitado la opción de adjuntar imágenes, ingresa la ruta completa de las imágenes que deseas enviar. Puedes especificar varias imágenes separadas por comas.

3. Abre el archivo `mensajes_anuncio.json` y personaliza tus mensajes de anuncio. Puedes agregar tantos mensajes como desees, siguiendo la estructura de ejemplo proporcionada.

4. Abre el archivo `canales_ids_anuncio.json` y configura los IDs de los canales en los que deseas enviar los anuncios. Puedes agregar tantos IDs como desees, siguiendo la estructura de ejemplo proporcionada.

## Uso

1. Asegúrate de que el bot tenga los permisos necesarios para enviar mensajes en los canales especificados en `canales_ids_anuncio.json`.

2. Ejecuta el programa ejecutando el siguiente comando en tu terminal:

```python
python bot.py
```

El bot se conectará a Discord y estará listo para enviar anuncios.

3. El bot enviará los anuncios automáticamente según el intervalo de tiempo establecido en `configuracion.json`. Puedes modificar este intervalo según tus preferencias.

## Registro de Actividad

El bot genera un registro de actividad en el archivo `registro.txt`. Este archivo contiene información sobre los mensajes enviados, los canales a los que se enviaron y el número de oleada. Puedes consultar este archivo para rastrear el progreso y las estadísticas de tus anuncios.

## Notas

- Asegúrate de mantener tus credenciales y tokens de Discord en un lugar seguro y no compartirlos con nadie.

- Si experimentas algún problema o error al ejecutar el bot, asegúrate de tener instaladas las bibliotecas `discord.py` y `colorama`. Puedes instalarlas usando el siguiente comando:

```bash
pip install colorama
```

- Recuerda respetar las políticas y términos de uso de Discord al enviar anuncios y asegurarte de tener los permisos adecuados para enviar mensajes en los canales seleccionados.

¡Disfruta de tus anuncios automáticos con DiscordAdvertiseBot! Si tienes alguna pregunta o necesitas ayuda, no dudes en contactar al desarrollador en s4var@proton.me.
