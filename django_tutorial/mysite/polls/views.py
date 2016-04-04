from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

"""
# Simple placeholder index page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
"""

# Index page that displays the latest 5 questions
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = 'Here are the latest 5 questions:\n'
    output += ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)