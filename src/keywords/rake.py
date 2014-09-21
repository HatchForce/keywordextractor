# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010). 
# Automatic keyword extraction from indi-vidual documents. 
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

debug = False
test = True

import operator

def calculateWordScores(phrases):
    # Calculates RAKE word scores
    wordfreq = {}
    worddegree = {}
    for phrase in phrases:
        wordlistlength = len(phrase)
        wordlistdegree = wordlistlength - 1
        # if wordlistdegree > 3: wordlistdegree = 3 #exp.
        for word in phrase:
            wordfreq.setdefault(word, 0)
            wordfreq[word] += 1
            worddegree.setdefault(word, 0)
            worddegree[word] += wordlistdegree  # orig.
            # worddegree[word] += 1/(wordlistlength*1.0) #exp.
    for item in wordfreq:
        worddegree[item] = worddegree[item] + wordfreq[item]     

    # Calculate Word scores = deg(w)/frew(w)
    wordscore = {}
    for item in wordfreq:
        wordscore.setdefault(item, 0)
        wordscore[item] = worddegree[item] / (wordfreq[item] * 1.0)  # orig.
        # wordscore[item] = wordfreq[item]/(worddegree[item] * 1.0) #exp.
    return wordscore
    
def generateCandidateKeywordScores(phraseList, wordscore):
    # Aggregates word scores over phrases
    keywordcandidates = {}
    for phrase in phraseList:        
        candidatescore = 0
        for word in phrase:
            candidatescore += wordscore.setdefault(word, 0)
        keywordcandidates[' '.join(phrase)] = candidatescore
    return keywordcandidates
