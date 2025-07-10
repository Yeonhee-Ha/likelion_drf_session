from django.urls import path
from .views import *

app_name = "movie"

urlpatterns = [
    path('',movie_list_create),
    path('<int:movie_id>', movie_detail_update_delete),
    path('<int:movie_id>/comment', comment_read_create),
    path('tags/<str:tags_name>', find_tag),
] 