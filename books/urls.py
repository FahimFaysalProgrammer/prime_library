from django.urls import path
from . views import AddBookCreateView, EditBookView, DeleteBookView, DetailBookView,  ReturnBookView, BorrowBookView

urlpatterns = [
    path('add/', AddBookCreateView.as_view(), name = 'add_book'),
    path('edit/<int:id>/', EditBookView.as_view(), name = 'edit_book'),
    path('delete/<int:id>/', DeleteBookView.as_view(), name = 'delete_book'),
    path('details/<int:id>/', DetailBookView.as_view(), name = 'detail_book'),
    path('borrow_book/<int:id>/', BorrowBookView.as_view(), name = 'borrow_book'),
    # path("report/", BorrowingHistoryReportView.as_view(), name = "borrowing_history_report"),
    path('return_book/<int:borrow_id>/', ReturnBookView.as_view(), name = 'pay'),
]