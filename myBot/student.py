# Класс для анкеты студента
class Student:
    alive = False
    accomplished = False

    def __init__(self):
        self.chat_id = None
        self.name = None
        self.course = None
        self.institute = None
        self.direction = None
        self.skills = None
        self.abilities = None
        self.time_available = None
        self.about = None
        self.portfolio = None
        self.alive = True
        self.accomplished = False

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def __str__(self):
        return f"ID студента: {self.chat_id}\n" \
               f"Имя: {self.name}\n" \
               f"Курс: {self.course}\n" \
               f"Институт: {self.institute}\n" \
               f"Направление: {self.direction}\n" \
               f"Навыки: {self.skills}\n" \
               f"Умения: {self.abilities}\n" \
               f"Время: {self.time_available}\n" \
               f"О себе: {self.about}\n" \
               f"Портфолио: {self.portfolio}"

    def data_student(self):
        return f"Студент: {self.chat_id}, Имя: {self.name}, Курс: {self.course}, Институт: {self.institute}, Направление: {self.direction}, Навыки: {self.skills}, Умения: {self.abilities}, Время: {self.time_available}, О себе: {self.about}, Портфолио: {self.portfolio}"

    def reset_student(self):
        id = self.chat_id
        dic = vars(self)
        for i in dic.keys():
            dic[i] = 0
        self.accomplished = False
        self.set_chat_id(id)