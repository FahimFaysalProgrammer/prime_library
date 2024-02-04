from django.utils import timezone
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Book, Review
from transactions.models import Transaction
from transactions.constants import BORROW_BOOK
from . import forms
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . models import Book, Borrow, Return
from datetime import datetime
from django.shortcuts import get_object_or_404
from . models import Borrow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from datetime import datetime
from django.db.models import Sum
from transactions.models import Transaction
from transactions.views import send_customer_email
from django.db import transaction

# Create your views here.
@method_decorator(login_required, name='dispatch')
class AddBookCreateView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class EditBookView(UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')



@method_decorator(login_required, name='dispatch')
class DeleteBookView(DeleteView):
    model = models.Book
    template_name = 'delete.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'



@method_decorator(login_required, name='dispatch')
class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = post
            new_review.user = request.user
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.reviews.all()
        review_form = forms.ReviewForm()

        context['now'] = timezone.localtime(timezone.now())
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context



    
# ///////////////////////////////////////////////////////////////////////



class BorrowBookView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def get(self, request, id):
        book = get_object_or_404(Book, pk=id)
        return render(request, self.template_name, {'book': book})

    @method_decorator(login_required)
    def post(self, request, id):
        book = get_object_or_404(Book, pk=id)
        amount_deposited = float(request.POST.get('amount', 0))

        if amount_deposited < book.book_borrowing_price:
            messages.error(request, "Insufficient funds to borrow the book.")
            return redirect('borrow_book', id=id)

        # Create a deposit record
        deposit = Transaction.objects.create(user=request.user, amount=amount_deposited)

        # Create a borrow record
        borrow = Borrow.objects.create(user=request.user, book=book, deposit=deposit)

        # Update user's account balance
        request.user.deposit.balance = amount_deposited - book.book_borrowing_price
        request.user.deposit.save()
        # Send email to the user
        send_mail(
            'Book Borrowing Confirmation',
            'You have successfully borrowed a book. Thank you for using our service.',
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )

        messages.success(request, "Book borrowed successfully. Check your email for confirmation.")
        return redirect('borrowing_history_report')

























class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, borrow_id):
        borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
        return render(request, 'accounts/profile.html', {'borrow': borrow})

    def post(self, request, borrow_id):
        borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
        amount_received = borrow.book_cost
        
        Return.objects.create(
            user=request.user,
            borrow=borrow,
            amount_received=amount_received
        )
        
        request.user.userprofile.account_balance += amount_received
        request.user.userprofile.save()
        borrow.delete()

        messages.success(request, "Book returned successfully.")
        return redirect('borrowing_history_report')














    








# class BorrowingHistoryReportView(LoginRequiredMixin, ListView):
#     template_name = 'borrow_report.html'
#     model = Borrow
    
#     def get_queryset(self):
#         queryset = Borrow.objects.filter(borrower=self.request.user)  # Change 'user' to 'borrower'
#         start_date_str = self.request.GET.get('start_date')
#         end_date_str = self.request.GET.get('end_date')
        
#         if start_date_str and end_date_str:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#             queryset = queryset.filter(book_borrow_date__date__gte=start_date, book_borrow_date__date__lte=end_date)
            
#         return queryset.distinct()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['account'] = self.request.user.account
#         return context
