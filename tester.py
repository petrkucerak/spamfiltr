from mail import Mail
from text_normalizer import WordNormalizer
from os import listdir
from os.path import isfile, join
import time
from collections import Counter
import json


if __name__ == '__main__':
    wn = WordNormalizer()
    mypath = 'spam-data-12-s75-h25/2'
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(
        join(mypath, f)) and not '!' in f]
    start = time.time()
    # for eachfile in onlyfiles:
    i = 0
    total_bow = Counter({})
    for file in onlyfiles:
        x = Mail(file)
        x.load(file)
        x.bag_of_words = Counter(wn.normalize(x.body))
        total_bow += x.bag_of_words
        i += 1
    print(i, time.time() - start)
    trimed_bow = []
    for word in total_bow.keys():
        if total_bow[word] > 1:
            trimed_bow.append((word, total_bow[word]))
    trimed_bow.sort(key=lambda x: x[1], reverse=True)
    with open('json_data.json', 'w') as fp:
        json.dump(trimed_bow, fp)
