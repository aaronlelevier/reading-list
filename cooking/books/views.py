import datetime
import re
import random

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Template, Context, RequestContext, loader
from django.contrib import auth 
from django.contrib.auth.models import User 
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404

from books.models import Book, Author, Note
from forms import ContactForm, LoginForm, UserForm, ProfileForm, ResetPassword, NoteForm, BookForm, AuthorForm, AddBookForm, ChangePasswordForm

def index(request):
	latest_book_list = Book.objects.order_by('-publication_date')[:8]
	context = {'latest_book_list': latest_book_list}
	return render(request, 'books/index.html', context)


def detail(request, book_requested):
	orig_book = uncode_display_url(book_requested)
	book = get_object_or_404(Book, title=orig_book)
	authors = book.authors.all()
	notes = Note.objects.filter(book__title=orig_book)
	return render(request, 'books/detail.html', {'book': book, 'authors': authors, 'notes': notes, 'tab_title': book.title})


def book_list(request):
	books = Book.objects.all()
	return render(request, 'books/book_list.html', {'books': books, 'tab_title': 'Book List'})

# views / functions for contact email form
def bodyString(name, message):
	return 'Name: ' + name + '\n' + 'Message: ' + message

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			email = EmailMessage(
				subject = cd['subject'],
				body = bodyString(cd['name'], cd['message']),
				from_email = 'aaron.lelevier@gmail.com',
				to = ['pyaaron@gmail.com'],
			)
			email.send(fail_silently=False)
			return HttpResponseRedirect(reverse('books:thanks'))
	else:
		form = ContactForm()
	return render(request, 'books/contact.html', {'form': form, 'tab_title': 'Contact Us'})

def thanks(request):
	return render(request, 'books/thanks.html')

# views for Login / Logout
def profile(request):
	user = request.user
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user.first_name, user.last_name, user.email = cd['first_name'], cd['last_name'], cd['email']
			user.save()
			return HttpResponseRedirect(reverse('books:updated'))
	else:
		form = ProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
		books = Book.objects.filter(user=user.id) 
		notes = Note.objects.filter(user=user.id)
	return render(request, 'books/profile.html', {'user': user, 'form': form, 'tab_title': 'Reading List | Profile', 'books': books, 'notes':notes})
# ---------------------------------------------------------------------------------------------------------------------------------

def edit_a_book(request, book_requested):
	if request.method == 'POST':
		formA = BookForm(request.POST, prefix='formA')
		formA.is_multipart()
		formB = AuthorForm(request.POST, prefix='formB')
		# Book Title Regex used before saving to DB --------------------------
		if formA.is_valid():
			title = formA.cleaned_data['title']
			m = re.match('(\w+\s)*(\w+)', title)
			# continue normal view as before -------------------------------------
			if all([formA.is_valid(), formB.is_valid()]) and m is not None and len(str(m.group())) == len(str(title)):
				orig_book = uncode_display_url(book_requested)
				book = get_object_or_404(Book, title=orig_book)
				author = Author.objects.get(book__title=orig_book)
				book.title = formA.cleaned_data['title']
				author.first_name = formB.cleaned_data['first_name']
				author.last_name = formB.cleaned_data['last_name']
				book.description = formA.cleaned_data['description']
				author.save()
				book.save()
				return HttpResponseRedirect(reverse('books:profile'))
	else:
		orig_book = uncode_display_url(book_requested)
		book = get_object_or_404(Book, title=orig_book)
		author = Author.objects.get(book__title=orig_book)
		formA = BookForm(prefix='formA', initial={'title': book.title, 'description': book.description})
		formB = AuthorForm(prefix='formB', initial={'first_name': author.first_name, 'last_name': author.last_name})
	return render(request, 'books/edit_a_book.html', {'formA': formA, 'formB': formB})


# ---------------------------------------------------------------------------------------------------------------------------------
def updated(request):
	title = 'Profile updated'
	return render(request, 'books/logged.html', {'title': title})

def book_updated(request):
	title = 'This book has been updated'
	return render(request, 'books/logged.html', {'title': title})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('books:loggedout'))

