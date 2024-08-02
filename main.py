import telebot
from telebot import types
import datetime

TOKEN = '7296525156:AAHutPoFku2sbg-hBMIF84ZsXhzq7Mm5TT0'

homework = {'Математика': "",
            "Русский язык": ""}

shedule = {1: "Понедельник:\n10:00 - Математика\n14:00 - Литература\n\n",
           2: "Вторник:\n09:00 - Английский язык\n13:00 - Физика\n\n",
           3: "Среда:\n09:00 - Русский язык\n13:00 - Литература\n\n",
           4: "Четверг:\n09:00 - Алгебра\n13:00 - Геометрия\n\n",
           5: "Пятница:\n09:00 - Английский язык\n13:00 - Физика\n\n"}


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['homework'])
def homework_def(message):
    user_id = message.from_user.id
    subjects = homework.keys()
    markup = types.InlineKeyboardMarkup()
    for subject in subjects:
        
        markup.add(types.InlineKeyboardButton(subject, callback_data=subject))
    bot.send_message(user_id, "Выбери предмет к которому хотел бы добавить домашнее задание.", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Получить расписание", callback_data='schedule'))
    bot.send_message(user_id, "Добро пожаловать в бот расписания нашей школы! Нажмите на кнопку ниже, чтобы получить расписание уроков.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in homework.keys())
def homework_call(call):
    bot.send_message(call.message.chat.id, "введите домашнее задание")
    bot.register_next_step_handler(call.message, h, subject=call.data)

def h(message,subject):
    homework[subject]=message.text
    bot.send_message(message.chat.id,'домашнее задание успешно сохранено')

@bot.callback_query_handler(func=lambda call: call.data == 'schedule')
def schedule(call):
    # Создание объекта datetime
    date = datetime.datetime.now() 
    # Вывод дня недели
    week =date.isoweekday()
    week =5
    if week in shedule:
        user_id = call.from_user.id
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=shedule[week])
    else:
        bot.send_message(call.message.chat.id,"Сейчас выходные дни")
    

def generate_schedule():
    schedule_text = "Расписание уроков на эту неделю:\n\n"
    schedule_text += "Понедельник:\n10:00 - Математика\n14:00 - Литература\n\n"
    schedule_text += "Вторник:\n09:00 - Английский язык\n13:00 - Физика\n\n"
    schedule_text += "Среда:\n09:00 - Русский язык\n13:00 - Литература\n\n"
    schedule_text += "Четверг:\n09:00 - Алгебра\n13:00 - Геометрия\n\n"
    schedule_text += "Пятница:\n09:00 - Английский язык\n13:00 - Физика\n\n"
    return schedule_text

bot.polling(none_stop=True)
