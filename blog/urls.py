from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.PostDetail.as_view()),
    path("category/<str:slug>/", views.categories_page),
    path("tags/<str:slug>/", views.tags_page),
    path("", views.PostList.as_view())
]