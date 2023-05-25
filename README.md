# Nombre del Proyecto

## Descripción

Este proyecto es un bot de Discord que se utiliza para enviar anuncios periódicos a varios canales y mensajes directos a usuarios seleccionados de diferentes servidores.

El bot está diseñado para cumplir con las necesidades de enviar anuncios con imágenes adjuntas y mensajes directos a usuarios de forma automatizada.

## Características

- Envío periódico de anuncios a múltiples canales de Discord.
- Adjuntar imágenes a los anuncios.
- Envío de mensajes directos a usuarios seleccionados de diferentes servidores.
- Reintento automático si los mensajes directos están cerrados.

## Requisitos Previos

- Python 3.7 o superior
- discord.py

## Configuración

1. Clona el repositorio o descarga los archivos del proyecto.

2. Obtén un token de bot de Discord siguiendo la [documentación oficial](https://discordpy.readthedocs.io/en/stable/discord.html).

3. Abre el archivo `bot.py` y reemplaza `'tu_token_de_discord'` con tu propio token de bot de Discord.

4. Configura las opciones del bot según tus necesidades:

   - `servidores_ids`: Lista de IDs de los servidores donde se seleccionarán los usuarios aleatorios.
   - `canales_ids_anuncio`: Lista de IDs de los canales de anuncios.
   - `intervalo_anuncio`: Intervalo de tiempo entre cada anuncio (en segundos).
   - `rutas_imagenes`: Rutas de las imágenes que se adjuntarán en los anuncios.
   - `intervalo_dm`: Intervalo de tiempo entre cada mensaje directo (en segundos).

5. Ejecuta el bot utilizando el siguiente comando:
   ```bash
   python main.py
   ```

## Uso

1. Invita al bot a tus servidores de Discord utilizando el enlace de invitación generado a través del [portal de desarrolladores de Discord](https://discord.com/developers/applications).

2. Configura los permisos necesarios para el bot en los servidores y canales donde deseas que funcione.

3. Ejecuta el comando `!start` en Discord para iniciar el envío de anuncios y mensajes directos.

4. Opcionalmente, puedes ejecutar el comando `!stop` para detener el envío de anuncios y mensajes directos.

## Contribución

Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.

2. Crea una rama con una descripción clara de la característica o corrección que deseas implementar.

3. Realiza los cambios necesarios en tu rama.

4. Realiza un pull request explicando tus cambios y las razones detrás de ellos.

## Agradecimientos

Agradecemos a todos los contribuyentes que han hecho posible este proyecto.

## Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).
