from django.urls import path
from . import views

urlpatterns = [
    path("update_post/<int:pk>", views.PostUpdate.as_view(), name="update"),
    path("create_post/", views.PostCreate.as_view()),
    path("tags/<str:slug>/", views.tags_page),
    path("category/<str:slug>/", views.categories_page),
    path("<int:pk>/", views.PostDetail.as_view(), name="blog-view"),
    path("<int:pk>/new_comment/", views.new_comment),
    path("", views.PostList.as_view()),
]