from premade_data_loader import PremadeData
from mail import Mail
from text_normalizer import TextNormalizer
from os import listdir
from os.path import isfile, join
import time
from collections import Counter
import json
from utils import read_classification_from_file

bow = 'bow'
total_mails = 'total_mails'
average_word_count = 'average_word_count'
# TODO: implement word counter
min_words = 'min_words'
max_words = 'max_words'


if __name__ == '__main__':
    tn = TextNormalizer()

    mypath = 'spam-data-12-s75-h25/1'
    onlyfiles = [f for f in listdir(mypath) if isfile(
        join(mypath, f)) and not '!' in f]
    truth = read_classification_from_file(mypath+'/!truth.txt')
    start = time.time()
    ld = {
        total_mails: 0,
        max_words: float('-inf'),
        min_words: float('inf'),
        bow: {'ok': Counter(), 'spam': Counter()}
    }
    for file in onlyfiles:

        x = Mail(join(mypath, file))
        x.load(join(mypath, file))
        x.bag_of_words = tn.normalize(x.body)
        ld[bow][truth[file].lower()] += x.bag_of_words
        ld[total_mails] += 1
    print(
        "Went though {0} emails in {1}s. That is {2}ms per email".format(str(ld[total_mails]), round(time.time() - start, 4), round(1000*(time.time() - start)/ld[total_mails], 3)))
    for type in ld[bow].keys():
        ld[bow][type] = [(k, r)
                         for k, r in (ld[bow][type]).items() if r > 9]
        ld[bow][type].sort(key=lambda x: x[1], reverse=True)
    with open('json_data.json', 'w') as fp:
        json.dump(ld, fp)