def loggedout(request):
	return render(request, 'books/loggedout.html')

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			password = cd['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect(reverse('books:loggedin'))
			else:
				no_match = 'Please check username and password'
				return render(request, 'books/login.html', {'form': form, 'no_match': no_match})
	else:
		form = LoginForm()
	return render(request, 'books/login.html', {'form': form})

def loggedin(request):
	title = 'Welcome, you are logged in'
	return render(request, 'books/logged.html', {'title': title})

def loginfail(request):
	title = 'Log in Fail'
	return render(request, 'books/logged.html', {'title': title})

def createUser(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			password = cd['password']
			user = User.objects.create_user(**form.cleaned_data)
			if user is not None:
				user = auth.authenticate(username=username, password=password)
				auth.login(request, user)
				return HttpResponseRedirect(reverse('books:loggedin'))
	else:
		form = UserForm()
	return render(request, 'books/createUser.html', {'form': form, 'tab_title': 'Create an Account'})

def reset_password(request):
	if request.method == 'POST':
		form = ResetPassword(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			myNewPassword = newPassword()
			username = cd['username']
			try:
				user = User.objects.get(username=username)
				if user.email == cd['email']:
					user.set_password(myNewPassword)
					user.save()
					email = EmailMessage(
						subject = 'Reading List - Temporary Password Request',
						body = 'Hello ' + str(cd['username']) + ',' + '\n\n' + 
							'Please log in with this temporary password: ' + str(myNewPassword) + '\n\n' +
							'Your password can be reset on your profile page.',

						from_email = 'pyaaron@gmail.com',
						to = [cd['email']],
					)
					email.send(fail_silently=False)
					return HttpResponseRedirect(reverse('books:email_sent'))
				else:
					no_match = 'Username and Email does not match'
					return render(request, 'books/reset_password.html', {'form': form, 'no_user': no_match})
			except User.DoesNotExist:
				no_user = 'Username Invalid'
				return render(request, 'books/reset_password.html', {'form': form, 'no_user': no_user})
	else:
		form = ResetPassword()
	return render(request, 'books/reset_password.html', {'form': form})

def email_sent(request):
	title = 'Email Sent'
	return render(request, 'books/logged.html', {'title': title})

def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		user = request.user
		if form.is_valid():
			cd = form.cleaned_data
			if cd['new_password'] == cd['confirm_password']:
				user.set_password(str(cd['new_password']))
				user.save()
				return HttpResponseRedirect(reverse('books:password_updated'))
			else:
				confirm_data = "Passwords do not match"
				return render(request, 'books/change_password.html', {'form': form, 'confirm_data': confirm_data})
	else:
		form = ChangePasswordForm()
	return render(request, 'books/change_password.html', {'form': form})

def password_updated(request):
	title = 'Password Updated'
	return render(request, 'books/logged.html', {'title': title})

# two "take note views ---------------------------------------------------------------------------------------
def take_notes(request):
	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			date = datetime.datetime.now()
			user = request.user
			note = Note(date=date, user=user, **form.cleaned_data)
			note.save()
			return HttpResponseRedirect(reverse('books:index'))
	else:
		form = NoteForm()
	books = Book.objects.all()
	return render(request, 'books/take_notes.html', {'form': form, 'books': books})

def take_specific_notes(request, book_id):
	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			date = datetime.datetime.now()
			user = request.user
			note = Note(date=date, user=user, **form.cleaned_data)
			note.save()
			return HttpResponseRedirect(reverse('books:index'))
	else:
		form = NoteForm(initial={'book': book_id})
	book = Book.objects.get(pk=book_id)	
	books = Book.objects.all()
	return render(request, 'books/take_notes.html', {'form': form, 'book': book, 'books': books})
# ---------------------------------------------------------------------------------------------------------

def add_a_book(request):
	if request.method == 'POST':
		formA = AddBookForm(request.POST, request.FILES, prefix='formA')
		formA.is_multipart()
		formB = AuthorForm(request.POST, prefix='formB')
		# Book Title Regex used before saving to DB --------------------------
		if formA.is_valid():
			title = formA.cleaned_data['title']
			m = re.match('(\w+\s)*(\w+)', title)
			# continue normal view as before -------------------------------------
			if all([formA.is_valid(), formB.is_valid()]) and m is not None and len(str(m.group())) == len(str(title)):
				title = formA.cleaned_data['title']
				first_name = formB.cleaned_data['first_name']
				last_name = formB.cleaned_data['last_name']
				description = formA.cleaned_data['description']
				date = datetime.datetime.now()
				a_book = formA
				a_author = formB
				new_book = a_book.save(commit=False)
				new_author, created_author = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
				new_book.file.name = content_file_name('content', formA['file'].name)
				new_book.user = request.user
				new_book.save()
				new_book.authors.add(new_author.id)
				new_book.save()
				return HttpResponseRedirect(reverse('books:index'))
	else:
		formA = AddBookForm(prefix='formA')
		formB = AuthorForm(prefix='formB')
	return render(request, 'books/add_a_book.html', {'formA': formA, 'formB': formB})


def mission(request):
	return render(request, 'books/mission.html')

def search_results(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		books = Book.objects.filter(title__icontains=q)
		title = 'Search Results'
		return render(request, 'books/search_results.html', {'title': title, 'books': books})
	else:
		title = 'No Matching Results'
		return render(request, 'books/search_results.html', {'title': title})




# ---------------------------- None View Helper Functions ------------------------------------

# Place to save image upload file
def handle_uploaded_file(f):
    with open(content_file_name(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Attempt Imagefield
def content_file_name(instance, filename):
    return '/'.join([filename])

def newPassword():
	a = random.randrange(97,122)
	b = random.randrange(5,122,7)
	c = random.randrange(97,122)
	d = random.randrange(7,122,6)
	e = random.randrange(97,122)
	return str(chr(a)) + str(ord(chr(b))) + str(chr(c)) + str(ord(chr(d))) + str(chr(e)) 


# Helper function to look up Book Obj. using display_url
def uncode_display_url(book_id):
	book = book_id.split('-')
	ans = ' '.join(book)
	return ans 