import os
import telebot
from dotenv import load_dotenv
from zkill_socket import logger

load_dotenv('.env')
token = os.getenv("my_token")
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message: 'telebot.types.Message') -> None:
    bot.send_message(message.from_user.id, 'This is the bot for sending Killmails by Alliance 7_62.')


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as err:
            logger.error(f'Bot: {err}')
