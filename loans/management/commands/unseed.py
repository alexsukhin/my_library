from django.core.management.base import BaseCommand, CommandError
from loans.models import Book

class Command(BaseCommand):
	help = "Removes seeded data from the database"

	def handle(self, *args, **options):
		Book.objects.all().delete()