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

words = [
    {"word": "apple", "translation": "яблоко", "transcription": "[ˈæpəl]"},
    {"word": "book", "translation": "книга", "transcription": "[bʊk]"},
    {"word": "cat", "translation": "кот", "transcription": "[kæt]"},
    {"word": "dog", "translation": "собака", "transcription": "[dɒɡ]"},
    {"word": "elephant", "translation": "слон", "transcription": "[ˈɛlɪfənt]"},
    {"word": "flower", "translation": "цветок", "transcription": "[ˈflaʊər]"},
    {"word": "guitar", "translation": "гитара", "transcription": "[ɡɪˈtɑːr]"},
    {"word": "house", "translation": "дом", "transcription": "[haʊs]"},
    {"word": "island", "translation": "остров", "transcription": "[ˈaɪlənd]"},
    {"word": "jungle", "translation": "джунгли", "transcription": "[ˈdʒʌŋɡəl]"}
]

# Список для хранения использованных слов
used_words = []

# Функция для получения 5 случайных слов
def get_random_words(word_list, num_words=5):
    available_words = [word for word in word_list if word not in used_words]
    if len(available_words) < num_words:
        return None
    selected_words = random.sample(available_words, num_words)
    used_words.extend(selected_words)
    return selected_words

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
    elif message.text == "Новые слова📗":
        # Показываем кнопки для начала теста
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_test_button = types.KeyboardButton("Получить 5 новых слов🙋")
        back_button = types.KeyboardButton("Вернуться назад🆘")
        markup.add(start_test_button, back_button)
        bot.send_message(message.chat.id, "Нажми на кнопку, чтобы получить 5 новых слов!", reply_markup=markup)
    elif message.text == "Получить 5 новых слов🙋":
        random_words = get_random_words(words)
        if random_words:
            response = "Вот 5 новых слов для изучения:\n\n"
            for word in random_words:
                response += f"Слово: {word['word']}\nПеревод: {word['translation']}\nТранскрипция: {word['transcription']}\n\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Слова закончились! Ждите обновления словаря!")
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок!")

# Запуск бота
bot.polling(none_stop=True, interval=0)