Files
- main.py		Application
- clusters.txt	Clusters used by Crackr
- skillset.dat	Skillset data used by Crackr
- stoplist.txt	Stop list used by RAKE
- keywords.wadl	WADL for the webservice
- keywords.html API documentation generated from the WADL with https://github.com/mnot/wadl_stylesheets

clusters.txt and skillset.dat are expected in the working directory.
stoplist.txt copied to avoid path dependencies.

Prerequisites:
- Crackr cloned from https://github.com/anjishnu/Crackr
- both Crackr/webserver and Crackr/webserver/RAKE must be in Python's search path

web.py 0.37
NLTK with Stanford POS tagger bindings (tested with NLTK 3.0)

Run as 
python main.py

Test with
curl -X POST http://localhost:8080/ -d "this is a test"