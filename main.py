import telebot
import sqlite3 as sl
from telebot import types
token='5367696164:AAHX8QGlpmlTMcvzgcx5QmYnv9KDs1X231I'
bot=telebot.TeleBot(token)
conn = sl.connect('test.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(ID_User: int, Date: str, Time:str, Location:str)
    cursor.execute('INSERT INTO Users (ID_User, Date, Time, Location) VALUES (?,?,?,?)',(ID_User, Date, Time, Location))
    conn.commit()
@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = user_name + " Ваш ID: " + str(user_id)
    bot_msg = f"Привет, {mention}"
    bot.send_message(cid, bot_msg)
@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Данные о геопозиции', request_location=True)
    item2=types.KeyboardButton('Данные о телефоне', request_contact=True)
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите, что вам надо', reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Тест":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Тест 3')
        markup.add(item1)
        bot.send_message(message.chat.id, "Тест 1 пройден успешно", reply_markup=markup)
    elif message.text=="Тест2":
        bot.send_message(message.chat.id, "Тест 2 пройден успешно")
    elif message.text=="Тест3":
        bot.send_message(message.chat.id, "Тест 3 пройден успешно")
    elif message.text.isdigit():
        bot.send_message(message.chat.id, 'Вы ввели цифры')
    elif message.text.isalpha():
        bot.send_message(message.chat.id, 'Вы ввели буквы')
    elif message.text.isalpha and message.text.isdigit:
        bot.send_message(message.chat.id, 'Вы ввели буквы с цифрами')
    else:
        bot.send_message('Вы использовали незнакомый боту символ')
    menu1=types.InlineKeyboardMarkup()
    menu1.add(types.InlineKeyboardButton(text = "Первая кнопка", callback_data="first"))
    menu1.add(types.InlineKeyboardButton(text = "Вторая кнопка", callback_data="second"))
    if message.text == "Тест 3 пройден успешно":
        bot_msg = bot.send_message(message.chat.id, 'Нажмите первую Inline кнопку', reply_markup=menu1)
@bot.callback_query_handler(func=lambda call: True)
def keyboard2(call):
    menu2 = types.InlineKeyboardMarkup()
    menu2.add(types.InlineKeyboardButton(text="Третья кнопка", callback_data="third"))
    menu2.add(types.InlineKeyboardButton(text="Четвертая кнопка", callback_data="fourth"))
    if call.data == 'first':
        bot_msg = bot.send_message(call.message.chat.id, 'Нажмите третью Inline кнопку', reply_markup=menu2)
    elif call.data == 'third':
        bot_msg = bot.send_message(call.message.chat.id, 'Конец')
bot.polling(none_stop=True)
