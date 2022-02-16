"""django_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from crawler.views import hello_view
from crawler.views import homepage
from django.urls import path, include
from django.conf.urls import url 
from crawler import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_view),
    path('home/', homepage),
    path('craw/', homepage),
    path('crawler/',include('crawler.urls'))
    # url(r'^admin/', admin.site.urls),
    # url(r'^hello/', hello_view),
    # url(r'^home/', homepage),
]
