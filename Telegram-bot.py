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

# Список новых слов
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

# Список правил
rules = [
    "1. Present Simple — это время, используемое для описания регулярных действий, фактов и состояний.",
    "2. Past Simple — это время, используемое для описания действий, которые произошли в прошлом.",
    "3. Future Simple — это время, используемое для описания действий, которые произойдут в будущем."
]

# Список описаний правил
description_rules = [
    "1. Формы образования Present Simple\nУтвердительная форма:\nДля I/You/We/They: используем основную форму глагола.\nДля He/She/It: добавляем окончание -s или -es.\nОтрицательная форма:\nИспользуем вспомогательный глагол do (для I/You/We/They) или does (для He/She/It) + not + основная форма глагола.\nВопросительная форма:\nВспомогательный глагол do или does ставим перед подлежащим.",
    "2. Формы образования Past Simple\nУтвердительная форма:\nДля всех подлежащих (I/You/He/She/It/We/They) используется вторая форма глагола (обычно это неправильные глаголы или добавление -ed к правильным).\nОтрицательная форма:\nИспользуем вспомогательный глагол did not (или сокращенно didn't) + основная форма глагола.\nВопросительная форма:\nВспомогательный глагол did ставим перед подлежащим, а основная форма глагола остается без изменений.",
    "3. Формы образования Future Simple\nУтвердительная форма:\nДля всех подлежащих (I/You/He/She/It/We/They) используется конструкция will + основная форма глагола.\nОтрицательная форма:\nИспользуем конструкцию will not (или сокращенно won't) + основная форма глагола.\nВопросительная форма:\nСтавим will перед подлежащим, а основная форма глагола остается без изменений."
]

# Словарь для хранения состояния пользователей
user_data = {}

