from mail import Mail
from text_normalizer import TextNormalizer
from naive_bayes import get_propabilities
from os.path import join,  isfile
from os import listdir
from macros import SPAM_TAG, HAM_TAG
from decimal import Decimal

# this skews close results towards being HAM since false positive is not as bad as false negative
BIAS = Decimal(6.5)


#TODO: documentation


class MyFilter:
    def train(self, train_dir):
        # Sadly don't have the time to implement this,
        # and it's not necessary as I've already prepared some data from the provided dataset
        pass

    def test(self, test_dir):

        tn = TextNormalizer()

        probabilities = get_propabilities()
        onlyfiles = [f for f in listdir(test_dir) if isfile(
            join(test_dir, f)) and not '!' in f]
        lines = []
        for file in onlyfiles:
            mail = Mail(join(test_dir, file))
            mail.load(join(test_dir, file))
            my_prediction = self.classify(mail.body, tn, probabilities)
            lines.append(f'{file} {my_prediction.upper()}')
        with open(join(test_dir, "!prediction.txt"), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def classify(self, body, tn, probabilities):
        type_chance, word_chance, unknown_word_chance = probabilities

        bag_of_words = tn.normalize(body)
        chances = {}
        for type in type_chance:
            propability = type_chance[type]
            propabilities = []
            for word in bag_of_words:
                if word in word_chance[type].keys():
                    try:
                        propabilities.append(word_chance[type][word])
                        propability *= word_chance[type][word]
                    except Exception as e:
                        print(type, word,
                              word_chance[type].keys(), '\n', e)
                        exit()

                else:
                    #print(f"Unknown word: {word} of type {type}")
                    propability *= unknown_word_chance[type]
            # print(propabilities)
            chances[type] = propability
        if chances[HAM_TAG]*BIAS > chances[SPAM_TAG]:
            return HAM_TAG
        else:
            return SPAM_TAG


if __name__ == '__main__':
    import time
    start = time.time()
    filter = MyFilter()

    filter.test('spam-data-12-s75-h25/1')
    print(time.time() - start)
