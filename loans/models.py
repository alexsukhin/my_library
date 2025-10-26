from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.core.exceptions import ValidationError

def validate_isbn(value):
    if not value.isdigit():
        raise ValidationError("ISBN must contain only digits.")
    if len(value) not in [10, 13]:
        raise ValidationError("ISBN must be exactly 10 or 13 digits long.")

class Book(models.Model):
	authors = models.CharField(
			max_length=255,
			validators=[MinLengthValidator(4)]
		)
	title = models.CharField(max_length=255)
	publication_date = models.DateField()
	isbn = models.CharField(
    	max_length=13,
    	unique=True,
    	validators=[validate_isbn]
    )

	def __str__(self):
		return(f"{self.authors}  ({self.publication_date.year})  \"{self.title}\"  ISBN {self.isbn}.")

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return(f"Member {self.id}: {self.last_name}, {self.first_name} <{self.email}>")

class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    start_at = models.DateField()
    end_at = models.DateField()