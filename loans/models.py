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
