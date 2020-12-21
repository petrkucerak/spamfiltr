import re
from data import stopwords

class Mail:
    
    def __init__(self, *file_name):
        self.mail_name = file_name
        
        self.header_meta = {}
        self.body = None # load mail body as a list by words

        self.to = None
        self.cc = None
        self.subject = None
        self.date = None

    def load(self, filepath):
        # load metadata in email header to direction
        # line by line
        metadata = ""
        with open(filepath, 'r', encoding='utf-8') as file:
            line = ""
            while line != '\n':
                line = file.readline()
                metadata += line
            
            # load rest of the text as mail body
            self.body = file.read()
        
        # delete whitespaces
        metadata = re.sub('\n( +|\t+|\t+ +)', '; ', metadata)
        # split methadat into direction
        for i in metadata.strip().split('\n'):
            i = i.split(': ', 1)
            if len(i) == 2:
                self.header_meta[i[0]] = i[1]
        
        # TODO: problem with loading metadata
        # - Recivied
        # - X-Spam-Status

        self.to = self.header_meta.get("To")
        self.cc = self.header_meta.get("Cc")
        self.subject = self.header_meta.get("Subject")
        self.date = self.header_meta.get("Date")

        # convert mail body from string into list of words for better manipulation
        self.mail_body_string_to_list()

    def remove_stop_words(self):
        '''remove stopwords in mail body'''
        for word in list(self.body):  # iterating on a copy since removing will mess things up
            if word in stopwords:
                self.body.remove(word)
            
    
    def mail_body_string_to_list(self):
        self.body = self.body.split()
    

if __name__ == "__main__":
    
    mail_test = Mail()
    mail_test.load('spam-data-12-s75-h25/1/1735.767c727c118916606982501980deb249')
    # mail_test.load('spam-data-12-s75-h25/1/01392.6a9e94b131381aa631022fc1b6c9bdab')
    # mail_test.load('spam-data-12-s75-h25/1/00039.889d785885f092c269741b11f2124dce')
    
    # print("====================")
    # print("MAIL HEADER")
    # print("====================")
    # test print header meta
    # for k, v in mail_test.header_meta.items():
    #     print(k + ":", v)
    
    # print()
    # print("====================")
    # print("MAIL BODY")
    # print("====================")

    # test print mail body
    # print(mail_test.body)

    # test print basic info of mail
    # print("Adresater:", mail_test.to)
    # print("Copy:", mail_test.cc)
    # print("Subject:", mail_test.subject)
    # print("Date:", mail_test.date)

    # test delete stopwords
    mail_test.remove_stop_words()
    print(mail_test.body)