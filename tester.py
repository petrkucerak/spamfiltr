from mail import Mail
from text_normalizer import WordNormalizer
from os import listdir
from os.path import isfile, join
import time
from collections import Counter
import json
from utils import read_classification_from_file

if __name__ == '__main__':
    wn = WordNormalizer()
    mypath = 'spam-data-12-s75-h25/1'
    onlyfiles = [f for f in listdir(mypath) if isfile(
        join(mypath, f)) and not '!' in f]
    truth = read_classification_from_file(mypath+'/!truth.txt')
    start = time.time()
    # for eachfile in onlyfiles:
    i = 0
    total_bow = {'ok': Counter({}), 'spam': Counter({})}
    for file in onlyfiles:
        x = Mail(join(mypath, file))
        x.load(join(mypath, file))
        x.bag_of_words = Counter(wn.normalize(x.body))
        total_bow[truth[file].lower()] += x.bag_of_words
        i += 1
    print(
        f"Went though {i} emails in {round(time.time() - start,4)}s. That is {round(1000*(time.time() - start)/i,3)}ms per email")
    for type in total_bow.keys():
        total_bow[type] = [(k, r)
                           for k, r in (total_bow[type]).items() if r > 9]
        total_bow[type].sort(key=lambda x: x[1], reverse=True)
    with open('json_data.json', 'w') as fp:
        json.dump(total_bow, fp)
