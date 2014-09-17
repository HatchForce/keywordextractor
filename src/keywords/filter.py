positive_list = []
negative_list = []

from util.util import loadWordList

def loadPositiveList(path):
    global positive_list
    positive_list = loadWordList(path)
    
def loadNegativeList(path):
    global negative_list
    negative_list = loadWordList(path)

def filter(keywords):
    
    global positive_list
    global negative_list
    
    non_negatives = [keyword for keyword in keywords if ' '.join(keyword) not in negative_list]
    positives = [keyword for keyword in non_negatives if ' '.join(keyword) in positive_list]
    non_positives = [keyword for keyword in keywords if keyword not in positives]
    uniques = [keyword for keyword in non_positives if not isSublistDuplicate(keyword, keywords)]
    
    filtered = []
    filtered.extend(positives)
    filtered.extend(uniques)
    return filtered

def isSublistOf(s, l):
    if len(l) >= len(s):
        for start in range(len(l) - len(s) + 1):
            isSublist = True
            for index in range(len(s)):
                if l[start + index] != s[index]:
                    isSublist = False
                    break
            if isSublist:
                return True
    return False

def isSublistDuplicate(ngram, keywords):
    for keyword in keywords:
        if ngram == keyword:
            continue
        if isSublistOf(ngram, keyword):
            return True
    return False
