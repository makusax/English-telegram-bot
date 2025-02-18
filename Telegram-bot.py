import telebot
from telebot import types
import random
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Получение токена
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден. Проверьте .env файл.")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Список вопросов для теста
questions = [
    {"sentence": "She ___ to school every day.", "answer": "goes"},
    {"sentence": "They ___ football right now.", "answer": "are playing"},
    {"sentence": "He ___ his homework yesterday.", "answer": "did"},
    {"sentence": "I ___ call you tomorrow.", "answer": "will"},
    {"sentence": "We ___ already finished the project.", "answer": "have"}
]

# Словарь для хранения состояния пользователей
user_data = {}

# Функция для определения уровня
def determine_level(correct_answers, total_questions):
    percentage = (correct_answers / total_questions) * 100

    if percentage >= 80:  # 4/5 или 5/5
        return "B1-B2"
    elif percentage >= 60:  # 3/5
        return "A2"
    elif percentage >= 40:  # 2/5
        return "A1"
    else:  # 1/5 или 0/5
        return "A0"

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
        # Показываем меню с выбором пунктов
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        level_button = types.KeyboardButton("Определение уровня💯")
        words_button = types.KeyboardButton("Новые слова📗")
        rules_button = types.KeyboardButton("Правила💬")
        markup.add(level_button, words_button, rules_button)
        bot.send_message(message.chat.id, "Хорошо, выбери из списка интересующий тебя пункт!", reply_markup=markup)

    elif message.text == "Комплимент⛰️":
        # Отправляем случайный комплимент
        compliments = [
            "Ты выглядишь потрясающе!",
            "Ты умнее, чем ты думаешь!",
            "Ты делаешь этот мир лучше!",
            "Ты настоящий герой!",
            "Ты вдохновляешь!"
        ]
        bot.send_message(message.chat.id, text=f"{random.choice(compliments)}")

    elif message.text == "Определение уровня💯":
        # Показываем кнопки для начала теста
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_test_button = types.KeyboardButton("Начать Тест🙋")
        back_button = types.KeyboardButton("Вернуться назад🆘")
        markup.add(start_test_button, back_button)
        bot.send_message(message.chat.id, "Начнем тест! Будь внимателен!", reply_markup=markup)

    elif message.text == "Начать Тест🙋":
        # Инициализация состояния пользователя
        user_data[message.chat.id] = {
            "current_question": 0,
            "correct_answers": 0,
            "questions": questions
        }
        # Отправка первого вопроса
        question = user_data[message.chat.id]["questions"][0]
        bot.send_message(message.chat.id, question["sentence"])

    elif message.text == "Вернуться назад🆘":
        # Возвращаемся к главному меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("🚀Старт")
        action_button = types.KeyboardButton("Комплимент⛰️")
        markup.add(start_button, action_button)
        bot.send_message(message.chat.id, "Возвращаемся в главное меню!", reply_markup=markup)

    elif message.chat.id in user_data:  # Пользователь в режиме теста
        # Получение текущего вопроса
        current_question = user_data[message.chat.id]["current_question"]
        question = user_data[message.chat.id]["questions"][current_question]

        # Проверка ответа
        if message.text.lower() == question["answer"].lower():
            user_data[message.chat.id]["correct_answers"] += 1
            bot.send_message(message.chat.id, "Правильно! 🎉")
        else:
            bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {question['answer']}")

        # Переход к следующему вопросу
        user_data[message.chat.id]["current_question"] += 1
        if user_data[message.chat.id]["current_question"] < len(user_data[message.chat.id]["questions"]):
            next_question = user_data[message.chat.id]["questions"][user_data[message.chat.id]["current_question"]]
            bot.send_message(message.chat.id, next_question["sentence"])
        else:
            # Завершение теста
            correct_answers = user_data[message.chat.id]["correct_answers"]
            total_questions = len(user_data[message.chat.id]["questions"])

            # Определение уровня
            level = determine_level(correct_answers, total_questions)

            # Отправка результата
            bot.send_message(message.chat.id, f"Тест завершен! Правильных ответов: {correct_answers}/{total_questions}")
            bot.send_message(message.chat.id, f"Ваш уровень английского: {level}")

            # Удаление состояния
            del user_data[message.chat.id]

    else:
        # Обработка неизвестных команд
        bot.send_message(message.chat.id, "Я могу отвечать только на нажатие кнопок!")

# Запуск бота
bot.polling(none_stop=True, interval=0)