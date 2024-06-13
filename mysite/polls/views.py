from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Question
# Create your views here.

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join(question.question_text for question in latest_questions)
    context = {'latest_questions': latest_questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except:
        raise Http404("Question does not exist")
    render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You'te voting on %s." % question_id)