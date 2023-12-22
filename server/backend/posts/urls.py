from django.urls import path
from .views import PostView, PostIDView

urlpatterns = [
    path("posts/", PostView.as_view(), name="get-posts"),
    path("post/<int:id>/", PostIDView.as_view(), name="get-post"),
]
