# Utiltiies

def isnum (s):
    # Test if token is a number
    try:
        if '.' in s:
            float(s)
        else:
            int(s)
        return True
    except ValueError:
        return False
    
    
def loadWordList(stopWordFile):
    # Word list loader 
    stopWords = []
    for line in open(stopWordFile):
        l = line.strip()
        # empty lines
        if l == "":
            continue
        # comments
        if l[0:1] == "#":
            continue
        # word
        stopWords.append(l)
    return stopWords