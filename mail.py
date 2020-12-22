import re


class Mail:
    bag_of_words = {}

    def __init__(self, *file_name):
        self.mail_name = file_name

        self.header_meta = {}
        self.body = None  # load mail body as a string

        self.to = None
        self.cc = None
        self.subject = None
        self.date = None

    def stringify(self):
        if self.body is not None:
            body = self.body[:95]+"..."
        else:
            body = "None"

        if self.to is not None:
            to = self.to
        else:
            to = "None"
        if self.cc is not None:
            cc = self.cc
        else:
            cc = "None"
        if self.subject is not None:
            subject = self.subject
        else:
            subject = "None"
        if self.date is not None:
            date = self.date
        else:
            date = "None"
        return f"Adresater: {to}\nCopy: {cc}\nSubject: {subject}\nDate: {date}\nBody: {body}\n"

    def __repr__(self):
        return self.stringify()

    def __str__(self):
        return self.stringify()

    def load(self, filepath):
        # load metadata in email header to direction
        # line by line
        metadata = ''
        with open(filepath, 'r', encoding='utf-8') as file:
            line = ''
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

        # TODO
        # problem with:
        # - Recivied
        # - X-Spam-Status

        self.to = self.header_meta.get("To")
        self.cc = self.header_meta.get("Cc")
        self.subject = self.header_meta.get("Subject")
        self.date = self.header_meta.get("Date")


if __name__ == "__main__":

    mail_test = Mail()
    # mail_test.load('spam-data-12-s75-h25/1/1735.767c727c118916606982501980deb249')
    # mail_test.load('spam-data-12-s75-h25/1/01392.6a9e94b131381aa631022fc1b6c9bdab')
    mail_test.load(
        'spam-data-12-s75-h25/1/01359.deafa1d42658c6624c6809a446b7f369')

    # test print header meta
    # for k, v in mail_test.header_meta.items():
    #     print(k + ":", v)

    # test print mail body
    # print(mail_test.body)

    # test print basic info of mail
    print("Adresater:", mail_test.to, '\n\n\n')
    print("Copy:", mail_test.cc, '\n\n\n')
    print("Subject:", mail_test.subject, '\n\n\n')
    print("Date:", mail_test.date, '\n\n\n')
    print(f"Body: \033[94m{mail_test.body}\033[0m")
