from django.db import models
from django.contrib.auth.models import User
from django.forms import Textarea
from django.core.validators import MaxLengthValidator


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
    	ordering = ['last_name', 'first_name']        

# Attempt Imagefield
def content_file_name(instance, filename):
    return '/'.join(['content', filename])
    

class Book(models.Model):
    title = models.CharField(max_length=80)
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=2000, blank=True,validators=[MaxLengthValidator(2000)])
    file = models.FileField(upload_to=content_file_name, null=False, verbose_name="Image")
    user = models.ForeignKey(User)
   
    def display_url(self):
        book = self.title.split()
        ans = '-'.join(book)
        return ans

    def __unicode__(self):
        return self.title

    class Meta:
    	ordering = ['title']    


class Note(models.Model):
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=50, verbose_name='Note Title')
    note = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']




