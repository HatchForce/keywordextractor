import web
import json

# Uncomment and adjust if java executable cannot be found
#import os
#os.environ['JAVAHOME']="/usr"

# Uncomment if Crackr source is not in $PYTHONPATH and
# Crackr has been cloned into parent directory of this 
# project
#import sys
#sys.path.append("../../../../Crackr/webserver")
#sys.path.append("../../../../Crackr/webserver/RAKE")
        
# Webservice endpoint declarations
urls = (
    '/rake', 'RakePre',
    '/crackr', 'CrackrPre',
    '/naive', 'NaivePre',
    '/none/rake', 'RakeNone',
    '/none/crackr', 'CrackrNone',
    '/none/naive', 'NaiveNone',
    '/pre/rake', 'RakePre',
    '/pre/crackr', 'CrackrPre',
    '/pre/naive', 'NaivePre',
    '/post/rake', 'RakePost',
    '/post/crackr', 'CrackrPost',
    '/post/naive', 'NaivePost'
)
app = web.application(urls, globals())

import datetime
def log(text):
    print datetime.datetime.utcnow()
    print text

# Webservide endpoint definitions 
class RakeNone:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')        
        return json.dumps(rake(web.data(), skillfilter=None))
    
class CrackrNone:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')        
        return json.dumps(crackr(web.data(), skillfilter=None))
    
class NaiveNone:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')        
        return json.dumps(naive(web.data(), skillfilter=None))
    
class RakePre:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(rake(web.data(), skillfilter='pre'))
    
class CrackrPre:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')        
        return json.dumps(crackr(web.data(), skillfilter='pre'))
    
class NaivePre:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')        
        return json.dumps(naive(web.data(), skillfilter='pre'))
    
class RakePost:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(rake(web.data(), skillfilter='post'))
    
class CrackrPost:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(crackr(web.data(), skillfilter='post'))
    
class NaivePost:
    def POST(self):
        log(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(naive(web.data(), skillfilter='post'))
    
# Algorithms

from candygen import skills, buildskilldict
skilldict = buildskilldict(skills)
from rake import buildStopwordRegExPattern
stopwordpattern = buildStopwordRegExPattern("stoplist.txt")

# Rapid Automatic Keyword Extraction (RAKE)
from rake import splitSentences, generateCandidateKeywords
from rake import calculateWordScores, operator
def rake(text, skillfilter=None):
    # preprocess text
    text = textprocess.preprocess(text)    
    
    # tokenize
    sentenceList = splitSentences(text)
    phraseList = generateCandidateKeywords(sentenceList, stopwordpattern)
    
    # generate candidates and calculate scores
    wordscores = calculateWordScores(phraseList)
    keywordcandidates = generateCandidateKeywordScores(phraseList, wordscores)    
    scored_ngrams = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    # pre/post-filter
    if skillfilter != None:
        scored_ngrams = [(ngram, score) for (ngram, score) in scored_ngrams if ngram in skilldict]
    
    # format
    return [{'keyword':pair[0], 'weight':pair[1]} for pair in scored_ngrams]

from rake import separatewords
def generateCandidateKeywordScores(phraseList, wordscore):
    keywordcandidates = {}
    for phrase in phraseList:
        keywordcandidates.setdefault(phrase, 0)
        wordlist = separatewords(phrase, 0) 
        candidatescore = 0
        for word in wordlist:
            candidatescore += wordscore.setdefault(word, 0)
        keywordcandidates[phrase] = candidatescore
    return keywordcandidates


# Crackr
import postagger as pt
from candygen import  words, clusters
def crackr(text, skillfilter=None):
    # skillfilter can be one of
    # - None: don't filter
    # - "pre": filter a priori
    # - "post": filter a posteriori

    # preprocess text
    text = textprocess.preprocess(text).lower()
    
    # tokenize
    sentenceList = splitSentences(text)
    phraseList = generateCandidateKeywords(sentenceList, stopwordpattern)
    wordscores = calculateWordScores(phraseList)
    
    # generate ngrams    
    tokens = text.split()
    
    # pre-filter
    if skillfilter == 'pre':
        tokens = [token for token in tokens if token in skilldict]        
    ngrams = [ngram for n in range(3) for ngram in generate_ngrams(tokens, n + 1)]    
    
    # filter clusters
    viableclusters = []
    for ngram in ngrams:
        try:
            viableclusters += [words[ngram] [1]]
        except:
            pass
            
    # filter words by clusters
    viablewords = []
    for cluster in set(viableclusters):
        for (word, _) in clusters[cluster]:
            viablewords += [word]
    viablewords = set(viablewords)
    
    # pos tag
    pos_tagged = pt.tag(text)
    
    # filter single words
    index = 0
    finallst = []        
    indices = []
    thirdlst = []
    for tup in pos_tagged:
        word, tag = tup
        if tag == 'CC':
            print word
            print pos_tagged[index - 1] [1] [0], pos_tagged[index - 1] [1] [0] 
        if tag[0] == 'N' or tag[0] == 'J' or (tag == 'CC' and pos_tagged[index - 1] [1] [0] == 'N'):
            if word.lower() in viablewords:
                finallst += [(word)]
                indices += [index]
                thirdlst += [(word, index)]
        index += 1

    # generate keyword phrases
    ngrams = stich(finallst, indices)
    ngrams = [" ".join(ngram) for ngram in ngrams]
    keywordcandidates = generateCandidateKeywordScores(phraseList, wordscores)  
    scored_ngrams = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    # post-filter
    if skillfilter == 'post':
        scored_ngrams = [(ngram, score) for (ngram, score) in scored_ngrams if ngram in skilldict]
    
    # format
    return [{'keyword':pair[0], 'weight':pair[1]} for pair in scored_ngrams]
    
def stich (words, indices):
    # corrected and modified version of stich provided with crackr
    # Stiches proximate words together to form longer keywords
    output = []
    prev = -1
    buff = []
    for i in range(len(indices)):
        index = indices[i]
        if index == prev + 1:
            buff += [words[i]]
        else:
            if buff != []:
                output += [buff]
            buff = []
            buff += [words[i]]
        prev = index
    if buff != []:
        output.append(buff)
    return output


# Naive Keyword Extraction
import textprocess
def naive(text, skillfilter=None, jointfilter=True):
    # preprocess
    text = textprocess.preprocess(text)
    
    # generate word scores
    wordscores = calculateWordScores(text)
    
    # tokenize    
    tokens = text.split()
    
    # prefilter    
    if skillfilter == 'pre':
        tokens = [token for token in tokens if token in skilldict]        
    phraseList = [ngram for n in range(3) for ngram in generate_ngrams(tokens, n + 1)]
    keywordcandidates = generateCandidateKeywordScores(phraseList, wordscores)  
    scored_ngrams = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    # post-filter
    if skillfilter == 'post':
        scored_ngrams = [(ngram, score) for (ngram, score) in scored_ngrams if ngram in skilldict]
    
    # format
    return [{'keyword':pair[0], 'weight':pair[1]} for pair in scored_ngrams] 

def generate_ngrams(tokens, n):
    # generates ngrams
    return [' '.join(tokens[index:index + n]) for index in range(len(tokens) - n)]


# Main loop
if __name__ == "__main__":
    app.run()
