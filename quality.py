import confmat
from utils import read_classification_from_file
from macros import SPAM_TAG, HAM_TAG
import os


def quality_score(tp, tn, fp, fn):
    '''calculates quality score base on predefined formula'''
    quality = (tp+tn)/(tp+tn+10*fn+fp)
    return quality


def compute_quality_for_corpus(corpus_dir):
    '''returns quality for !preditions.txt and !truth.txt in a folder'''
    bcm = confmat.BinaryConfusionMatrix(HAM_TAG, SPAM_TAG)
    truth = read_classification_from_file(corpus_dir+'/!truth.txt')
    prediction = read_classification_from_file(corpus_dir+'/!prediction.txt')
    bcm.compute_from_dicts(truth, prediction)
    comp = bcm.as_dict()
    score = quality_score(**comp)
    return score


if __name__ == '__main__':
    print('Quality: ', compute_quality_for_corpus('spam-data-12-s75-h25/1'))
