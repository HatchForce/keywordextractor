import web

urls = ()
app = web.application(urls, globals())

import keywords.service
keywords.service.add(app)
    
if __name__ == "__main__":
    app.run()