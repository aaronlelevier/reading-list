from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from books.models import Author, Book, Note

class BookForm(forms.ModelForm):
	description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
	class Meta:
		model = Book

class BookAdmin(admin.ModelAdmin):
    form = BookForm
    filter_horizontal = ('authors',)

class NoteForm(forms.ModelForm):
	note =  forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
	class Meta:
		model = Note

class NoteAdmin(admin.ModelAdmin):
	form = NoteForm


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Note, NoteAdmin)