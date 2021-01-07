from macros import *
from mail import Mail
from text_normalizer import TextNormalizer
from os import listdir
from os.path import isfile, join
import time
from collections import Counter
import json
from utils import read_classification_from_file
from known_mail import KnownMail
from decimal import Decimal


def account_bow(key, bag_of_words):
    '''return value from bag of words if it exists, otherwise returns 0'''
    if key in bag_of_words:
        return bag_of_words[key]
    else:
        return 0


class LearnedData:
    '''a simple class to hold learned data'''

    def __init__(self):
        self.count_per_type = {HAM_TAG: 0, SPAM_TAG: 0}
        self.n_of_words_per_type = {HAM_TAG: 0, SPAM_TAG: 0}

        self.total_mails = 0
        #self.max_words = float('-inf'),
        #self.min_words = float('inf'),
        self.bow = {HAM_TAG: Counter(), SPAM_TAG: Counter()}


def build_known(my_path, tn):
    '''builds known.json form folder'''

    # get list of all files holding emails in a folder
    onlyfiles = [f for f in listdir(my_path) if isfile(
        join(my_path, f)) and not '!' in f]

    truth = read_classification_from_file(my_path+'/!truth.txt')
    ld = LearnedData()
    known_mail_dict = {HAM_TAG: [], SPAM_TAG: []}
    start = time.time()

    for file in onlyfiles:
        mail = Mail(join(my_path, file))
        mail.load(join(my_path, file))
        mail_type = truth[file]

        mail.bag_of_words = tn.normalize(mail.body)

        km = KnownMail(account_bow, file, mail)
        known_mail_dict[mail_type].append(km)
        n_of_words = sum(mail.bag_of_words.values())
        ld.count_per_type[mail_type] += 1
        ld.n_of_words_per_type[mail_type] += n_of_words
        ld.bow[mail_type] += mail.bag_of_words
        ld.total_mails += 1
    print(
        "Went though {0} emails in {1}s. That is {2}ms per email".format(str(ld.total_mails), round(time.time() - start, 4), round(1000*(time.time() - start)/ld.total_mails, 3)))

    for type in ld.bow.keys():
        # converts bag of words to list of tuples
        ld.bow[type] = [(k, r)
                        for k, r in (ld.bow[type]).items() if r > 0]
        # sorts list by value (descending)
        ld.bow[type].sort(key=lambda x: x[1], reverse=True)
        # converts back to dict
        ld.bow[type] = dict(ld.bow[type])

    # convets all KnownMail to a serializable dictionary
    for type in known_mail_dict:
        known_mail_dict[type] = [x.__dict__ for x in known_mail_dict[type]]

    # converts all learned data into a big serializable dictionary
    data = {"compiled_data": ld.__dict__, "all_data": known_mail_dict}

    # writes
    with open('known.json', 'w',  encoding='utf-8') as fp:
        json.dump(data, fp, indent=4)


if __name__ == '__main__':
    tn = TextNormalizer()
    build_known('spam-data-12-s75-h25/1', tn)
