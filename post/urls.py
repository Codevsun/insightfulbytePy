from django.urls import path
from post.views import (
    post_detail,
    post_create,
    post_update,
    post_delete,
    post_display,
    all_posts,
    my_posts,
)

urlpatterns = [
    path("<int:post_id>/", post_detail, name="detail-post"),
    path("<int:post_id>/update/", post_update, name="post-update"),
    path("<int:post_id>/delete/", post_delete, name="post-delete"),
    path("display/", post_display, name="post-display"),
    path("all-posts/", all_posts, name="all-posts"),
    path("my-posts/", my_posts, name="my-posts"),
    path("create-post/", post_create, name="create-post"),
]
