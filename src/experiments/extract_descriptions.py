#!python

# Script to extract descriptions from LinkedIn data. Expects CSV encoded input.
# Run as 
# cat information_technology_linkedin_jobs.csv | python experiments/extract_descriptions.py > descriptions

import csv
import sys

top = 5

def main(argv):
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 7 :
            continue
        print row[6]

if __name__ == "__main__":
    main(sys.argv)
