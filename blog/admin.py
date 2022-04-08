from django.contrib import admin
from .models import Post, Category

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    # name field 값으로 slug 자동으로 생성
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)