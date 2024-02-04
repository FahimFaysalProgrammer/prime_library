from django.db import models
from django.utils import timezone
from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from . constants import RATINGS
from transactions.models import Transaction
from authors.models import Author

# Create your models here.
class Book(models.Model):
    book_title = models.CharField(max_length = 250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    description = models.TextField(blank=True, null=True, default='')
    image = models.ImageField(upload_to = 'books/media/uploads/', blank = True, null = True)
    book_borrowing_price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ManyToManyField(Category)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    quantity = models.IntegerField(default = 0)

    def __str__(self):
        return f"Book Title: {self.book_title}, Author: {self.author}"



class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    book_borrow_date = models.DateTimeField(auto_now_add = True)
    deposit = models.ForeignKey(Transaction, on_delete = models.SET_NULL, null = True)
    borrow_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Borrowed {self.book.book_title} on {self.book_borrow_date}"

class Return(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Borrow, on_delete = models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)
    amount_received = models.DecimalField(max_digits = 10, decimal_places = 2)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = 'reviews')
    name = models.CharField(max_length=30)
    email = models.EmailField(blank = True, null = True, verbose_name = 'Contact Email (Optional)')
    comment = models.TextField()
    rating = models.IntegerField(choices=RATINGS)
    review_date = models.DateTimeField(default=timezone.now)
    review_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review_date}"