import telebot
from telebot import types
from secrets import secrets
from compliment import compliments
import random
token = ("8195726179:AAHP1t-YFSkYjJgiZX_y6L8FkV4Np3nke_M")
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀Старт")
    action_button = types.KeyboardButton("Комплимент⛰️")
    markup.add(start_button, action_button)
    bot.send_message(message.chat.id, "Привет✌️ , {0.first_name} \nВоспользуйся кнопками!".format(message.from_user), reply_markup=markup)

bot.polling(none_stop=True, interval=0)



@bot.message_handler(content_types=["text"])
def buttons(message):
    if(message.text == "🚀Старт"):
        bot.send_message(message.chat.id, text="Хорошо , выбери из списка интересующий тебя пункт! \n1.Опредиление уровня \n2.Новые слова \n3.Правила")
    elif (message.text =="Комплимент⛰️" ):
        bot.send_message(message.chat.id, text=f"{random.choice(compliments)}")
    else:
        bot.send_message(message.chat.id , text = "Я могу отвечать только на нажатие кнопок!")