#!python
  
# Processor for CSV formatted LinkedIn job descriptions. Produces idf histogram 
# ngrams occurrences in the input corpus.
# Run as 
# cat information_technology_linkedin_jobs.csv | python idf/generate_ngram_idf_from_linkedin.py > ../data/keywords/idf.txt
     
import sys
import csv
import re
import math

# maximum length of ngrams to be generated
maxN = 3

occurrenceThreshold = 10
documentThreshold = 3

def process():
    
    occurrences = dict()
    documents = dict()
    
    # Mapper
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    documentCount = 0
    for row in reader:
        documentCount += 1
        if len(row) < 7 :
            continue
        description = row[6]
        tokens = separatewords(description, 0)
        ngrams = [' '.join(tokens[i:i + n + 1]) for n in range(maxN) for i in range(len(tokens) - n)]
        for ngram in ngrams:
            occurrences.setdefault(ngram, 0)
            occurrences[ngram] += 1
        for ngram in set(ngrams):
            documents.setdefault(ngram, 0)
            documents[ngram] += 1
    
    for ngram in occurrences.keys():
        if occurrences[ngram] < occurrenceThreshold:
            continue        
        if documents.setdefault(ngram, 0) < documentThreshold:
            continue
        idf = math.log((1 + documentCount) / (1 + documents[ngram]))
        print ngram + "\t" + repr(idf)
        
def separatewords(text, minWordReturnSize):
    # Tokenizer used by service
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for singleWord in splitter.split(text):
        currWord = singleWord.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to invlate scores of their phrases
        if len(currWord) > minWordReturnSize and currWord != '' and not isnum(currWord): 
            words.append(currWord)
    return words

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

if __name__ == "__main__":
    process()
