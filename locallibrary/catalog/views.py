from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

def index(request):
  """View function for home page of site."""

  # Generate counts of some of the main objects
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count

  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()


  # The 'all()' is implied by default.
  num_authors = Author.objects.count()

  # Number of visits to this view, as counted in the session variable
  num_visits = request.session.get('num_visits', 0)
  num_visits += 1
  request.session['num_visits'] = num_visits

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits': num_visits,
  }

  # Render the HTML template index.html with the data in the context variable 
  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  context_object_name = 'book_list'
  paginate_by = 10

  ## Get 5 books containing the title war
  # def get_queryset(self):
  #   return Book.objects.filter(title__icontains='war')[:5] 
    
  ## Get 5 books containing the title war:
  # queryset = Book.objects.filter(title__icontains='war')[:5]

  ## Specify your own template name/location
  # template_name = 'books/my_arbitrary_template_name_list.html'  

  # def get_context_data(self, **kwargs):
    ## Call the base implementation first to get the context
    # context = super(BookListView, self).get_context_data(**kwargs)
    
    ## Create any data and add it to the context
    # context['some_data'] = 'This is just some data'
    # return context

class BookDetailView(generic.DetailView):
  model = Book

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10

  def get_queryset(self):
    return (
      BookInstance.objects.filter(borrower=self.request.user)
      .filter(status__exact='o')
      .order_by('due_back')
    )

class LoanedBooksFullList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
  """Generic class-based view listing all books on loan."""
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_all.html'
  paginate_by = 10
  permission_required = 'catalog.can_mark_returned'

  def get_queryset(self):
    return (
      BookInstance.objects.filter(status__exact='o')
      .order_by('due_back')
    )

class AuthorListView(generic.ListView):
  """Generic class-based list view for a list of authors."""
  model = Author
  paginate_by = 10

class AuthorDetailView(generic.DetailView):
  """Generic class-based detail view for an author."""
  model = Author