from django.urls import URLPattern, path, include
from . import views
URLPattern = [
    path('',views.simple_crawl),
    path('POST_crawl/',views.POST_crawl),
]