from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import random

from loans.models import Book
from loans.forms import BookForm

SLOGAN_LIST = [
	"Having fun isn't hard when you've got a library card.",
	"Libraries make shhh happen.",
	"Believe in your shelf.",
	"Need a good read? We’ve got you cover to covered.",
	"Check us out. And maybe one of our books too.",
	"Get a better read on the world.",
]

def welcome(request):
	context = {'slogan': random.choice(SLOGAN_LIST)}
	return render(request, 'welcome.html', context)

def list_books(request):
	context = {'books': Book.objects.all()}
	return render(request, 'books.html', context)

def get_book(request, book_id):
	try:
		context = {'book': Book.objects.get(id=book_id)}
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 
	else:
		return render(request, 'book.html', context)

def create_book(request):
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			try:
				form.save()
			except:
				form.add_error(None, "It was not possible to save this book to the database.")
			else:
				path = reverse('list_books')
				return HttpResponseRedirect(path)
	else:
		form = BookForm()
	return render(request, 'create_book.html', {'form': form})

def update_book(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 

	if request.method == "POST":
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			try:
				form.save()
			except:
				form.add_error(None, "It was not possible to save this book to the database.  Check the ISBN number.")
			else:
				path = reverse('list_books')
				return HttpResponseRedirect(path)
	else:
		form = BookForm(instance=book)
	return render(request, 'update_book.html', {'book_id': book_id, 'form': form})

def delete_book(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 

	if request.method == "POST":
		book.delete()
		path = reverse('list_books')
		return HttpResponseRedirect(path)
	else:
		return render(request, 'delete_book.html', {'book': book})
