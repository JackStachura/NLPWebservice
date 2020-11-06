import cherrypy
import nlpIO

NLP = nlpIO.NLPUnit()

class IntegrationNLPWebservice(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self, param=None, pid=None):
        if param == None:
            data = cherrypy.request.json
            data = NLP.processRequest(data)
            return data
        else:
          free_text = param
          return NLP.processText(free_text, pid)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in() 
    def query(self, text=None):
        if text == None:
            data = cherrypy.request.json
            data = NLP.processQuery(data)
            return data
    
    @cherrypy.expose       
    def home(self):
        return """<html>
          <head>
            
          </head>
          <body>
          <h1>medaCy Free Text Entry</h1>
            <form method="post" action="process">
              <input type="text" value="50" name="param"/>
              <input type="text" value="5" name="pid"/>
              <button type="submit">Submit</button>
            </form>
          </body>
        </html>"""

if __name__ == '__main__':
   config = {'server.socket_host': '0.0.0.0'}
   cherrypy.config.update(config)
   cherrypy.quickstart(IntegrationNLPWebservice())
