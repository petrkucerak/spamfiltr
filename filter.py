from corpus import Corpus
from utils import SPAM_TAG, HAM_TAG


class MyFilter:
    def train(self, train_dir):
        # TODO: implement training method
        raise NotImplementedError

    def test(self, test_dir):
        prediction = {}
        c = Corpus(test_dir)
        for filename, body in c.emails():
            my_prediction = self.classify(body)
            prediction[filename] = my_prediction
            print(f'Email {filename} is {my_prediction}')

    def classify(self, body):
        # TODO: implement classifier
        raise NotImplementedError
