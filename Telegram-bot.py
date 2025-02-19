import telebot
from telebot import types
import random
from compliment import compliments
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка токена
if not TOKEN:
    raise ValueError("Токен не найден. Проверьте .env файл.")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

words = [{}]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀Старт")
    action_button = types.KeyboardButton("Комплимент⛰️")
    markup.add(start_button, action_button)
    bot.send_message(message.chat.id, f"Привет✌️, {message.from_user.first_name} \nВоспользуйся кнопками!", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=["text"])
def buttons(message):
    if message.text == "🚀Старт":
        bot.send_message(message.chat.id, text="Хорошо, выбери из списка интересующий тебя пункт! \n1.Определение уровня💯 \n2.Новые слова📗 \n3.Правила💬")
    elif message.text == "Комплимент⛰️":
        bot.send_message(message.chat.id, text=f"{random.choice(compliments)}")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок!")

    if message.text == "Новые слова📗":
        # Показываем кнопки для начала теста
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_test_button = types.KeyboardButton("Получить 5 новых слов🙋")
        back_button = types.KeyboardButton("Вернуться назад🆘")
        markup.add(start_test_button, back_button)
        bot.send_message(message.chat.id, "Вот 5 новых слов! Удачи!", reply_markup=markup)

# Запуск бота
bot.polling(none_stop=True, interval=0)