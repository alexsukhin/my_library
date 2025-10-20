from django.core.management.base import BaseCommand, CommandError
from loans.models import Book
from faker import Faker
from random import randint

BOOK_COUNT = 100

class Command(BaseCommand):
	help = "Seeds the database with sample data"

	def handle(self, *args, **options):
		fake = Faker()
		for count in range(0, BOOK_COUNT):
			author = f"{fake.last_name()}, {fake.first_name()}"
			title = fake.sentence()
			publication_date = fake.date()
			isbn = fake.unique.isbn13().replace('-','')
			Book.objects.create(authors=author, title=title, publication_date=publication_date, isbn=isbn)
