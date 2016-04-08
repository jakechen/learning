New Project Checklist
=====================

Project Directory
-----------------
1. Create a project

        $ django-admin startproject mysite

2. Kick off dev server

        $ python manage.py runserver

3. Creating an app

        $ python manage.py startapp polls
        
4. Define app index page  
In _polls/views.py_

        from django.http import HttpResponse
        def index(request):
            return HttpResponse("Hello, world. You're at the polls index.")
        
5. Create the app's url list

        & touch _polls/url.py_

6. Add index to app url list  
In _polls/url.py_

        from django.conf.urls import url
        from . import views
        urlpatterns = [
            url(r'^$', views.index, name='index'), # directs polls/[blank] to index
        ]
        
7. Add app to main url list
in _mysite/url.py_

        from django.conf.urls import include, url
        from django.contrib import admin
        urlpatterns = [
            url(r'^polls/', include('polls.urls')),
            url(r'^admin/', admin.site.urls),
        ]
        

Database Setup
--------------
1. Define engine in _mysite/settings.py_ line 79  
Either 'django.db.backends.sqlite3', 'django.db.backends.postgresql', 'django.db.backends.mysql', or 'django.db.backends.oracle'. Other backends are also available.

2. Define name  in _mysite/settings.py_ line 80

3. Migrate

        $ python manage.py migrate
        

Creating Models
---------------
1. Define model(s) 
Add model classes to _polls/models.py_

        class Question(models.Model):
            question_text = models.CharField(max_length=200)
            pub_date = models.DateTimeField('date published')
            def __str__(self):
                return self.question_text
        class Choice(models.Model):
            question = models.ForeignKey(Question, on_delete=models.CASCADE)
            choice_text = models.CharField(max_length=200)
            votes = models.IntegerField(default=0)
            def __str__(self):
                return self.choice_text
            
2. Add models to main settings (assuming new app)  
Add app to INSTALLED_APPS section in _mysite/settings.py_

        INSTALLED_APPS = [
            'polls.apps.PollsConfig',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ]
        
3. Activate these models i.e. make migrations  

        $ python manage.py makemigrations polls
        
4. Migrate

        $ python manage.py migrate
        

Adding New Views
----------------
1. Define new views  
Add new views to _polls/views.py_  
**Note that these views take arguments**

        def detail(request, question_id):
            return HttpResponse("You're looking at question %s." % question_id)
        def results(request, question_id):
            response = "You're looking at the results of question %s."
            return HttpResponse(response % question_id)
        def vote(request, question_id):
            return HttpResponse("You're voting on question %s." % question_id)
            
2. Add new views to app url  
Wire these new views into the _polls.urls_ module by adding the following url() calls:

        urlpatterns = [
            # ex: /polls/
            url(r'^$', views.index, name='index'),
            # ex: /polls/5/
            url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'), # ?P<question_id> defines variable, [0-9]+ only matches numbers
            # ex: /polls/5/results/
            url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
            # ex: /polls/5/vote/
            url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
        ]


Adding Database Hooks to Views
------------------------------
1. Use Django's database API https://docs.djangoproject.com/en/1.9/topics/db/queries/  
In _polls/views.py_ import the Question model then modify index():

		from .models import Question
		def index(request):
			latest_question_list = Question.objects.order_by('-pub_date')[:5]
			output = ', '.join([q.question_text for q in latest_question_list])
			return HttpResponse(output) # Required
	
		
Customizing Templates
---------------------
1. Define template namespace for the app  
Add the app_name variable to _polls/url.py_:  
**This way it's possible to have app1/abc.html as well as app2/abc.html**

		app_name = 'polls'
		urlpatterns = [
			url(r'^$', views.index, name='index'),
			url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
			url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
			url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
		]

2. Create a templates directory and then within this directory create another directory with the same name as app

		$ mkdir polls/templates
		$ mkdir polls/templates/polls # For reasoning see "Template namespacing" inside https://docs.djangoproject.com/en/1.9/intro/tutorial03/

3. Create .html files inside this directory  
Create a _polls/templates/polls/index.html_ and put this inside there:  
**Use {% url %} template tag to automatically looks up 'detail' url from polls/url.py, so if you change url you don't have to change each template**

		{% if latest_question_list %}
			<ul>
			{% for question in latest_question_list %}
				<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
			{% endfor %}
			</ul>
		{% else %}
			<p>No polls are available.</p>
		{% endif %}

4. Point view to template  
Modify _polls/views.py_ to render using the new template:
			
		# With render() shortcut
		from django.shortcuts import render
		def index(request):
			latest_question_list = Question.objects.order_by('-pub_date')[:5]
			context = {'latest_question_list': latest_question_list}
			return render(request, 'polls/index.html', context)

		# Without render() shortcut (same as above)
		from django.template import loader
		def index(request):
			latest_question_list = Question.objects.order_by('-pub_date')[:5]
			template = loader.get_template('polls/index.html')
			context = {'latest_question_list': latest_question_list}
			return HttpResponse(template.render(context, request))

5. Redirect to 404 (optional)
Modify _polls/views.py_ to catch _Model.DoesNotExist_ exception and redirect to a 404:

		# Long version
		from django.http import Http404
		def detail(request, question_id):
			try:
				question = Question.objects.get(pk=question_id)
			except Question.DoesNotExist:
				raise Http404("Question Does Not Exist")
			return render(request, 'polls/detail.html', {'question':question})
			
		# With get_object_or_404() shortcut
		from django.shortcuts import get_object_or_404, render
		def detail(request, question_id):
			question = get_object_or_404(Question, pk=question_id)
			return render(request, 'polls/detail.html', {'question':question})
		
	
Forms
-----
1. Insert <form> element into a tempate  
Modify _polls/template/polls/detail.html_ to include <form> element:  

		<form action="{% url 'polls:vote' question.id %}" method="post">
		{% csrf_token %}
		{% for choice in question.choice_set.all %}
			<input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
			<label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
		{% endfor %}
		<input type="submit" value="Vote" />
		</form>

2. Add form processing code to the associated view
Modify _vote()_ inside _polls/views.py_ with this:

        def vote(request, question_id):
            question = get_object_or_404(Question, pk=question_id)
            try:
                selected_choice = question.choice_set.get(pk=request.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
            else:
                selected_choice.votes =+ 1
                selected_choice.save()
                return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


Generic Views
-------------
WIP