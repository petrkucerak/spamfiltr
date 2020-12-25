import re
from utils import read_classification_from_file
from io import StringIO
from html.parser import HTMLParser
import string
from collections import Counter
import time
from premade_data_loader import PremadeData

# I've used the porter_stemmer method from the nltk library
#   (I've only copied the necessary files to run this method and am not using anything else from nltk)
try:
    from word_stemmer import stem_list_of_words
    stemmer_imported = True
except:
    stemmer_imported = False


class MLStripper(HTMLParser):
    # TODO: check where I got this
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class TextNormalizer:

    def compile_patterns(self):
        '''precompiles regex patterns'''
        self.patterns = []

        # replaces a email adresses with 'standardEmailAddress'
        mail_pat = re.compile(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
        self.patterns.append((mail_pat, 'standardEmailAddress'))

        # replaces soemthing that is purely numerical (may be negative or decimal)
        just_num_pat = re.compile(r'^-?\d+(\.|,\d+)?$')
        self.patterns.append((just_num_pat, 'standardPureNumber'))

        phone_pat = re.compile(
            r"[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}", re.IGNORECASE)
        self.patterns.append((phone_pat, 'standardPhoneNumber'))
        # TODO: figure out where I got this (had this saved in my regex cheat sheet for years)
        url_pat = re.compile(
            r'(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|'  # or ip
            r'(www\.[a-zA-Z0-9]+\.)'    # or 'www.something.
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)', re.IGNORECASE)
        self.patterns.append((url_pat, 'standardUrlString'))

        ip_pat = re.compile(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        self.patterns.append((ip_pat, 'standardIpAddress'))

        price_pat = re.compile(r'^\$\d+(\.|,\d+)?$')
        self.patterns.append((price_pat, 'standardPriceString'))

        # TODO: time pattern
        # TODO: date pattern
        #print('loaded patterns: ', self.patterns)

        repeting_sequence_pat = re.compile(r'^(.+)\1{6,}$')
        self.patterns.append((repeting_sequence_pat, 'notableRepeatingChars'))

    def __init__(self):

        self.compile_patterns()

        self.leading_char_regex = re.compile(r'^\(')
        # FIXME: No idea why this regex doesnt work
        self.unwanted_char_regex = re.compile(r'=|\\|\"')
        self.repeting_sequence_pat = re.compile(r'^(.+)\1{2,}$')

        self.pm = PremadeData('data.json')

    def normalize_words(self, words):
        '''replaces coplex structures such as mail adresses and urls with simplified strings'''
        # TODO: make it so this returns two list of words, so the nomralized strings don't have to go though stemming
        new_words = []
        pattern_counter = Counter({})

        for pattern in self.patterns:
            pattern_counter[pattern[1]] = 0

        found = False
        for word in words:
            found = False
            for pattern in self.patterns:
                if pattern[0].match(word):
                    pattern_counter[pattern[1]] += 1
                    found = True
                    break
            if not found:
                new_words.append(word)
        word_counter = Counter(new_words)
        return (word_counter, pattern_counter)

    def remove_unwanted(self, counter):
        list = dict(counter).items()
        list = [(x, y) for x, y in list
                if not self.unwanted_char_regex.match(x)]
        return Counter(dict(list))

    def normalize(self, text):
        '''takes a string and returns a list of normalized words'''
        text = text.lower()
        # need text instead of just a list of words for this
        clean_text = strip_tags(text)
        words = clean_text.split()

        # ignores words shorter than 3 characters
        words = [x for x in words if len(x) > 2]

        # removes trailing special characters from words
        words = [x if x[-1].isalnum() else x[:-1] for x in words]

        # removes unwanted first characters from words
        words = [x[1:] if self.leading_char_regex.match(
            x) else x for x in words]

        # removes stopwords (words that won't help us with evaluating if the mail is spam
        #   like pronouns, sentence connectors and such)
        words = [x for x in words if x not in self.pm.stopwords]

        counters = self.normalize_words(words)
        word_counter = self.remove_unwanted(counters[0])
        final_counter = counters[1]
        final_counter += stem_list_of_words.stem_words(word_counter)

        return final_counter


# TODO: need to figure out how these passing
#        ["$19.9", 16],
#        ["$1,000,00", 15],

#        ["=3c=2fdiv=3", 15],
#        ["=09=0", 43],

#        ["--deathtospamdeathtospamdeathtospam-", 31],

#        ["it'", 61], (the ' at the end)
#        ["company'", 13],

#        ["(and", 15],

#        ["..", 14],
#        ["==", 47],

#        ["[1", 12],

#        ["-----origin", 10],
#        ["message----", 10],

#        ["=2", 120],

#        ["{margin-right:0cm", 80],
#        ["text-decoration:underline;", 49],
#        ["font-size:9.0pt", 25],
#

#        ["charset=\"iso-8859-1", 65],
