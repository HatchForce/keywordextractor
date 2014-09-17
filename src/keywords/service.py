import web
import json

def add(app):
    app.add_mapping('/keywords', 'keywords.service.Keywords')

class Keywords:
    def POST(self):
        web.header('Content-Type', 'application/json')
        from keywords.extractor import extract      
        return json.dumps(extract(web.data()))