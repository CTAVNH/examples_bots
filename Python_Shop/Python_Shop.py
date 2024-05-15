import telebot
import requests
from telebot import types
from config import BOT_TOKEN
from config import API_KEY

# Токен вашего бота
TOKEN = BOT_TOKEN

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения списка товаров
def get_products():
    try:
        response = requests.get(API_KEY)
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении данных:", response.status_code)
            return None
    except Exception as e:
        print("Ошибка при получении данных:", e)
        return None

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(types.KeyboardButton('/low'), types.KeyboardButton('/high'))
    kb.add(types.KeyboardButton('/custom'), types.KeyboardButton('/help'))
    bot.send_message(message.chat.id, "Привет! Этот бот предоставляет информацию о товарах.\n"
                                      "Чтобы начать, используйте кнопки ниже или команду /help:\n"
                                      "/low - сортировать товары от меньшего к большему\n"
                                      "/high - сортировать товары от большего к меньшему\n"
                                      "/custom - выбрать диапазон цен\n"
                                      "/help - получить помощь", reply_markup=kb)

# Функция для получения списка товаров с исключением "New Product"
def get_products():
    try:
        response = requests.get("https://api.escuelajs.co/api/v1/products")
        if response.status_code == 200:
            products = response.json()
            return [product for product in products if product.get('title', '') != 'New Product']
        else:
            print("Ошибка при получении данных:", response.status_code)
            return None
    except Exception as e:
        print("Ошибка при получении данных:", e)
        return None

# Функция для отправки товаров пользователю с учетом заданного количества
def send_products(message, products, quantity):
    if len(products) == 0:
        bot.send_message(message.chat.id, "Нет товаров в заданном диапазоне цен.")
    else:
        count = min(len(products), quantity)
        sent_count = 0
        for product in products:
            if sent_count >= quantity:
                break
            bot.send_message(message.chat.id, f"Название: {product['title']}\nЦена: {product['price']}")
            if 'images' in product and len(product['images']) > 0:
                for image in product['images']:
                    try:
                        bot.send_photo(message.chat.id, image)
                    except Exception as e:
                        print(f"Ошибка отправки изображения: {e}")
            sent_count += 1

# Обработчик команды /low
@bot.message_handler(commands=['low'])
def sort_low(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(types.KeyboardButton('Clothes'), types.KeyboardButton('Electronics'))
    kb.add(types.KeyboardButton('Shoes'), types.KeyboardButton('Miscellaneous'))
    kb.add(types.KeyboardButton('Books'))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=kb)
    bot.register_next_step_handler(message, process_category_low)

def process_category_low(message):
    category = message.text
    bot.send_message(message.chat.id, "Введите количество товаров для отображения (от 1 до 10):")
    bot.register_next_step_handler(message, lambda m: process_quantity_low(m, category))

def process_quantity_low(message, category):
    try:
        quantity = int(message.text)
        if 1 <= quantity <= 10:
            products = get_products()
            if products:
                filtered_products = [p for p in products if p['category']['name'] == category]
                if filtered_products:
                    sorted_products = sorted(filtered_products, key=lambda x: x['price'])
                    send_products(message, sorted_products, quantity)
                else:
                    bot.send_message(message.chat.id, "Нет товаров в заданной категории и диапазоне цен.")
            else:
                bot.send_message(message.chat.id, "Ошибка при получении данных о товарах.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")

# Обработчик команды /high
@bot.message_handler(commands=['high'])
def sort_high(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(types.KeyboardButton('Clothes'), types.KeyboardButton('Electronics'))
    kb.add(types.KeyboardButton('Shoes'), types.KeyboardButton('Miscellaneous'))
    kb.add(types.KeyboardButton('Books'))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=kb)
    bot.register_next_step_handler(message, process_category_high)

def process_category_high(message):
    category = message.text
    bot.send_message(message.chat.id, "Введите количество товаров для отображения (от 1 до 10):")
    bot.register_next_step_handler(message, lambda m: process_quantity_high(m, category))

def process_quantity_high(message, category):
    try:
        quantity = int(message.text)
        if 1 <= quantity <= 10:
            products = get_products()
            if products:
                filtered_products = [p for p in products if p['category']['name'] == category]
                if filtered_products:
                    sorted_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
                    send_products(message, sorted_products, quantity)
                else:
                    bot.send_message(message.chat.id, "Нет товаров в заданной категории и диапазоне цен.")
            else:
                bot.send_message(message.chat.id, "Ошибка при получении данных о товарах.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")

# Обработчик команды /custom
@bot.message_handler(commands=['custom'])
def custom_price(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add(types.KeyboardButton('Clothes'), types.KeyboardButton('Electronics'))
    kb.add(types.KeyboardButton('Shoes'), types.KeyboardButton('Miscellaneous'))
    kb.add(types.KeyboardButton('Books'))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=kb)
    bot.register_next_step_handler(message, process_category_custom)

def process_category_custom(message):
    category = message.text
    bot.send_message(message.chat.id, "Введите минимальную цену:")
    bot.register_next_step_handler(message, lambda m: process_min_price_custom(m, category))

def process_min_price_custom(message, category):
    try:
        min_price = int(message.text)
        products = get_products()
        if products:
            filtered_products = [p for p in products if p['price'] >= min_price and p['category']['name'] == category]
            if filtered_products:
                send_products(message, filtered_products, len(filtered_products))
            else:
                bot.send_message(message.chat.id, "Нет товаров в заданной категории и диапазоне цен.")
        else:
            bot.send_message(message.chat.id, "Ошибка при получении данных о товарах.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную цену.")

# Обработчик любого входящего сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Привет! Я могу помочь вам с информацией о товарах. "
                                      "Используйте кнопки ниже или команду /help, чтобы узнать, что я могу.")

# Запускаем бота
bot.polling()
