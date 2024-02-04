from django import forms
from . models import Book, Review

class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        exclude = ['category']


class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ['name', 'email', 'comment', 'rating']