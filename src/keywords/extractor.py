import util.textprocess
from keywords import stopwords
import filter
import casing
import operator
import idf

stopwords.loadStopWords("../data/keywords/stopwords.txt")
filter.loadPositiveList("../data/keywords/positives.txt")
filter.loadNegativeList("../data/keywords/negatives.txt")
casing.loadCasings("../data/keywords/casings.txt")
idf.loadIDF("../data/keywords/idf.txt")

from util.tokenizer import separatewords, splitSentences
from rake import calculateWordScores, generateCandidateKeywordScores
from filter import prefilter, postfilter
def extract(text):
    # Extracts keywords from text
    
    # preprocess, tokenize, group in n-grams
    text = util.textprocess.preprocess(text)
    sentences = [separatewords(sentence, 0) for sentence in splitSentences(text)]    
    phrases = [ngram for sentence in sentences for n in range(3) for ngram in generate_ngrams(sentence, n + 1)]    
    phrases = prefilter(phrases)
    
    # casings
    casings = {}
    for phrase in phrases:
        casings[' '.join(phrase)] = casing.normalize(phrase)
    
    # RAKE
    wordscores = calculateWordScores(phrases)        
    keywords = generateCandidateKeywordScores(phrases, wordscores)
    
    # Factor in IDF
    for keyphrase in keywords.keys():
        idfScore = idf.get(keyphrase)
        if idfScore == 0:
            del keywords[keyphrase]
            continue
        keywords[keyphrase] /= idfScore
                
    # Post filter    
    filtered = postfilter(keywords.keys())
    for keyphrase in keywords.keys():
        if keyphrase not in filtered:
            del keywords[keyphrase]    
    
    # Normalize scores
    if len(filtered) > 0:        
        maxWeight = max([keywords[keyphrase] for keyphrase in filtered])
        if maxWeight > 0:
            for keyphrase in keywords.keys():
                keywords[keyphrase] /= maxWeight
        
    # format
    keywords = sorted(keywords.iteritems(), key=operator.itemgetter(1), reverse=True)
    return [{"keyword":casings.setdefault(pair[0], pair[0]), "weight":pair[1]} for pair in keywords]

def generate_ngrams(tokens, n):
    # generates ngrams
    return [tokens[start:start + n] for start in range(len(tokens) - n + 1)]
