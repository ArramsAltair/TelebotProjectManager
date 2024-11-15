import glob
import json
import os
import orjson

class FileReader:

    def open_profile_file(self, stdn):
        path = f"profiles/{stdn.chat_id}.json"
        if(os.path.exists(path)):
            with open(path, 'r') as f:
                data = orjson.loads(f.read())
                #print(data)
                stdn.name = data['name']
                stdn.course = data['course']
                stdn.institute = data['institute']
                stdn.direction = data['direction']
                stdn.skills = data['skills']
                stdn.abilities = data['abilities']
                stdn.time_available = data['time_available']
                stdn.about = data['about']
                stdn.portfolio = data['portfolio']
                stdn.accomplished = True
                print(stdn.__str__())
        else:
            stdn.resetStudent()

    def write_profile_in_file(self, stdn):
        path = f'profiles/{stdn.chat_id}.json'
        data = stdn.data()
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def write_profile_in_json_file(self, stdn):
        path = f'profiles/{stdn.chat_id}.json'
        data = {
            "chat_id": f"{stdn.chat_id}",
            "name": f"{stdn.name}",
            "course": f"{stdn.course}",
            "institute": f"{stdn.institute}",
            "direction": f"{stdn.direction}",
            "skills": f"{stdn.skills}",
            "abilities": f"{stdn.abilities}",
            "time_available": f"{stdn.time_available}",
            "about": f"{stdn.about}",
            "portfolio": f"{stdn.portfolio}"
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def open_project_file(self, prjct):
        path = f"projects/{prjct.chat_id}.json"
        if (os.path.exists(path)):
            with open(path, 'r') as f:
                data = orjson.loads(f.read())
                # print(data)
                prjct.name = data['name']
                prjct.concept = data['concept']
                prjct.team_size = data['team_size']
                prjct.need_participant = data['need_participant']
                prjct.need_consultant = data['need_consultant']
                prjct.required_skills = data['required_skills']
                prjct.required_help = data['required_help']
                prjct.time_available = data['time_available']
                prjct.accomplished = True
                print(prjct.__str__())
        else:
            prjct.resetProject()

    def write_project_in_json_file(self, prjct):
        path = f'projects/{prjct.chat_id}.json'
        data = {
            "chat_id": f"{prjct.chat_id}",
            "name": f"{prjct.name}",
            "concept": f"{prjct.concept}",
            "team_size": f"{prjct.team_size}",
            "need_participant": f"{prjct.need_participant}",
            "need_consultant": f"{prjct.need_consultant}",
            "required_skills": f"{prjct.required_skills}",
            "required_help": f"{prjct.required_help}",
            "time_available": f"{prjct.time_available}"
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def load_projects(self, projects):
        path = '/projects'
        for filename in glob.glob(os.path.join(path, '*.json')):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
                projects.update(data = orjson.loads(f.read()))