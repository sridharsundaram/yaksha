# Main application

import sys

sys.path.insert(0, 'sympy.zip')  # or whatever

import init
import webapp2

#settings._target = None

from google.appengine.ext import db
from base.form_handler import Formdb
from base.form_handler import FormHandler
from handlers.quiz import Quiz
from handlers.configure import Configure
from handlers.template import Template
from handlers.findtemplate import FindTemplate
from handlers.import_spreadsheet import ImportWords
from handlers.preferences import Preferences

class Yaksha(Formdb):
  id_field = 'app_num'
  author = db.UserProperty()

class YakshaAttachment(FormHandler):
  cls = Yaksha

  def get(self):
    self.get_attachment()

def initialize():
  init.initProblems()
  init.initTemplatesInDb(force = False)
  init.initSyllabusInDb()
  
def main():
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


initialize()
application = webapp2.WSGIApplication(
                                       [
                                         ('/', Preferences),
                                         ('/quiz', Quiz),
                                         ('/configure', Configure),
                                         ('/template', Template),
                                         ('/findtemplate', FindTemplate),
                                         ('/importwords', ImportWords),
                                        ],
                                       debug=True)
