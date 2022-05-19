import telebot, requests, time
import json
import sqlite3 as sl
from telebot import types
token = '5367696164:AAHX8QGlpmlTMcvzgcx5QmYnv9KDs1X231I'
bot = telebot.TeleBot(token)
tconv = lambda x: time.strftime("%H:%M:%S", time.localtime(x))
tcoj = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))
conn = sl.connect('Stabis.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(ID_User: int, Date: str, Time:str, Location:str):
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
    item3=types.KeyboardButton('Тест')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите, что вам надо', reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Тест":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Тест 3')
        markup.add(item1)
        bot.send_message(message.chat.id, "Тест 1 пройден успешно", reply_markup=markup)
    if message.text.lower=='бд':
        bot.send_message(message.from_user.id, 'Привет! Ваши данные внесены в базу данных')
    elif message.text=="Тест 2":
        bot.send_message(message.chat.id, "Тест 2 пройден успешно")
    elif message.text=="Тест 3":
        bot.send_message(message.chat.id, "Тест 3 пройден успешно")
        menu1 = types.InlineKeyboardMarkup()
        menu1.add(types.InlineKeyboardButton(text="Первая кнопка", callback_data="first"))
        menu1.add(types.InlineKeyboardButton(text="Вторая кнопка", callback_data="second"))
        bot_msg = bot.send_message(message.chat.id, 'Нажмите первую Inline кнопку', reply_markup=menu1)
    elif message.text.isdigit():
        bot.send_message(message.chat.id, 'Вы ввели цифры')
    elif message.text.isalpha():
        bot.send_message(message.chat.id, 'Вы ввели буквы')
    elif message.text.isalpha and message.text.isdigit:
        bot.send_message(message.chat.id, 'Вы ввели буквы с цифрами')
    us_id = message.from_user.id
    us_date = tconv(message.date)
    us_time = tcoj(message.date)
    us_location = message.from_user.username

    db_table_val(ID_User=us_id, Date=us_date, Time=us_time, Location=us_location)
@bot.callback_query_handler(func=lambda call: True)
def keyboard2(call):
    menu2 = types.InlineKeyboardMarkup()
    menu2.add(types.InlineKeyboardButton(text="Третья кнопка", callback_data="third"))
    menu2.add(types.InlineKeyboardButton(text="Четвертая кнопка", callback_data="fourth"))
    if call.data == 'first':
        bot_msg = bot.send_message(call.message.chat.id, 'Нажмите третью Inline кнопку', reply_markup=menu2)
    elif call.data == 'third':
        bot_msg = bot.send_message(call.message.chat.id, 'Конец')
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        bot.send_message == (message.location)
        bot.send_message(message.chat.id, geocoder(message.location.latitude, message.location.longitude))


def geocoder(latitude, longitude):
    token2 = 'pk.0a7f690b1ee2f5bc671e79241d167b57'
    headers = {"Accept-Language": "ru"}
    try:
        address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={token2}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
        return f'Твое местоположение: {address.get("display_name")}'
    except Exception as e:
        return 'error'
bot.polling(none_stop=True)