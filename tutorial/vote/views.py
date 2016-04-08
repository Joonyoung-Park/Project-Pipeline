from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Choice, Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'detail.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):

    choice_id = request.POST['choice']

    ch = get_object_or_404(Choice, pk=choice_id)

    ch.votes +=1
    ch.save()

    return HttpResponseRedirect(reverse('vote:results', args=(question_id,)))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list , "aaa": "HELLO!!!"}

    return render(request, 'index.html', context)