# Функция для определения уровня
def determine_level(correct_answers, total_questions):
    percentage = (correct_answers / total_questions) * 100

    if percentage >= 80:
        return "B1-B2-С1"
    elif percentage >= 60:
        return "A2"
    elif percentage >= 40:
        return "A1"
    else:
        return "A0"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀Старт")
    action_button = types.KeyboardButton("Комплимент⛰️")
    markup.add(start_button, action_button)
    bot.send_message(message.chat.id, f"Привет✌️, {message.from_user.first_name} \nВоспользуйся кнопками!",
                     reply_markup=markup)

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

    elif message.text == "Правила💬":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        gives_rules_button = types.KeyboardButton("Получить правила🙋")
        back_button = types.KeyboardButton("Вернуться назад🆘")
        markup.add(gives_rules_button, back_button)
        bot.send_message(message.chat.id, "Давай же начнем изучения правил английского языка!", reply_markup=markup)

    elif message.text == "Получить правила🙋":
        user_data[message.chat.id] = {"mode": "choosing_rule"}  # Устанавливаем режим выбора правила
        rules_list = "Выберите правило, которое хотите изучить, введя его номер:\n"
        for i, rule in enumerate(rules, start=1):
            rules_list += f"{i}. {rule}\n"
        bot.send_message(message.chat.id, rules_list)

    elif message.text.strip().isdigit() and message.chat.id in user_data and user_data[message.chat.id].get("mode") == "choosing_rule":
        rule_number = int(message.text)
        if 1 <= rule_number <= len(rules):
            # Отправляем правило
            bot.send_message(message.chat.id, rules[rule_number - 1])
            # Отправляем описание
            bot.send_message(message.chat.id, description_rules[rule_number - 1])
            del user_data[message.chat.id]  # Сбрасываем режим
        else:
            bot.send_message(message.chat.id, "Правило с таким номером не найдено. Попробуйте ещё раз.")

    elif message.text == "Определение уровня💯":
        # Запрашиваем количество правильных ответов
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_test_button = types.KeyboardButton("Начать Тест🙋")
        back_button = types.KeyboardButton("Вернуться назад🆘")
        markup.add(start_test_button, back_button)
        bot.send_message(message.chat.id, "Начнем тест! Будь внимателен!", reply_markup=markup)

    elif message.text == "Начать Тест🙋":
        # Инициализация состояния пользователя для теста
        user_data[message.chat.id] = {
            "current_question": 0,
            "correct_answers": 0,
            "questions": [
                {"sentence": "She ___ to school every day.", "answer": "goes"},
                {"sentence": "They ___ football right now.", "answer": "are playing"},
                {"sentence": "He ___ his homework yesterday.", "answer": "did"},
                {"sentence": "I ___ call you tomorrow.", "answer": "will"},
                {"sentence": "We ___ already finished the project.", "answer": "have"},
                {"sentence": "She is ___ best student in the class.", "answer": "the"},
                {"sentence": "The book is ___ the table.", "answer": "on"},
                {"sentence": "This is the ___ movie I have ever seen.", "answer": "best"},
                {"sentence": "You ___ wear a helmet while riding a bike.", "answer": "must"},
                {"sentence": "There are three ___ in the room.", "answer": "chairs"}
            ]
        }
        # Отправка первого вопроса
        question = user_data[message.chat.id]["questions"][0]
        bot.send_message(message.chat.id, question["sentence"])

    elif message.text == "Новые слова📗":
        # Инициализация состояния пользователя для новых слов
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {
                "learned_words": []  # Инициализируем пустой список изученных слов
            }

        # Получаем слова, которые еще не изучены
        learned_words = user_data[message.chat.id].get("learned_words", [])  # Используем .get() для безопасности
        available_words = [word for word in words if word not in learned_words]

        if len(available_words) == 0:
            bot.send_message(message.chat.id, "Вы изучили все слова. Ждите обновления словаря!")
            return

        # Получаем 5 случайных слов
        new_words = random.sample(available_words, min(5, len(available_words)))
        user_data[message.chat.id]["learned_words"].extend(new_words)  # Добавляем новые слова в изученные

        # Отправляем новые слова
        response = "Вот ваши новые слова:\n"
        for word in new_words:
            response += f"Слово: {word['word']}, Перевод: {word['translation']}, Транскрипция: {word['transcription']}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == "Вернуться назад🆘":
        # Возвращаемся к главному меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("🚀Старт")
        action_button = types.KeyboardButton("Комплимент⛰️")
        markup.add(start_button, action_button)
        bot.send_message(message.chat.id, "Возвращаемся в главное меню!", reply_markup=markup)

    else:
        # Обработка ответов на вопросы теста
        if message.chat.id in user_data and "questions" in user_data[message.chat.id]:
            current_question = user_data[message.chat.id]["current_question"]
            questions = user_data[message.chat.id]["questions"]
            correct_answer = questions[current_question]["answer"]

            if message.text.strip().lower() == correct_answer.lower():
                user_data[message.chat.id]["correct_answers"] += 1
                bot.send_message(message.chat.id, "Правильно! 👍")
            else:
                bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {correct_answer}")

            # Переход к следующему вопросу
            user_data[message.chat.id]["current_question"] += 1

            if user_data[message.chat.id]["current_question"] < len(questions):
                next_question = questions[user_data[message.chat.id]["current_question"]]
                bot.send_message(message.chat.id, next_question["sentence"])
            else:
                # Завершение теста и определение уровня
                correct_answers = user_data[message.chat.id]["correct_answers"]
                total_questions = len(questions)
                level = determine_level(correct_answers, total_questions)
                bot.send_message(message.chat.id, f"Тест завершен! Ваш уровень: {level}")

                # Возвращаемся к главному меню
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                start_button = types.KeyboardButton("🚀Старт")
                action_button = types.KeyboardButton("Комплимент⛰️")
                markup.add(start_button, action_button)
                bot.send_message(message.chat.id, "Возвращаемся в главное меню!", reply_markup=markup)

                # Очищаем состояние пользователя
                del user_data[message.chat.id]
        else:
            # Обработка неизвестных команд
            bot.send_message(message.chat.id, "Я могу отвечать только на нажатие кнопок!")

# Запуск бота
bot.polling(none_stop=True, interval=0)