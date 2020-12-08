import confmat
from utils import read_classification_from_file
import os


SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'


def quality_score(tp, tn, fp, fn):
    quality = (tp+tn)/(tp+tn+10*fn+fp)
    return quality


def compute_quality_for_corpus(corpus_dir):

    bcm = confmat.BinaryConfusionMatrix(HAM_TAG, SPAM_TAG)
    truth = read_classification_from_file(corpus_dir+'/!truth.txt')
    prediction = read_classification_from_file(corpus_dir+'/!prediction.txt')
    bcm.compute_from_dicts(truth, prediction)
    comp = bcm.as_dict()
    score = quality_score(**comp)
    return score


if __name__ == '__main__':
    res = {'tp': 0, 'tn': 10, 'fp': 0, 'fn': 20}
    tn = 'tn'
    tp = 'tp'
    fp = 'fp'
    fn = 'fn'
    print(f'({res[tp]}+{res[tn]})/({res[tp]}+{res[tn]}+10*{res[fp]}+{res[fn]})')

    print('Quality: ', quality_score(**res))
