import telebot, requests, time, json, sqlite3 as sl
from telebot import types

token = '5367696164:AAHX8QGlpmlTMcvzgcx5QmYnv9KDs1X231I'
bot = telebot.TeleBot(token)
conn = sl.connect('Stabis.db', check_same_thread=False)
cursor = conn.cursor()
itr = cursor.execute("SELECT Location FROM Users").fetchall()
select_Info = []
for abInfo in itr:
    select_Info.append(abInfo[])
print(abInfo)
tconv = lambda x: time.strftime("%H:%M:%S", time.localtime(x))
tcoj = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))



def db_table_val(ID_User: int, Date: str, Time:str, Location:str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (ID_User, Date, Time, Location) VALUES (?,?,?,?)',(ID_User, Date, Time, Location))
    conn.commit()
    cursor.close()
    conn.close()
def db_table_update(Latitude: str, Longitude: str, Location: str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Latitude = ?, Longitude = ? WHERE Location = 'Bruh'", (Latitude, Longitude, Location))
def db_table_delete(Location:str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE Location = (?)", (Location, ))
    conn.commit()
    cursor.close()
    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = user_name + " Ваш ID: " + str(user_id)
    bot_msg = f"Привет, {mention}"
    bot.send_message(cid, bot_msg)

@bot.message_handler(commands=['menu'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Добавить название объекта')
    item2 = types.KeyboardButton('Отправить геолокацию')
    item3 = types.KeyboardButton('Реестр объектов')
    item4 = types.KeyboardButton('Удалить объект')
    markup.row(item1)
    markup.row(item2)
    markup.row(item3, item4)
    bot.send_message(message.chat.id, 'Выберите, что вам надо', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить название объекта")
def add_object(message):
    msg = bot.send_message(message.chat.id, "Введите название объекта")
    bot.register_next_step_handler(msg, add_object_2)

def add_object_2(message):
    bot.send_message(message.chat.id, 'Мы запомнили это')
    us_id = message.from_user.id
    us_date = tconv(message.date)
    us_time = tcoj(message.date)
    db_table_val(ID_User=us_id, Date= us_date, Time= us_time, Location=message.text)

@bot.message_handler(func=lambda message: message.text == "Отправить геолокацию")
def add_geolog(message):
    msg = bot.send_message(message.chat.id, "Выберите объект", reply_markup=makeKeyboard())
    bot.register_next_step_handler(msg, add_geolog2)

def add_geolog2(message):
    bot.send_message(message.chat.id, "Геолокация добавлена")
    db_table_update(Latitude=us_latitude, Longitude=us_longitude, Location=us_location)

@bot.message_handler(func=lambda message: message.text == "Удалить объект")
def del_object(message):
    msg = bot.send_message(message.chat.id, "Введите название объекта")
    bot.register_next_step_handler(msg, del_object2)

def del_object2(message):
    bot.send_message(message.chat.id, "Удаление прошло успешно")
    db_table_delete(Location=message.text)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        bot.send_message == (message.location)
        coords = geocoder(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, coords)
        us_latitude = message.location.latitude
        us_longitude = message.location.longitude
        db_table_update(Latitude=us_latitude, Longitude=us_longitude)


def geocoder(latitude, longitude):
    token2 = 'pk.0a7f690b1ee2f5bc671e79241d167b57'
    headers = {"Accept-Language": "ru"}
    try:
        address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={token2}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
        return f'{address["address"].get("city")}, {address["address"].get("road")}, {address["address"].get("house_number")} '
    except Exception as e:
        return 'error'

'''def makeKeyboard():
    markup5 = types.InlineKeyboardMarkup()
    for row in obInfo:
        markup5.add(types.InlineKeyboardButton(text=result, callback_data=select_Info"['result', '" + str(result) + "']"))
    return markup5'''

bot.polling(none_stop=True)