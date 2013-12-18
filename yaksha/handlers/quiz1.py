from base.form_handler import FormHandler
from datamodel.domain import Domain
from datamodel.problemtemplate import GenerateQuestionForModelProblems
from datamodel.syllabusunit import SyllabusUnit
from modelproblem import ModelProblem
from google.appengine.api import users
from google.appengine.ext.db import Key
from datamodel.usr import User
from google.appengine.ext import db

import logging

class Quiz1(FormHandler):
  html_form = 'html/quiz.json'
  authorize = False
  
  def get(self):
    domainType = self.request.get('domain', default_value='whole')
    questionType = self.request.get('type', default_value='mc')
    highlightAnswer = int(self.request.get('answermode', default_value='1'))
    syllabus = self.request.get('syllabus', default_value='BODMAS rule')
    domain = Domain.defaultDomain(Domain.externalToInternalType(domainType))
    syllabusUnits = SyllabusUnit.all().filter("name = ", syllabus)
    knowledgeUnits = [s.knowledgeUnit for s in syllabusUnits]
    modelProblems = ModelProblem.findModelProblemsMatchingKnowledgeUnits(knowledgeUnits) 
    problems = []
    tags = self.request.get_all("tag")
    numquestions = int(self.request.get('numquestions', default_value=3))
    outputFormat = self.request.get('format', default_value='json')
    self.html_form = 'html/quiz.html' if outputFormat == 'html' else 'html/quiz.json'
    
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
  
