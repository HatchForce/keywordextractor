# Module to handle serialized IDF information.

idf = dict()

def loadIDF(path):
    global idf
    for line in open(path,"r"):
        parts = line.strip().split("\t")
        if len(parts)<2:
            continue
        try:
            idf[parts[0]] = float(parts[1])
        except Exception:
            continue

def get(ngram):
    global idf
    return idf.setdefault(ngram,0)