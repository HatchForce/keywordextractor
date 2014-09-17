import util.textprocess
from keywords import stopwords
import filter
import casing
import operator

stopwords.loadStopWords("../data/naive/stopwords.txt")
filter.loadPositiveList("../data/naive/positives.txt")
filter.loadNegativeList("../data/naive/negatives.txt")
casing.loadCasings("../data/naive/casings.txt")

from util.tokenizer import separatewords
from rake import calculateWordScores, generateCandidateKeywordScores
from stopwords import splitByStopWords
def extract(text):
    
    # preprocess, tokenize, group in n-grams
    text = util.textprocess.preprocess(text)     
    tokens = separatewords(text, 0)
    phrases = splitByStopWords(tokens)
    phrases = [ngram for phrase in phrases for n in range(3) for ngram in generate_ngrams(phrase, n + 1)]
    
    print phrases
    
    # filter
    filtered = [' '.join(ngram) for ngram in filter.filter(phrases)]
    print filtered
    
    # casings
    casings = {}
    for phrase in phrases:
        casings[' '.join(phrase)] = casing.normalize(phrase)
    print casings    
    
    # RAKE
    wordscores = calculateWordScores(phrases)        
    keywords = generateCandidateKeywordScores(phrases, wordscores)
    keywords = sorted(keywords.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    # format    
    return [{'keyword':casings.setdefault(pair[0], pair[0]), 'weight':pair[1]} for pair in keywords if pair[0] in filtered]

def generate_ngrams(tokens, n):
    # generates ngrams
    return [tokens[start:start + n] for start in range(len(tokens) - n + 1)]

