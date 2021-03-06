
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from books.views import get_hello, get_uuids_a, get_uuids_b, get_argument_from_path, get_arguments_from_query, \
    check_http_query_type, get_headers, raise_error_for_fun

urlpatterns = [

    path('', get_hello),
    path('books/', include('books.urls')),
    path('uuids-a', get_uuids_a),
    path('uuids-b', get_uuids_b),
    path('path-args/<int:x>/<str:y>/<slug:z>', get_argument_from_path, name='get_from_path'),
    path('query-args', get_arguments_from_query, name='get_from_query'),
    path('query-type', check_http_query_type, name='check_query_type'),
    path('get-headers', get_headers, name='get_headers'),
    path('raise-error', raise_error_for_fun, name='raise_error'),
     ]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
