from django.urls import path

from catalog.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<str:pk>/renew/', RenewBookView.as_view(), name='renew-book-librarian')

]