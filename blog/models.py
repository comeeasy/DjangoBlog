import os.path

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/tag/{self.slug}"

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}"


class Post(models.Model):
    title = models.CharField(max_length=30)
    contents = models.TextField()

    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)
    attached_file = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True) # null=True, on_delete=models.SET_NULL are default

    def __str__(self):
        return f"[{self.pk}] {self.title} :: {self.author}"

    def get_absolute_url(self):
        return f"{self.pk}"

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)