import json


class LoadData:
    stopwords = None

    def load_premade(self):
        '''loads data from premade.json'''
        with open('premade.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.stopwords = data['stopwords']
            return data

    def load_known(self):
        '''loads data from known.json'''
        with open('known.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.compiled_data = data['compiled_data']
            self.all_data = data['all_data']
            return data
