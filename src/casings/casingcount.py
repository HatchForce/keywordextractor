#!python

# Mapper script for CSV formatted LinkedIn job descriptions. Produces casings 
# histogram
# Run as 
# cat information_technology_linkedin_jobs.csv | python casings/casingcount.py > casingcounts-output
     
import sys
import csv
import re

def main(argv):
    # Mapper
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:    
        if len(row) < 7 :
            continue
        description = row[6]
        try:
            for word in separatewords(description, 0):
                print  "LongValueSum:" + word + "\t" + "1"
        except "end of file":
            return
        
def separatewords(text, minWordReturnSize):
    # Tokenizer used by service
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for singleWord in splitter.split(text):
        currWord = singleWord.strip()
        # leave numbers in phrase, but don't count as words, since they tend to invlate scores of their phrases
        if len(currWord) > minWordReturnSize and currWord != '' and not isnum(currWord): 
            words.append(currWord)
    return words

def isnum (s):
    # Tests if token is a number
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
