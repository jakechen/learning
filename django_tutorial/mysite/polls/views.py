from django.http import HttpResponse

# Create your views here.

"""
# Simple placeholder index page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
"""
"""
# Index page that displays the latest 5 questions
from .models import Question
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = '<p>Here are the latest 5 questions:</p>'
    output += ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
"""
"""
from django.template import loader
# Index page that displays the latest 5 questions
from .models import Question
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))
"""
    
# Index page with render() shortcut
from django.shortcuts import render
from .models import Question
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Detail page with 404 using get_object_or_404() shortcut
from django.shortcuts import get_object_or_404
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)