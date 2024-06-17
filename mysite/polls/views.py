
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question
# Create your views here.
from django.views import generic

# def index(request):
#     latest_questions = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join(question.question_text for question in latest_questions)
#     context = {'latest_questions': latest_questions}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
    