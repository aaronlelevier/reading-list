from django import forms
from django.contrib.auth.models import User

from books.models import Book, Author, Note

class ContactForm(forms.Form):
	name = forms.CharField()
	subject = forms.CharField()							# subject
	message = forms.CharField(widget=forms.Textarea)	# body

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
	new_password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password','email',)
		widgets = {
		    'password': forms.PasswordInput(),
		}

class ProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name','email',)

class ResetPassword(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note 
		fields = ('book', 'title', 'note',)
		widgets = {
			'note': forms.Textarea,
		}

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('title', 'description',)
		widgets = {
			'description': forms.Textarea,
		}	

class AddBookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('title', 'description', 'file')
		widgets = {
			'description': forms.Textarea,
			'file': forms.FileInput,
		}

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ('first_name', 'last_name',)

