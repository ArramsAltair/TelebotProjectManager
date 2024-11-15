
import telebot


class InlineKeyboard:

    def create_course_keyboard(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1", callback_data='course_1'),
            telebot.types.InlineKeyboardButton("2", callback_data='course_2'),


        )
        markup.row(
            telebot.types.InlineKeyboardButton("3", callback_data='course_3'),
            telebot.types.InlineKeyboardButton("4", callback_data='course_4'))
        return markup

    def create_institute_keyboard(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("ИОМ", callback_data='institute_1'),
            telebot.types.InlineKeyboardButton("ИГУиП", callback_data='institute_2'),
            telebot.types.InlineKeyboardButton("ИИС", callback_data='institute_3')
        )
        markup.row(
            telebot.types.InlineKeyboardButton("ИУПСиБК", callback_data='institute_4'),
            telebot.types.InlineKeyboardButton("ИЭФ", callback_data='institute_5'),
            telebot.types.InlineKeyboardButton("ИМ", callback_data='institute_6'))
        markup.row(
            telebot.types.InlineKeyboardButton("ИЗО", callback_data='institute_7'))
        return markup

    def create_direction_keyboard(self, institute):
        # Добавьте логику для выбора направлений, соответствующих институту
        markup = telebot.types.InlineKeyboardMarkup()
        if institute == 'ИОМ':
            markup.row(
                telebot.types.InlineKeyboardButton("Политическое управление", callback_data='direction_1')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Менеджмент креативных проектов", callback_data='direction_2')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Медиажурналистика", callback_data='direction_3')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Современный дизайн", callback_data='direction_4')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Психология", callback_data='direction_5')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Менеджмент", callback_data='direction_6')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Реклама и связи с общественностью", callback_data='direction_7')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Журналистика", callback_data='direction_8')
            )
        elif institute == 'ИГУиП':
            markup.row(
                telebot.types.InlineKeyboardButton("Государственное и муниципальное управление", callback_data='direction_9')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Менеджмент", callback_data='direction_10')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Юриспруденция", callback_data='direction_11')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Политология", callback_data='direction_12')
            )
        elif institute == 'ИИС':
            markup.row(
                telebot.types.InlineKeyboardButton("Бизнес-информатика", callback_data='direction_13')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Информационные технологии и системная аналитика",
                                                   callback_data='direction_14')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Бизнес-математика и анализ данных",
                                                   callback_data='direction_15')
            )
        elif institute == 'ИУПСиБК':
            markup.row(
                telebot.types.InlineKeyboardButton("Юриспруденция", callback_data='direction_16')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Международное право", callback_data='direction_17')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Управление персоналом", callback_data='direction_18')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Менеджмент", callback_data='direction_10')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Экономика", callback_data='direction_19')
            )
        elif institute == 'ИЭФ':
            markup.row(
                telebot.types.InlineKeyboardButton("Юриспруденция", callback_data='direction_16')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Международное право", callback_data='direction_17')
            )
        elif institute == 'ИМ':
            markup.row(
                telebot.types.InlineKeyboardButton("Юриспруденция", callback_data='direction_16')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Международное право", callback_data='direction_17')
            )
        elif institute == 'ИЗО':
            markup.row(
                telebot.types.InlineKeyboardButton("Юриспруденция", callback_data='direction_16')
            )
            markup.row(
                telebot.types.InlineKeyboardButton("Международное право", callback_data='direction_17')
            )
        return markup

    def create_a_time_keyboard(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("Утро", callback_data='a_time_1'),
            telebot.types.InlineKeyboardButton("День", callback_data='a_time_2'),
            telebot.types.InlineKeyboardButton("Вечер", callback_data='a_time_3')
        )
        return markup

    def create_p_time_keyboard(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("Утро", callback_data='p_time_1'),
            telebot.types.InlineKeyboardButton("День", callback_data='p_time_2'),
            telebot.types.InlineKeyboardButton("Вечер", callback_data='p_time_3')
        )
        return markup


    def create_team_type_keyboard(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("Участник команды", callback_data='team_participant'),
            telebot.types.InlineKeyboardButton("Консультант", callback_data='team_consultant')
        )
        return markup