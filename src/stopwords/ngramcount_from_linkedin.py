#!python
  
# Mapper script for CSV formatted LinkedIn job descriptions. Produces frequency 
# histogram of ngrams occurrences in the input corpus.
# Run as 
# cat information_technology_linkedin_jobs.csv | python stopwords/ngramcount_from_linkedin.py > ngramcount-output
     
import sys
import csv
import re

# maximum length of ngrams to be generated
maxN = 3
    
def main(argv):
    # Mapper
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 7 :
            continue
        description = row[6]
        tokens = separatewords(description, 0)
        for n in range(maxN):        
            for i in range(len(tokens) - n):
                print "LongValueSum:" + ' '.join(tokens[i:i + n + 1]) + "\t" + "1"
        
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
    main(sys.argv)
