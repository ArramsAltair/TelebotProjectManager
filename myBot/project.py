class Project:
    def __init__(self):
        self.project_id = None
        self.creator_id = None
        self.name = None
        self.concept = None
        self.team_size = None
        #self.team_roles = None
        self.need_participant = None
        self.need_consultant = None
        self.required_skills = None
        self.required_help = None
        self.time_available = None

    def set_creator_id(self, creator_id):
        self.creator_id = creator_id

    def set_project_id(self, creator_id):
        self.project_id = creator_id


    def __str__(self):
        return  f"Создатель проекта: {self.creator_id}\n" \
                f"Название: {self.name}\n" \
                f"Концепция: {self.concept}\n" \
                f"Размер команды: {self.team_size}\n" \
                f"Нужен участник: {self.need_participant}\n" \
                f"Требуемые навыки: {self.required_skills}\n" \
                f"Нужен консультант: {self.need_participant}\n" \
                f"Требуемая помощь: {self.required_help}\n" \
                f"Время работы: {self.time_available}"

    def reset_project(self):
        id = self.creator_id
        dic = vars(self)
        for i in dic.keys():
            dic[i] = 0
        self.set_creator_id(id)