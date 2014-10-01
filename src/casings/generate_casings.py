#!python

# Script to generate the casing model from the cased word counts produced by 
# casings/casingcount.py. Expects input of the format WORD\tCOUNT\n.
# Run as
# cat information_technology_linkedin_jobs.csv | python casings/casingcount_from_linkedin.py > casingcounts-output
# python casings/generate_casings.py casingcounts-output > ../data/keywords/casings.txt

import operator
import sys

# minimum threshold for the occurrence of a word to be added to the model
threshold = 10

casings = {}

def loadCasingCounts(path):
    # Load output of casingcount.py
    global casings
    for line in open(path):
        parts = line.strip().split("\t")
        if len(parts) < 2:
            continue
        casing = parts[0]
        count = int(parts[1])
        casings.setdefault(casing.lower(), {})
        casings[casing.lower()].setdefault(casing,0)
        casings[casing.lower()][casing] += count
        
from keywords.casing import defaultCase
def generate_casings():
    # Choose most likely casing of any word. Exclude
    # default casing of service and lower case as
    # default casing in text corpus.
    global casings
    defaults = []
    for word in casings.keys():
        variants = sorted(casings[word].iteritems(), key=operator.itemgetter(1), reverse=True)
        if len(variants) == 0:
            continue
        main, count = variants[0]
        if count < threshold:
            continue
        if main != defaultCase(main) and main != main.lower():
            defaults += [main]
    return defaults

if __name__=="__main__":
    loadCasingCounts(sys.argv[1])
    print "\n".join(generate_casings())
    