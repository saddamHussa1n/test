import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView

from catalog.forms import RenewBookForm
from catalog.models import *


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status='a').count()
        num_authors = Author.objects.all().count()
        num_visits = request.session.get('num_visits', 1)
        request.session['num_visits'] = num_visits + 1
        context.update({
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_visits': num_visits
        })

        return render(request, self.template_name, context)


class BookListView(ListView):
    model = Book
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='o').order_by('due_back')


class RenewBookView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/book_renew_librarian.html'

    def get_context_data(self, **kwargs):
        context = super(RenewBookView, self).get_context_data(**kwargs)
        context['bookinst'] = get_object_or_404(BookInstance, pk=kwargs.get('pk'))
        context['form'] = RenewBookForm(initial={'renewal_date': date.today() + datetime.timedelta(weeks=3)})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RenewBookForm(self.request.POST or None)
        book_inst = context['bookinst']

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return redirect('my-borrowed')

        context['form'] = form
        return render(request, self.template_name, context)
