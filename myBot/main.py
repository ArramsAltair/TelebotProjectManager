import asyncio
import logging
import sys
import time
from asyncio import wait_for, timeout
from random import randint

import telebot
import configparser

from telebot.apihelper import send_message

import dictionary
import fileReader
import student
import project
import inlineKeyboard
import searcherProjects

config = configparser.ConfigParser()

# Подключение бота
config.read("settings.ini")
TOKEN = config["Telebot"]["TOKEN_BOT"]
ADMIN = config["Telebot"]["ID"]
bot = telebot.TeleBot(TOKEN)

# Словари для хранения данных
students = {}
projects = {}

courses = dictionary.courses
institutes = dictionary.institutes
directions = dictionary.directions
time_available = dictionary.time_available

#init
stdn = student.Student()
prjct = project.Project()
flRdr = fileReader.FileReader()
inlnKb = inlineKeyboard.InlineKeyboard()
searcher_p = searcherProjects.SearcherProjects()

#fields
profile_edit = False
project_edit = False
do = True



# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def set_chat_id(id):
    stdn.chat_id = id

def set_id_for_new_project(id):
    prjct.set_creator_id(id)
    prjct.set_project_id(id)


def main_menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    if not stdn.accomplished:
        markup.row(
            telebot.types.InlineKeyboardButton("Заполнить анкету\nстудента", callback_data='student_form'),
        )
        markup.row(
            telebot.types.InlineKeyboardButton("Заполнить карточку\nпроекта", callback_data='project_form')
        )
    elif stdn.accomplished:
        markup.row(
            telebot.types.InlineKeyboardButton("Заполнить анкету\nстудента заново", callback_data='student_form'),
        )
        markup.row(
            telebot.types.InlineKeyboardButton("Посмотреть анкету\nстудента",
                                               callback_data='student_accomplished_form'),
        )
        markup.row(
            telebot.types.InlineKeyboardButton("Заполнить карточку\nпроекта", callback_data='project_form')
        )
    markup.row(
        telebot.types.InlineKeyboardButton("Поиск проектов", callback_data='search'),
        telebot.types.InlineKeyboardButton("Случайный проект", callback_data='random')
    )
    markup.add(telebot.types.InlineKeyboardButton("Техническая поддержка", callback_data='support'))
    bot.send_message(message.chat.id,
                     "Привет! Я бот, который поможет тебе найти команду для проекта или найти проект, который тебе подходит.  Что ты хочешь сделать?",
                     reply_markup=markup)
    send_message_log(f"С ботом взаимодействует пользователь: {message.chat.id}")

def send_message_log(str):
    bot.send_message(ADMIN, str)

@bot.message_handler(commands=['stop'])
def stop_command(message):
    if message.chat.id == int(ADMIN):
        send_message_log("Завершение работы бота")
        bot.stop_polling()
        try:
            wait_for(10)
        except:
            print("Завершение работы!")
        sys.exit(0)

@bot.message_handler(commands=['start'])
def start_command(message):
    logging.info('Пользователь вошел в чат')
    set_chat_id(message.chat.id)
    flRdr.open_profile_file(stdn)
    stdn.name = message.from_user.first_name
    main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'student_accomplished_form')
def student_form(call):
    chat_id = call.message.chat.id
    logging.info('Пользователь просматривает свою анкету')
    if stdn.accomplished and stdn.chat_id == call.message.chat.id:
        bot.send_message(chat_id, "Анкета студента:\n\n" + stdn.__str__())
    else:
        bot.send_message(chat_id,"Анкета пуста")
    bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")

@bot.callback_query_handler(func=lambda call: call.data == 'student_form')
def student_form(call):
    logging.info('Пользователь начал заполнение анкеты')
    profile_edit = True
    bot.send_message(call.message.chat.id, "Заполните анкету студента:\n\n1. Выберите курс обучения:", reply_markup=inlnKb.create_course_keyboard())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('course_'))
