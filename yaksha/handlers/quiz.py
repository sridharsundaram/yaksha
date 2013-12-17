from base.form_handler import FormHandler
from datamodel.domain import Domain
from datamodel.problemtemplate import GenerateQuestionForModelProblems
from modelproblem import ModelProblem
from google.appengine.api import users
from datamodel.usr import User
from google.appengine.ext import db

import logging

class Quiz(FormHandler):
  html_form = 'html/quiz.html'
  authorize = True
  
  def get(self):
    current_user = users.get_current_user()
    user = User.retrieve(User, current_user.nickname())
#    session = sessions.Session(writer = "cookie")
    domainType = user.domainType
    questionType = user.questionType
    if user.answermode == 'on' or not user.answermode:
      user.answermode = '1'
    highlightAnswer = int(self.request.get('answermode', default_value=user.answermode))
    domain = Domain.defaultDomain(Domain.externalToInternalType(domainType))
    syllabusUnits = db.get(user.syllabusUnitKeys)
    knowledgeUnits = [s.knowledgeUnit for s in syllabusUnits]
    modelProblems = ModelProblem.findModelProblemsMatchingKnowledgeUnits(knowledgeUnits) 
    problems = []
    tags = self.request.get_all("tag")
    numquestions = int(self.request.get('numquestions', default_value=user.numquestions))
    outputFormat = self.request.get('format', default_value='html')
    self.html_form = 'html/quiz.html' if outputFormat == 'html' else 'html/quiz.txt'
    
    # At least one tag must match
    while len(problems) < numquestions:
      problem = GenerateQuestionForModelProblems(modelProblems, domain, tags, questionType, highlightAnswer, outputFormat)
      logging.info("Num problems generated = " + str(len(problems)))
      if problem:
        problems.append(problem)

    self.template_values = {
      'problems' : problems,
    }
    FormHandler.get(self)
  
