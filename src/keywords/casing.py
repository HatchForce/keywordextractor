# Module to apply casing normalization during keywords extraction 

casings = {}

from util.util import loadWordList 
def loadCasings(path):
    # load casing model
    model = loadWordList(path)
    for line in model:
        casings[line.lower()] = line
        
def titleCase(text):
    # title casing
    if text == "":
        return text
    return text[0:1].upper() + text[1:len(text)].lower()

def defaultCase(text):
    return titleCase(text)
        
def normalize(phrase):
    # 1-gram casing normalization
    cased = []
    for word in phrase:
        cased.append(casings.setdefault(word, titleCase(word)))
    return " ".join(cased)