def course_question(call):
    logging.info('Пользователь выбирает институт')
    stdn.course = courses[call.data]
    bot.send_message(call.message.chat.id, "2. Выберите ваш институт:", reply_markup=inlnKb.create_institute_keyboard())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('institute_'))
def institute_question(call):
    logging.info('Пользователь выбирает направление подготовки')
    stdn.institute = institutes[call.data]
    bot.send_message(call.message.chat.id, "3. Выберите ваше направление подготовки:", reply_markup=inlnKb.create_direction_keyboard(stdn.institute))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('direction_'))
def direction_question(call):
    logging.info('Пользователь сообщает о своих навыках')
    stdn.direction = directions[call.data]
    bot.send_message(call.message.chat.id, "4. Ваши навыки (soft skills):\n\nВведите навыки через запятую, например: коммуникация, лидерство, креативность")
    bot.register_next_step_handler(call.message, skills_question)

@bot.message_handler(func=lambda message: message.chat.id and profile_edit)
def skills_question(message):
    logging.info('Пользователь сообщает о своих умениях')
    stdn.skills = message.text.split(',')
    bot.send_message(message.chat.id,"5. Ваши умения (hard skills):\n\nВведите умения через запятую, например: Python, HTML, Excel")
    bot.register_next_step_handler(message, abilities_question)

@bot.message_handler(func=lambda message: message.chat.id and profile_edit)
def abilities_question(message):
    logging.info('Пользователь сообщает, сколько может уделять времени проекту')
    stdn.abilities = message.text.split(f',')
    bot.send_message(message.chat.id, "6. В какое время суток Вы готовы уделять внимание проекту?", reply_markup=inlnKb.create_a_time_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('a_time_'))
def time_question(call):
    logging.info('Пользователь рассказывает о себе')
    stdn.time_available = time_available[call.data]
    bot.send_message(call.message.chat.id, "7. Расскажите о себе:")
    bot.register_next_step_handler(call.message, about_question)

