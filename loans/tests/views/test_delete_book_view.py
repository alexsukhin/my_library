from django.test import TestCase
from django.urls import reverse
from django.http import Http404
import datetime

from loans.models import Book

class DeleteBookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            authors="Doe, J.",
            title="Book to delete",
            publication_date=datetime.date(2024, 9, 1),
            isbn="1234567890123"
        )

        self.url = reverse('delete_book', args = [self.book.id])

    def test_delete_book_url(self):
        self.assertEqual(self.url, f'/delete_book/{self.book.id}')

    def test_delete_book_post_deletes_book(self):
        before_count = Book.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count - 1)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book.id)
        expected_redirect_url = reverse('list_books')
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_delete_book_get_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_book.html')
        self.assertIn('book', response.context)
        self.assertEqual(response.context['book'], self.book)

    def test_delete_nonexistent_book_get_404(self):
        url = reverse('delete_book', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_book_post_404(self):
        url = reverse('delete_book', args=[9999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Book.objects.count(), 1)