from macros import *

# this is not necessary in this version of the project


class KnownMail:
    '''a simple class to hold all possible data about a known email'''
    name = None
    subject = None
    subject_length = None
    n_of_repeat_char_words = None
    word_count = None
    sender = None
    reply_chain = None
    word_counter = None
    n_of_other_recipients = None
    n_of_mentioned_mails = None
    n_of_urls = None
    bow_score = None
    n_of_normal_number = None

    def __init__(self, account_bow, file, mail):
        self.name = file
        self.n_of_repeat_char_words = account_bow(STANDARD_EMAIL_ADDRESS,
                                                  mail.bag_of_words)

        self.n_of_urls = account_bow(STANDARD_URL, mail.bag_of_words)

        self.n_of_mentioned_mails = account_bow(
            STANDARD_EMAIL_ADDRESS, mail.bag_of_words)

        self.n_of_urls = account_bow(
            STANDARD_PRICE, mail.bag_of_words)

        self.n_of_normal_number = account_bow(
            STANDARD_NUMBER, mail.bag_of_words)

        self.word_counter = mail.bag_of_words

        if mail.cc is not None:
            self.n_of_other_recipients = len(mail.cc)
        else:
            self.n_of_other_recipients = 0

        self.subject = mail.subject

        if mail.subject is not None:
            self.subject_length = len(mail.subject)
        else:
            self.subject_length = 0

        self.word_count = sum(mail.bag_of_words.values())


if __name__ == "__main__":
    km = KnownMail("Test_mail", subject="test subject",
                   n_of_repeat_char_words=12, word_count=156, sender="sender@sender.com", reply_chain=0, word_counter={'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6}, n_of_recipients=2)
    import json
    with open('new_data.json', 'w',  encoding='utf-8') as fp:
        json.dump(km.__dict__, fp, sort_keys=True, indent='\t')
