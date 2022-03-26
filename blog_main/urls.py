"""blog_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUDOKU_WEB_APP = os.path.join(BASE_DIR, "..", 'sudoku')

def sudoku_redirect(request, resource):
    return serve(request, resource, SUDOKU_WEB_APP)

urlpatterns = [
    path("sudoku/", lambda r: sudoku_redirect(r, "index.html")),
    path("sudoku/<path:resource>", sudoku_redirect),
    path('blog/', include("blog.urls")),
    path('admin/', admin.site.urls),
    path("", include("single_pages.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)