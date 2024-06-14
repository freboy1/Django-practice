from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import Choice, Question
# Create your views here.

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join(question.question_text for question in latest_questions)
    context = {'latest_questions': latest_questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(id=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'error_message': 'Fuck you', 'question': question})
    else:
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=[question_id,]))
    