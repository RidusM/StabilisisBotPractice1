import telebot
from telebot import types
token='5367696164:AAHX8QGlpmlTMcvzgcx5QmYnv9KDs1X231I'
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = user_name+" Ваш ID: "+str(user_id)
    bot_msg = f"Привет, {mention}"
    bot.send_message(cid, bot_msg)
@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
bot.infinity_polling()
