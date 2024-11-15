class Project:
    def __init__(self):
        self.chat_id = None
        self.name = None
        self.concept = None
        self.team_size = None
        #self.team_roles = None
        self.need_participant = None
        self.need_consultant = None
        self.required_skills = None
        self.required_help = None
        self.time_available = None

    def setChatId(self, chat_id):
        self.chat_id = chat_id

    def __str__(self):
        return f"Создатель проекта: {self.chat_id}\n" \
               f"Название: {self.name}\n" \
               f"Концепция: {self.concept}\n" \
               f"Размер команды: {self.team_size}\n" \
               f"Нужен участник: {self.need_participant}\n" \
               f"Требуемые навыки: {self.required_skills}\n" \
               f"Нужен консультант: {self.need_participant}\n" \
               f"Требуемая помощь: {self.required_help}\n" \
               f"Время работы: {self.time_available}"

    def resetProject(self):
        id = self.chat_id
        dic = vars(self)
        for i in dic.keys():
            dic[i] = 0
        self.setChatId(id)