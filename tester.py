from math import log
from macros import CustomMacros
from premade_data_loader import LoadData
from mail import Mail
from text_normalizer import TextNormalizer
from os import listdir
from os.path import isfile, join
import time
from collections import Counter
import json
from utils import read_classification_from_file
import known_mail
from decimal import Decimal
import filter
padding = 1


def account_bow(key, bag_of_words):
    '''return value from bag of words if it exists, otherwise returns 0'''
    if key in bag_of_words:
        return bag_of_words[key]
    else:
        return 0


class LD:
    def __init__(self):
        self.count_per_type = {'ok': 0, 'spam': 0}
        self.word_count_per_type = {'ok': 0, 'spam': 0}

        self.total_mails = 0
        #self.max_words = float('-inf'),
        #self.min_words = float('inf'),
        self.bow = {'ok': Counter(), 'spam': Counter()}


def generate_known_mail(account_bow, file, mail):
    km = known_mail.KnownMail(name=file)

    km.n_of_repeat_char_words = account_bow(CustomMacros.notable_repeating_sequence,
                                            mail.bag_of_words)

    km.n_of_urls = account_bow(CustomMacros.standard_url, mail.bag_of_words)

    km.n_of_mentioned_mails = account_bow(
        CustomMacros.standard_email_address, mail.bag_of_words)

    km.n_of_urls = account_bow(
        CustomMacros.standard_price_string, mail.bag_of_words)

    km.n_of_normal_number = account_bow(
        CustomMacros.standard_pure_number, mail.bag_of_words)

    km.word_counter = mail.bag_of_words

    if mail.cc is not None:
        km.n_of_other_recipients = len(mail.cc)
    else:
        km.n_of_other_recipients = 0

    km.subject = mail.subject

    if mail.subject is not None:
        km.subject_length = len(mail.subject)
    else:
        km.subject_length = 0

    km.word_count = sum(mail.bag_of_words.values())
    #TODO: sender
    #TODO: reply_chain
    return km


def build_known(my_path):
    onlyfiles = [f for f in listdir(my_path) if isfile(
        join(my_path, f)) and not '!' in f]
    truth = read_classification_from_file(my_path+'/!truth.txt')
    total_spam_length = 0
    ld = LD()
    kmd = {'ok': [], 'spam': []}
    start = time.time()

    for file in onlyfiles:
        mail = Mail(join(my_path, file))
        mail.load(join(my_path, file))
        mail_type = truth[file].lower()

        mail.bag_of_words = tn.normalize(mail.body)

        km = generate_known_mail(account_bow, file, mail)
        kmd[mail_type].append(km)
        word_count = sum(mail.bag_of_words.values())
        ld.count_per_type[mail_type] += 1
        ld.word_count_per_type[mail_type] += word_count
        ld.bow[mail_type] += mail.bag_of_words
        ld.total_mails += 1
    print(
        "Went though {0} emails in {1}s. That is {2}ms per email".format(str(ld.total_mails), round(time.time() - start, 4), round(1000*(time.time() - start)/ld.total_mails, 3)))

    for type in ld.bow.keys():
        ld.bow[type] = [(k, r)
                        for k, r in (ld.bow[type]).items() if r > 0]
        ld.bow[type].sort(key=lambda x: x[1], reverse=True)
        ld.bow[type] = dict(ld.bow[type])

    for type in kmd:
        kmd[type] = [x.__dict__ for x in kmd[type]]

    data = {"compiled_data": ld.__dict__, "all_data": kmd}

    with open('known.json', 'w',  encoding='utf-8') as fp:
        json.dump(data, fp, indent=4)


def load_known():
    dl = LoadData()
    return dl.load_known('known.json')


def get_propabilities():
    compiled_data = load_known()['compiled_data']
    type_chance = {}
    for type in compiled_data['count_per_type']:
        type_chance[type] = Decimal(compiled_data['count_per_type'][type] /
                                    compiled_data['total_mails'])
    word_chance = {}
    unknown_word_chance = {}
    for type in compiled_data['bow']:
        unknown_word_chance[type] = Decimal(padding /
                                            compiled_data['word_count_per_type'][type]*10)
        word_chance[type] = {}
        for word in compiled_data['bow'][type]:
            word_chance[type][word] = Decimal((
                compiled_data['bow'][type][word]+padding) / compiled_data['word_count_per_type'][type]*10)
        # print(word_chance[type])
    return type_chance, word_chance, unknown_word_chance


if __name__ == '__main__':
    mf = filter.MyFilter()
    tn = TextNormalizer()
    build_known('spam-data-12-s75-h25/1')
    my_path = 'spam-data-12-s75-h25/1'
    probabilities = get_propabilities()
    onlyfiles = [f for f in listdir(my_path) if isfile(
        join(my_path, f)) and not '!' in f]
    truth = read_classification_from_file(my_path+'/!truth.txt')
    guesses = {}
    for file in onlyfiles:
        mail = Mail(join(my_path, file))
        mail.load(join(my_path, file))
        guesses[file] = mf.classify(mail.body, tn, probabilities)
    good_guesses = 0
    bad_guesses = 0
    for file in guesses:
        if str(truth[file]).lower() == str(guesses[file]).lower():
            good_guesses += 1
        else:
            bad_guesses += 1
        print(str(truth[file]).lower(), str(
            guesses[file]).lower())

    print(
        f'bad_guesses: {bad_guesses}, good_guesses: {good_guesses}, success: {good_guesses/(bad_guesses+good_guesses)}')
