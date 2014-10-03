Keyword Extractor
=================

Running the Service
-------------------
cd src/
python main.py

This starts the service in web.py at endpoint http://localhost:8080/keywords . The service expects POST requests with the input text in the HTTP body.


Generating a Casing Model
-------------------------
cd src/
cat information_technology_linkedin_jobs.csv | python casings/casingcount_from_linkedin.py > casingcounts-output
python casings/generate_casings.py casingcounts-output > ../data/keywords/casings.txt


Generating IDF Information
--------------------------
cd src/
cat information_technology_linkedin_jobs.csv | python idf/generate_ngram_idf_from_linkedin.py > ../data/keywords/idf.txt


Implicit User Feedback
----------------------
Collect these signals from frontend:
- User removes presented keyword (removed)
- User leaves presented/adds keywords (added)
Add all keywords removed more than 5x and not contained in data/keywords/positives.txt to data/keywords/negatives.txt. Remove all added keywords from data/keywords/negatives.txt and add to data/keywords/positives.txt.


Input Data Refresh
------------------
Collect job descriptions to refresh
- Casing models: casings/generate_casings.py (see above)
- IDF scores: idf/generate_ngram_idf_from_linkedin.py (see above)

Stopwords would normally be refreshed from either
- 1-gram histogram: stopwords/wordcount_from_linkedin.py
- or IDF score: idf/generate_ngram_idf_from_linkedin.py
by setting a threshold and removing all words occurring in data/keywords/positives.txt


Packages
--------
- keywords: Keyword extractor code
- util: Utilities
- casings: Casing model handling
- stopwords: Stopword list handling
- idf: IDF information
- experiments: Experiments
- prototype: Original prototype for comparison


Experiments: Generate All Keywords from LinkedIn data 
-----------------------------------------------------
cat information_technology_linkedin_jobs.csv | python experiments/generate_keywords_from_linkedin.py > all_keywords

