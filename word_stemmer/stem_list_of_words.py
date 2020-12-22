from . import porter


def stem_words(words):
    stemmer = porter.PorterStemmer()

    stemed = [stemmer.stem(plural) for plural in words]

    return stemed