@bot.message_handler(func=lambda message: message.chat.id  and profile_edit)
def about_question(message):
    logging.info('Пользователь сообщает, есть ли у него портфолио')
    stdn.about = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("У меня есть портфолио", callback_data='portfolio_yes'),
        telebot.types.InlineKeyboardButton("У меня нет портфолио", callback_data='portfolio_no')
    )
    bot.send_message(message.chat.id, "8. У вас есть портфолио?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith ('portfolio_'))
def portfolio_finish(call):
    try:
        if call.data =='portfolio_yes':
            stdn.portfolio = 'Есть'
        elif call.data =='portfolio_no':
            stdn.portfolio = 'Нет'

    except:
        logging.info('Ошибка заполнения анкеты ')
        bot.send_message(call.message.chat.id,'Ошибка заполнения анкеты!')
    else:
        logging.info('Пользователь закончил заполнение анкеты')
        profile_edit = False
        flRdr.write_profile_in_json_file(stdn)
        bot.send_message(call.message.chat.id, "Анкета студента успешно заполнена!\n\n"+stdn.__str__())
        bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")



# Карточка проекта
@bot.callback_query_handler(func=lambda call: call.data == 'project_form')
def project_form(call):
    project_edit = True
    set_id_for_new_project(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Заполните карточку проекта:\n\n1. Укажите название/тему вашего проекта:")
    bot.register_next_step_handler(call.message, project_name_question)

@bot.message_handler(func=lambda message: message.chat.id and project_edit)
def project_name_question(message):
    prjct.name = message.text
    bot.send_message(message.chat.id, "2. Укажите концепцию вашего проекта:")
    bot.register_next_step_handler(message, project_concept_question)

@bot.message_handler(func=lambda message: message.chat.id and project_edit)
def project_concept_question(message):
    prjct.concept = message.text
    bot.send_message(message.chat.id, "3. Укажите количество участников в вашей команде на данный момент:")
    bot.register_next_step_handler(message, project_team_size_question)

@bot.message_handler(func=lambda message: message.chat.id and project_edit)
def project_team_size_question(message):
    prjct.team_size = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("Участник команды", callback_data='team_participant'),
        telebot.types.InlineKeyboardButton("Консультант", callback_data='team_consultant')
    )
    bot.send_message(message.chat.id, "4. Укажите, вам нужен участник команды или консультант?",  reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('team_'))
def project_team_type_question(call):
    if call.data == 'team_participant':
        prjct.need_participant = "Да"
        bot.send_message(call.message.chat.id, "5. Укажите, какие навыки участника вам требуются:")
    elif call.data == 'team_consultant':
        prjct.need_participant = "Нет"
        bot.send_message(call.message.chat.id, "5. Укажите, какая требуется помощь от консультанта?")
    bot.register_next_step_handler(call.message, project_required_skills_question)

@bot.message_handler(func=lambda message: message.chat.id and project_edit)
def project_required_skills_question(message):
    if prjct.need_participant == "Да":
        prjct.required_skills = message.text.split(',')
        prjct.required_help = "Не нужна"
    elif prjct.need_participant == "Нет":
        prjct.required_help = message.text.split(',')
        prjct.required_skills = "Не нужны"
    bot.send_message(message.chat.id, "6. Укажите в какое время суток ваша команда работает над проектом:", reply_markup=inlnKb.create_p_time_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith('p_time_'))
def project_time_available_question(call):
    prjct.time_available = time_available[call.data]
    project_edit = False
    try:
        flRdr.write_project_in_json_file(prjct)
    except:
        bot.send_message(call.message.chat.id, "Ошибка записи карточки проекта")
    else:
        bot.send_message(call.message.chat.id, "Карточка проекта успешно заполнена!")
        bot.send_message(call.message.chat.id,f"Карточка проекта:\n{prjct.__str__()}")
    bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")

# Поиск проекта
@bot.callback_query_handler(func=lambda call: call.data == 'search')
def search_project(call):
    try:
        _list_projects = searcher_p.search_projects()
        for i in range(0, len(_list_projects)):
            bot.send_message(call.message.chat.id,(f"ID проекта: {_list_projects[i].get('project_id')}. Имя проекта: {_list_projects[i].get('name')}"))
    except:
        bot.send_message(call.message.chat.id, "Не удается открыть проекты.\nПовторите попытку еще раз")

    bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")


# Техническая поддержка
@bot.callback_query_handler(func=lambda call: call.data == 'support')
def support(call):
    bot.send_message(call.message.chat.id, "Свяжитесь с технической поддержкой по адресу: support@example.com")
    bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")

# Поиск случайного проекта
@bot.callback_query_handler(func=lambda call: call.data == 'random')
def search_random_project(call):
    try:
        projects = searcher_p.search_projects()
        random_project = set_random_project(projects)
        _prjct = project_project(prjct, random_project)
    except:
        bot.send_message(call.message.chat.id,"Не удается открыть проект.\nПовторите попытку еще раз")
    else:
        bot.send_message(call.message.chat.id,f"Случайный проект:\n{_prjct.__str__()}:")
    bot.send_message(call.message.chat.id, "Для возврата в меню -> /start")


def set_random_project(projects):
    rand_project = randint(0, len(projects))
    return projects[rand_project]

def project_project(project1, project2):
    project1.project_id = project2['project_id']
    project1.creator_id = project2['creator_id']
    project1.name = project2['name']
    project1.concept = project2['concept']
    project1.team_size = project2['team_size']
    project1.need_participant = project2['need_participant']
    project1.need_consultant = project2['need_consultant']
    project1.required_skills = project2['required_skills']
    project1.required_help = project2['required_help']
    project1.time_available = project2['time_available']
    project1.accomplished = True
    return project1

def bot_start():
    try:
        send_message_log("Бот запущен")
        print("Бот запущен")
        bot.polling()
    except:
        print("Не удалось запустить бота\nПовторная попытка запуска")
        time.sleep(5)
        bot_start()
    else:
        return

# Запуск бота
if __name__ == '__main__':
    bot_start()
    print("Бот остановлен")

