import datetime

from django.test import TestCase
from django.utils import timezone

from books.models import Book, Note, Author

class BookModelTest(TestCase):
	"""
	test to test my Book Model 
	"""
	def test_publication_date_is_not_in_future(self):
		book = Book(publication_date=timezone.now())
		test = book.publication_date <= timezone.now()
		self.assertEqual(test, True)

