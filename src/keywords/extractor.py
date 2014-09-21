import util.textprocess
from keywords import stopwords
import filter
import casing
import operator

stopwords.loadStopWords("../data/keywords/stopwords.txt")
filter.loadPositiveList("../data/keywords/positives.txt")
filter.loadNegativeList("../data/keywords/negatives.txt")
casing.loadCasings("../data/keywords/casings.txt")

from util.tokenizer import separatewords, splitSentences
from rake import calculateWordScores, generateCandidateKeywordScores
from stopwords import splitByStopWords
def extract(text):
    # Extracts keywords from text
    
    # preprocess, tokenize, group in n-grams
    text = util.textprocess.preprocess(text)
    sentences = [separatewords(sentence, 0) for sentence in splitSentences(text)]
    phrases = [phrase for sentence in sentences for phrase in splitByStopWords(sentence)]    
    phrases = [ngram for phrase in phrases for n in range(3) for ngram in generate_ngrams(phrase, n + 1)]    
    
    # filter
    filtered = [' '.join(ngram) for ngram in filter.filter(phrases)]
    
    # casings
    casings = {}
    for phrase in phrases:
        casings[' '.join(phrase)] = casing.normalize(phrase)
    
    # RAKE
    wordscores = calculateWordScores(phrases)        
    keywords = generateCandidateKeywordScores(phrases, wordscores)
    
    # Normalize scores
    maxWeight = max(keywords.values())
    if maxWeight > 0:
        for keyphrase in keywords.keys():
            keywords[keyphrase] /= maxWeight
    
    # format    
    keywords = sorted(keywords.iteritems(), key=operator.itemgetter(1), reverse=True)
    return [{'keyword':casings.setdefault(pair[0], pair[0]), 'weight':pair[1]} for pair in keywords if pair[0] in filtered]

def generate_ngrams(tokens, n):
    # generates ngrams
    return [tokens[start:start + n] for start in range(len(tokens) - n + 1)]

