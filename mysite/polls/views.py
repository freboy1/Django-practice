from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question
# Create your views here.

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join(question.question_text for question in latest_questions)
    template = loader.get_template('polls/index.html')
    context = {'latest_questions': latest_questions}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You'te voting on %s." % question_id)