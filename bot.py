import asyncio
import logging
import telebot

from config import token, data_dict
from zkill_socket import killmail


logger = logging.getLogger(__name__)
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message: 'telebot.types.Message') -> None:
    bot.send_message(message.from_user.id, 'This is the bot for sending Killmails by Alliance 7_62.')


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a', filename='logs.log')
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
            asyncio.run(killmail(data=data_dict))
        except Exception as err:
            logger.error(f'{err}')
