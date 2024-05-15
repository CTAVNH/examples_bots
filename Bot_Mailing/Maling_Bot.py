from telegram import Bot
from telegram.error import TelegramError
import logging
import schedule
import time

# Устанавливаем уровень логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Список пользователей, которым нужно отправить сообщение
USERS = ['USER_ID_1', 'USER_ID_2']  # Замените на реальные ID пользователей

# Текст сообщения для рассылки
MESSAGE = 'Ваше сообщение здесь'

# Функция рассылки сообщения
def send_message(bot, user_id, message):
    try:
        bot.send_message(chat_id=user_id, text=message)
    except TelegramError as e:
        logger.error(f"Failed to send message to user {user_id}: {e.message}")

# Функция для отправки сообщения в определенное время
def send_message_at_time(bot, user_id, message, time):
    schedule.every().day.at(time).do(send_message, bot, user_id, message)

# Функция для отправки сообщения с определенным интервалом времени
def send_message_periodically(bot, user_id, message, interval):
    schedule.every(interval).minutes.do(send_message, bot, user_id, message)

def main():
    # Создаем объект бота
    bot = Bot(token=TOKEN)

    # Отправляем сообщение каждому пользователю из списка в определенное время
    for user_id in USERS:
        send_message_at_time(bot, user_id, MESSAGE, '10:00')

    # Отправляем сообщение каждому пользователю из списка с определенным интервалом времени
    for user_id in USERS:
        send_message_periodically(bot, user_id, MESSAGE, 60)  # каждые 60 минут

    # Запускаем планировщик
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()

