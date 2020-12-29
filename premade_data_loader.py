import json


class LoadData:
    stopwords = None

    def load_premade(self, filename):
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.stopwords = data['stopwords']
            self.prepared_data = data['prepared_data']
            return data

    def load_known(self, filename):
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.compiled_data = data['compiled_data']
            self.all_data = data['all_data']
            return data
