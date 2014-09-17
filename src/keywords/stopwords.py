stopwords = []

from util.util import loadWordList
def loadStopWords(path):
    global stopwords
    stopwords = loadWordList(path)

def splitByStopWords(tokens):
    global stopwords
    phrases = []
    phrase = []
    for token in tokens:
        if token in stopwords:
            if len(phrase) > 0:
                phrases.append(phrase)
                phrase = []
            continue
        phrase.append(token)
    if len(phrase) > 0:
        phrases.append(phrase)
    return phrases
