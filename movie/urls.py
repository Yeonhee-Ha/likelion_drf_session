from django.urls import path, include
from rest_framework import routers

from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "movie"

default_router = routers.SimpleRouter(trailing_slash = False)
default_router.register("movie", MovieViewSet, basename="movies")

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet,basename="comments")

movie_comment_router = routers.SimpleRouter(trailing_slash=False)
movie_comment_router.register("comments", MovieCommentViewSet, basename="comments")

tag_router = routers.SimpleRouter(trailing_slash=False)
tag_router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
    path("movie/<int:movie_id>/", include(movie_comment_router.urls)),
    path("", include(tag_router.urls)),
]