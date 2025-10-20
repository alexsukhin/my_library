from django.db import transaction
from django.test import TestCase
from django.urls import reverse

import datetime

from loans.forms import BookForm
from loans.models import Book

INVALID_BOOK_ID = 0

class UpdateBookTestCase(TestCase):
	def setUp(self):
		self.book = Book.objects.create(
			authors="Doe, J.",
			title="A title",
			publication_date=datetime.datetime(2024,9,1),
			isbn="1234567890123",
		)
		self.form_input = {
			'authors': "Doe, J. Jr.",
			'title': "Another title",
			'publication_date': "2025-10-02",
			'isbn': "1234567890124",
		}
		self.url = reverse('update_book', kwargs={'book_id': self.book.id})

	def test_update_book_url(self):
		self.assertEqual(self.url, f'/update_book/{self.book.id}')

	def test_get_update_book(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update_book.html')
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, BookForm))
		self.assertFalse(form.is_bound)

	def test_get_update_book_with_invalid_pk(self):
		invalid_url = reverse('update_book', kwargs={'book_id': INVALID_BOOK_ID})
		response = self.client.get(invalid_url)
		self.assertEqual(response.status_code, 404)

	def test_post_with_valid_data(self):
		book_id = self.book.id
		before_count = Book.objects.count()
		response = self.client.post(self.url, self.form_input, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count)
		expected_redirect_url = reverse('list_books')
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		book = Book.objects.get(pk=book_id)
		self.assertEqual(self.form_input['authors'], book.authors)
		self.assertEqual(self.form_input['title'], book.title)
		expected_publication_date = datetime.datetime.strptime(self.form_input['publication_date'], '%Y-%m-%d').date()
		self.assertEqual(expected_publication_date, book.publication_date)
		self.assertEqual(self.form_input['isbn'], book.isbn)

	def test_post_with_invalid_pk(self):
		invalid_url = reverse('update_book', kwargs={'book_id': INVALID_BOOK_ID})
		before_count = Book.objects.count()
		response = self.client.post(invalid_url, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count)
		self.assertEqual(response.status_code, 404)

	def test_post_with_invalid_form_data(self):
		self.form_input['authors'] = ''
		before_count = Book.objects.count()
		response = self.client.post(self.url, self.form_input, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update_book.html')
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, BookForm))
		self.assertTrue(form.is_bound)

	def test_post_with_non_unique_isbn(self):
		Book.objects.create(
			authors="Pickles, P.", 
			title="My book", 
			publication_date=datetime.datetime(2023,8,2), 
			isbn="1234567890124"
		)
		before_count = Book.objects.count()
		with transaction.atomic():
			response = self.client.post(self.url, self.form_input, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update_book.html')
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, BookForm))
		self.assertTrue(form.is_bound)