#!python

# Script to generate keyword histogram. Expects input of the format 
# DESCRIPTION\tKEYWORDS\n where KEYWORDS is JSON encoded.
# Run as
# cat information_technology_linkedin_jobs.csv | python experiments/extract_keywords_from_linked.py > all_keywords
# cat all_keywords | python experiments/aggregate_keywords.py > keywords_histogram

import sys
import json
import operator

keywords = dict()
documents = dict()

doFilter = True

for line in sys.stdin:
    parts = line.strip().split("\t")
    text = parts[-1]
    text = text.replace("'", "\"")
    try:
        for pair in json.loads(text):
            keyword = pair['keyword']
            score = pair['weight']
            keywords.setdefault(keyword, 0)
            keywords[keyword] += float(score)
            documents.setdefault(keyword, 0)
            documents[keyword] += 1
    except ValueError:
        pass
    except IndexError:
        pass
        
for keyword, score in sorted(keywords.iteritems(), key=operator.itemgetter(1), reverse=True):
    if doFilter:
        if documents[keyword] <= 10:
            continue
        if score < 1:
            continue
    print keyword# + "\t" + repr(score) + "\t" + repr(documents[keyword])
