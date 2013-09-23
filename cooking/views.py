from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.models import User 
from django.views.generic.detail import DetailView

#5 - Imported for making templates separate
from django.template.loader import get_template
from django.shortcuts import render
from books.models import Publisher, Book, Author

import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)

def current_datetime_using_template(request):
	now = datetime.datetime.now()
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)

def current_datetime_using_template_2(request):
	now = datetime.datetime.now()
	return render(request, 'current_datetime.html', {'current_date': now})

def grilled_cheese(request):
	return render(request, 'grilled-cheese.html')

def salmon_sandwitch(request):
	return render(request, 'fish-sandwitch_using-base.html')

def base_book(request):
	theBook = Book.objects.get(title__contains="Two")
	myAuthors = theBook.authors.all()
	myImage = theBook.image
	return render(request, 'base_book.html', {'book': theBook, 'author': myAuthors, 'myImage': myImage})

def two_scoops_django(request):
	theBook = Book.objects.get(title__contains="Winning")
	myAuthors = theBook.authors.all()
	myImage = theBook.image
	return render(request, 'two_scoops_django.html', {'book': theBook, 'author': myAuthors, 'myImage': myImage})

def generic_book(request):
	theBook = Book.objects.get(title__contains="Winning")
	myAuthors = theBook.authors.all()
	myImage = theBook.image
	return render(request, 'generic_book.html', {'book': theBook, 'author': myAuthors, 'myImage': myImage})


def generic_book3(request, bookName):
		return render(request, bookName)

class SingleBookView(DetailView):
	model  = Book

    def get_context_data(self, **kwargs):
        context = super(SingleBookView, self).get_context_data(**kwargs)
        return context

singlebook = SingleBookView.as_view()




def title_page(request):
	theBook = Book.objects.all()
	myAuthors = theBook.authors.all()
	myImage = theBook.image
	return render(request, 'generic_book.html', {'book': theBook, 'author': myAuthors, 'myImage': myImage})




def single_book2(request, pk):
    book = Book.objects.get(pk=pk)
    myAuthors = theBook.authors.all()
    ctx = {'book': book, 'author': myAuthors}
    return render_to_response('generic_book.html', RequestContext(request, ctx))


