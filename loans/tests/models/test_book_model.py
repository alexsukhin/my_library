from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

import datetime

from loans.models import Book

class BookTestCase(TestCase):
    def setUp(self):
        authors = "Doe, J."
        title = "A title"
        publication_date = datetime.datetime(2024, 9, 1)
        isbn = "1234567890123"
        self.book = Book(authors=authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_valid_book_is_valid(self):
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("Default test book should be deemed valid.")


    def test_book_with_blank_author_is_invalid(self):
        self.book.authors = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_author_is_invalid(self):
        self.book.authors = 'x' * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_too_short_author_is_invalid(self):
        self.book.authors = "abc"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_title_is_invalid(self):
        self.book.title = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_title_is_invalid(self):
        self.book.authors = 'x' * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_publication_date_is_invalid(self):
        self.book.publication_date = None
        with self.assertRaises(ValidationError):
            self.book.full_clean()
    
    def test_book_with_non_date_publication_date_is_invalid(self):
        self.book.publication_date = 'this is not a date'
        with self.assertRaises(ValidationError):
            self.book.full_clean()
    
    def test_book_with_blank_isbn_is_invalid(self):
        self.book.isbn = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_isbn_is_invalid(self):
        self.book.isbn = 'x' * 14
        with self.assertRaises(ValidationError):
            self.book.full_clean()
    
    def test_book_isbn_must_be_unique(self):
        self.book.save()
        authors = "Pickles, P."
        title = "Another title"
        publication_date = datetime.datetime(2023, 8, 2)
        isbn = "1234567890123"
        with self.assertRaises(IntegrityError):
            Book.objects.create(authors=authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_book_str_method_returns_expected_string(self):
        expected_str = 'Doe, J.  (2024)  "A title"  ISBN 1234567890123.'
        self.assertEqual(str(self.book), expected_str)

class BookISBNTestCase(TestCase):
    def setUp(self):
        authors = "Doe, J."
        title = "A title"
        publication_date = datetime.datetime(2024, 9, 1)
        isbn = "1234567890123"
        self.book = Book(authors=authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_isbn_13_digits_valid(self):
        self.book.isbn = "1234567890123"
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("13-digit ISBN should be valid.")

    def test_isbn_10_digits_valid(self):
        self.book.isbn = "1234567890"
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("10-digit ISBN should be valid.")

    def test_isbn_too_long_14_digits_invalid(self):
        self.book.isbn = "12345678901234"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_9_digits_invalid(self):
        self.book.isbn = "123456789"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_11_digits_invalid(self):
        self.book.isbn = "12345678901"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_12_digits_invalid(self):
        self.book.isbn = "123456789012"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_10_chars_with_non_digit_invalid(self):
        self.book.isbn = "12345b7890"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_isbn_13_chars_with_non_digit_invalid(self):
        self.book.isbn = "12345b7890123"
        with self.assertRaises(ValidationError):
            self.book.full_clean()