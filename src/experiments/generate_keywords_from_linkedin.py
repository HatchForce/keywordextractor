#!python

# Script to generate keywords from LinkedIn data. Expects CSV-encoded input.
# Run as
# cat information_technology_linkedin_jobs.csv | python experiments/generate_keywords_from_linkedin.py > all_keywords 

import csv
import sys

# Number of keywords to extract per description
top = 5

from keywords.extractor import extract
def main(argv):
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 7 :
            continue
        description = row[6]
        keywords = extract(description)
        if top <= 0:
            print description + "\t" + repr(keywords)
        else:
            print description + "\t" + repr(keywords[0:top])

if __name__ == "__main__":
    main(sys.argv)

