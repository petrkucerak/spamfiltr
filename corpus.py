import os


class Corpus:

    def __init__(self, corpus_dir):
        self.corpus_dir = corpus_dir

    def emails(self):
        filenames = os.listdir(self.corpus_dir)
        for filename in filenames:
            if filename[0] == '!':
                continue

            with open(self.corpus_dir+'/'+filename, 'r', encoding='utf-8') as file:
                emailbody = file.read()
                yield filename, emailbody
