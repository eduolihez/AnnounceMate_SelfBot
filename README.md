# 🌟 AnnounceMate SelfBot🌟

## Description

AnnounceMate SelfBot is a specialized bot for announcements that allows you to send promotional messages to multiple Discord channels automatically and efficiently. With AnnounceMate, you can customize your announcements, include attractive images, and set time intervals for their delivery.

## Requirements

- Python 3.5 or higher
- Discord.py library
- Colorama library

## Configuration

1. Clone this repository to your local machine or download the program files.

2. Open the `configuration.json` file and configure the following parameters:

   - `token`: Insert your Discord bot token here. You can obtain it by creating a bot application on the [Discord Developer Portal](https://discord.com/developers/applications).

   - `email`: Insert your email address associated with your Discord account here.

   - `attach_photos`: Set this option to `true` if you want to attach images to your announcements. If you don't want to attach images, set this option to `false`.

   - `images`: If you have enabled the option to attach images, enter the full path of the images you want to send. You can specify multiple images separated by commas.

3. Open the `announcement_messages.json` file and customize your announcement messages. You can add as many messages as you want, following the provided example structure.

4. Open the `announcement_channel_ids.json` file and configure the IDs of the channels where you want to send the announcements. You can add as many IDs as you want, following the provided example structure.

## Usage

1. Ensure that the bot has the necessary permissions to send messages in the channels specified in `announcement_channel_ids.json`.

2. Run the program by executing the following command in your terminal:

```python
python bot.py
```

The bot will connect to Discord and be ready to send announcements.

3. The bot will automatically send announcements according to the time interval set in `configuration.json`. You can modify this interval according to your preferences.

## Activity Log

The bot generates an activity log in the `log.txt` file. This file contains information about sent messages, the channels they were sent to, and the wave number. You can refer to this file to track the progress and statistics of your announcements.

## Notes

- Ensure that you keep your Discord credentials and tokens secure and do not share them with anyone.

- If you encounter any issues or errors when running the bot, make sure you have the `discord.py` and `colorama` libraries installed. You can install them using the following command:

```bash
pip install colorama
```

- Remember to adhere to Discord's policies and terms of use when sending announcements, and ensure you have the appropriate permissions to send messages in the selected channels.

Enjoy automatic announcements with AnnounceMate! If you have any questions or need assistance, feel free to contact the developer at s4var@proton.me.
