from . import views
from django.urls import path

urlpatterns = [
    path("", views.all_posts, name="home"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:pk>", views.post_detail, name="post_detail")
]