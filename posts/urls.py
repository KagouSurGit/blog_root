from .views import all_posts, create_post
from django.urls import path

urlpatterns = [
    path("", all_posts, name="home"),
    path("posts/create/", create_post, name="create_post")
]