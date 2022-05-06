from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Post, Category, Tag
from .forms import CommentForm

from django.shortcuts import get_object_or_404


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        "title",
        "contents",
        "head_image",
        "attached_file",
        "category",
    ]
    template_name = "blog/post_form_update.html"

    def test_func(self):
        return self.request.user.is_superuser or \
               self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated and request.user == obj.author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError

    def get_success_url(self):
        return reverse("blog-view", kwargs={'pk': self.object.pk})


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = [
        "title",
        "contents",
        "head_image",
        "attached_file",
        "category",
    ]

    def test_func(self):
        return self.request.user.is_superuser or \
               self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and self.test_func():
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect("/blog/")

    def get_success_url(self):
        return reverse("blog-view", kwargs={'pk': self.object.pk})


class PostList(ListView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["count_posts_without_category"] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["category"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        context["comment_form"] = CommentForm

        return context


def categories_page(request, slug):
    if slug == "no-category":  # not categorized posts request
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        "categories": Category.objects.all(),
        "count_posts_without_category": Post.objects.filter(category=None).count(),
        "category": category,
        "post_list": post_list
    }

    return render(
        request,
        "blog/post_list.html",
        context,
    )


def tags_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        "categories": Category.objects.all(),
        "count_posts_without_category": Post.objects.filter(category=None).count(),
        "tag": tag,
        "post_list": post_list
    }

    return render(
        request,
        "/blog/post_list.html",
        context
    )


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        return PermissionDenied
