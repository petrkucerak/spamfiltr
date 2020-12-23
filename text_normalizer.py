import re
from utils import read_classification_from_file
from io import StringIO
from html.parser import HTMLParser
import string

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


class WordNormalizer:

    def load_stopwords(self):
        '''load premade list of stopwords form a file'''
        try:
            with open('stop_words.txt', 'r') as f:
                self.stopwords = f.read().splitlines()
            self.stopwords_loaded = True
            #print('loaded stopwords: ', self.stopwords)
        except:
            self.stopwords_loaded = False

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

        # decided not to use this since it had too many false positives
        # I just concider any 4-digit number a year
        #year_pat = re.compile(r'^\d{4}$')
        #self.patterns.append((year_pat, 'standardYearString'))

        # TODO: time pattern
        # TODO: date pattern
        #print('loaded patterns: ', self.patterns)

        repeting_sequence_pat = re.compile(r'^(.+)\1{4,}$')
        self.patterns.append((repeting_sequence_pat, 'standardRepeatingChars'))

    def __init__(self):

        self.load_stopwords()
        self.compile_patterns()

        self.html_tag_regex = re.compile('<.*?>')
        self.trailing_char_regex = re.compile('(\.|,|\?|:|!|\$|\')$')

    def normalize_words(self, words):
        '''replaces coplex structures such as mail adresses and urls with simplified strings'''
        new_words = []
        found = False
        for word in words:
            found = False
            for pattern in self.patterns:
                if pattern[0].match(word):
                    new_words.append(pattern[1])
                    found = True
                    break
            if not found:
                new_words.append(word)
        return new_words

    def normalize(self, text):
        '''takes a string and returns a list of normalized words'''
        text = text.lower()
        # need text instead of just a list of words for this
        clean_text = strip_tags(text)
        words = clean_text.split()
        words = [x for x in words if len(x) > 2]
        words = [x if x[-1].isalpha() else x[:-1] for x in words]
        if self.stopwords_loaded:
            words = [x for x in words if x not in self.stopwords]

        # TODO: decide if we want to keep this since it  doubles the time of this method
        words = stem_list_of_words.stem_words(words)

        words = self.normalize_words(words)

        return words


if __name__ == "__main__":
    wn = WordNormalizer()
    just_num_pat = re.compile(r'^-?\d+(\.|,\d+)?$')
    words = ["100", "10", "20", "50"]
    print(words)

    words = [w for w in words if just_num_pat.match(w)]
    print(words)

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
