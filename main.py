import telebot, requests, time, json, ast, sqlite3 as sl
from telebot import types
'''from flask import Flask, render_template, app'''

'''app = Flask(__name__)'''

token = None
with open("token.txt") as f:
    token = f.read().strip()
bot = telebot.TeleBot(token)

tconv = lambda x: time.strftime("%H:%M:%S", time.localtime(x))
tcoj = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))

conn = sl.connect('Stabis.db', check_same_thread=False)
cursor = conn.cursor()

'''@app.route('/')
def db_table_selectAll():
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchall()
    return render_template('index.html', output_data = data)'''

'''if __name__ == '__main__':
    app.run(debug=True)'''

def db_table_selectAll():
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchall()
    my_list = []
    for x in data:
        my_list.append(''.join(str(x)))
    my_str = ''.join(str(my_list))
    return my_str

def db_table_select():
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT ProjName FROM Users")
    obInfo = [item[0] for item in cursor.fetchall()]
    return obInfo

def db_table_val(ID_User: int, Date: str, Time:str, ProjName:str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (ID_User, Date, Time, ProjName) VALUES (?,?,?,?)',(ID_User, Date, Time, ProjName))
    conn.commit()
    cursor.close()
    conn.close()
def db_table_update(Latitude: str, Longitude: str, Location:str, ProjName:str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Latitude = ?, Longitude = ?, Location = ? WHERE ProjName = ?", (Latitude, Longitude, Location, ProjName))
    conn.commit()
    cursor.close()
    conn.close()
def db_table_delete(ProjName:str):
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE ProjName = ?", (ProjName, ))
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
    bot.send_message(message.chat.id, 'Выберите, что вам надо', reply_markup=markup, )

@bot.message_handler(func=lambda message: message.text == "Добавить название объекта")
def add_object(message):
    msg = bot.send_message(message.chat.id, "Введите название объекта")
    bot.register_next_step_handler(msg, add_object_2)

def add_object_2(message):
    bot.send_message(message.chat.id, 'Мы запомнили это')
    us_id = message.from_user.id
    us_date = tconv(message.date)
    us_time = tcoj(message.date)
    db_table_val(ID_User=us_id, Date= us_date, Time= us_time, ProjName=message.text)

@bot.message_handler(func=lambda message: message.text == "Отправить геолокацию")
def add_geolog(message):
    msg = bot.send_message(message.chat.id, "Выберите объект", reply_markup=makeKeyboard())
    bot.register_next_step_handler(msg, add_geolog2)

def add_geolog2(message):
    us_projname =
    print(us_projname)
    if message.location is not None:
        bot.send_message == (message.location)
        coords = geocoder(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, coords)
        us_longitude = message.location.longitude
        us_latitude = message.location.latitude
        us_location = coords
        print (us_projname)
        db_table_update(Latitude=us_latitude, Longitude=us_longitude, Location=us_location, ProjName=us_projname)

@bot.message_handler(func=lambda message: message.text == "Удалить объект")
def del_object(message):
    msg = bot.send_message(message.chat.id, "Выберите объект", reply_markup=delKeyboard())

@bot.callback_query_handler(func=lambda msg:True)
def del_object2(callback_query):
    if callback_query.data.startswith("['del'"):
        print(ast.literal_eval(callback_query.data)[1])
        db_table_delete(ProjName=(ast.literal_eval(callback_query.data)[1]))
        bot.send_message(callback_query.message.chat.id, 'Удалено')


@bot.message_handler(func=lambda message: message.text == "Реестр объектов")
def reg_object(message):
    bot.send_message(message.from_user.id, db_table_selectAll())


@bot.message_handler(content_types=["location"], func=lambda msg:True)
def location(message):
    if message.location is not None:
        bot.send_message == (message.location)
        coords = geocoder(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, coords)
        us_longitude = message.location.longitude
        us_latitude = message.location.latitude
        us_location = coords
        us_projname = del_object2()
        print (us_projname)
        db_table_update(Latitude=us_latitude, Longitude=us_longitude, Location=us_location, ProjName=message.text)


def geocoder(latitude, longitude):
    token2 = 'pk.0a7f690b1ee2f5bc671e79241d167b57'
    headers = {"Accept-Language": "ru"}
    try:
        address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={token2}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
        return f'{address["address"].get("city")}, {address["address"].get("road")}, {address["address"].get("house_number")} '
    except Exception as e:
        return 'error'


def makeKeyboard():
    markup5 = types.ReplyKeyboardMarkup()
    obInfo1 = db_table_select()
    for result in obInfo1:
        markup5.add(types.KeyboardButton(text=result, request_location = True))
    return markup5

def delKeyboard():
    markup6 = types.InlineKeyboardMarkup()
    obInfo1 = db_table_select()
    for result in obInfo1:
        markup6.add(types.InlineKeyboardButton(text=result, callback_data="['del', '" + str(result) + "']"))
    return markup6

bot.polling(none_stop=True)