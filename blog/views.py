from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post

class PostList(ListView):
    model = Post

class PostDetail(DetailView):
    model = Post