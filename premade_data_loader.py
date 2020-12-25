import json


class PremadeData:
    stopwords = None

    def __init__(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self.stopwords = data['stopwords']
