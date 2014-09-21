# Python module with service information

import web
import json

# Add service endpoints
def add(app):
    app.add_mapping('/keywords', 'keywords.service.Keywords')

# Endpoint definition
class Keywords:
    def POST(self):
        web.header('Content-Type', 'application/json')
        from keywords.extractor import extract      
        return json.dumps(extract(web.data()))