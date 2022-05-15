from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User

from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest, PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from books.forms import CategoryForm, AuthorForm, BookForm
from books.models import BookAuthor, Category, Book
import logging

logger = logging.getLogger('david')


class AuthorListBaseView(View):
    template_name = 'author_list.html'
    queryset = BookAuthor.objects.all()  # type: ignore

    def get(self, request: WSGIRequest, *args, **kwargs):
        logger.debug(f'{request}DUPA!!!')
        contex = {'authors': self.queryset}
        return render(request, template_name=self.template_name, context=contex)


class CategoryListTemplateView(TemplateView):
    template_name = 'category_list.html'
    extra_context = {'categories': Category.objects.all()}  # type: ignore


class BooksListView(PermissionRequiredMixin, ListView):
    template_name = 'books_list.html'
    model = Book
    paginate_by = 10
    permission_required = 'books.view_book'


class BookDetailsView(PermissionRequiredMixin, DetailView):
    template_name = 'book_detail.html'
    model = Book
    permission_required = 'books.view_book'

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))


class CategoryCreateFormView(FormView):
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list.html')

    def form_valid(self, form):
        result = super().form_valid(form)
        logger.info(f"form = {form}")
        logger.info(f"form.cleaned_data = {form.cleaned_data}")  # cleaned means with removed html indicators
        check_entity = Category.objects.create(**form.cleaned_data) # type: ignore
        logger.info(f"check_entity-id={check_entity.id}")
        return result


class AuthorCreateView(CreateView):
    template_name = "author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("author_list")


class AuthorUpdateView(UpdateView):
    template_name = "author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("author_list")

    def get_object(self, **kwargs):
        return get_object_or_404(BookAuthor, id=self.kwargs.get("pk"))


class BookCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'book_form.html'
    form_class = BookForm
    success_url = reverse_lazy('books_list.html')
    permission_required = 'books.change_book'


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "book_form.html"
    form_class = BookForm
    permission_required = 'books.add_book'
    success_url = reverse_lazy("books_list")

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))


class BookDeleteView(DeleteView):
    template_name = "book_delete.html"
    model = Book
    success_url = reverse_lazy("books_list")

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))


@login_required
def get_hello(request: WSGIRequest) -> HttpResponse:
    user: User = request.user  # type: ignore
    # password = None if user.is_anonymous else user.password
    # date = None if user.is_anonymous else user.date_joined
    # if not user.is_authenticated:
    #     # raise PermissionDenied()
    #     return HttpResponseRedirect(reverse('login'))
    is_auth: bool = user.is_authenticated
    hello = f"Hello {user.username}. That's your password: {user.password}, and date your joined {user.date_joined}."

    return render(request, template_name='hello_world.html', context={'hello_var': hello, "is_authen": is_auth})


def get_uuids_a(request: WSGIRequest) -> HttpResponse:
    uuids = [f'{uuid4()}' for _ in range(10)]
    return HttpResponse(f'uuids={uuids}')


def get_uuids_b(request: WSGIRequest) -> JsonResponse:
    uuids = [f'{uuid4()}' for _ in range(10)]
    return render(request, template_name='uuid.html', context={'elements': uuids})
    # return JsonResponse({'uuids':uuids})


def get_argument_from_path(request: WSGIRequest, x:int, y:str, z:str) -> HttpResponse:

    return HttpResponse(f'x={x}, y={y}, z={z}')


def get_arguments_from_query(request: WSGIRequest) -> HttpResponse:
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    print(type(a))
    return HttpResponse(f'a = {a}, b = {b}, c = {c}')


@csrf_exempt
def check_http_query_type(request: WSGIRequest) -> HttpResponse:
    # query_type = 'Unknown'
    # if request.method == 'GET':
    #     query_type = 'this is GET'
    # elif request.method == 'POST':
    #     query_type = 'this is POST'
    # elif request.method == 'DELETE':
    #     query_type = 'this is DELETE'
    # elif request.method == 'PUT':
    #     query_type = 'this is PUT'
    # return HttpResponse(query_type)
    return render(request, template_name="methods.html", context={})


def get_headers(request: WSGIRequest) -> JsonResponse:
    our_headers = request.headers

    return JsonResponse({'headers': dict(our_headers)})


@csrf_exempt
def raise_error_for_fun(request: WSGIRequest) -> HttpResponse:
    if request.method != 'GET':
        raise BadRequest('method not allowed')
    return HttpResponse('ok')
