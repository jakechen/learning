from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<html><body>Hello, World!</body></html>')

def about(request):
    return HttpResponse(
        "Here is the About Page. Want to return home? <a href='/'>Back Home</a>"
    )
