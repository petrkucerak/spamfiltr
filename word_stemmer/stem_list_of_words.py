from . import porter
from collections import Counter


def stem_words(words):
    stemmer = porter.PorterStemmer()
    stemed = {}
    for word in words:
        stemed_word = stemmer.stem(word)
        if stemed_word in stemed:
            stemed[stemed_word] += words[stemed_word]
        else:
            stemed[stemed_word] = words[stemed_word]

    return Counter(stemed)
