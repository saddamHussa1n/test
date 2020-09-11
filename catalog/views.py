from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from catalog.models import *


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status='a').count()
        num_autors = Author.objects.all().count()
        num_visits = request.session.get('num_visits', 1)
        request.session['num_visits'] = num_visits + 1
        context.update({
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_autors,
            'num_visits': num_visits
        })

        return render(request, self.template_name, context)


class BookListView(ListView):
    model = Book
    paginate_by = 1


class BookDetailView(DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='o').order_by('due_back')