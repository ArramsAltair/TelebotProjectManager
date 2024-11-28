import orjson

import fileReader

flRdr = fileReader.FileReader()

class  SearcherProjects:
    flRdr = fileReader.FileReader()

    def search_projects(self):
        path = 'projects/'
        file_resolution = '*.json'
        list_projects = flRdr.load_files(path, file_resolution)
        return  list_projects