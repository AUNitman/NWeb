from django.urls import path
from .views import CommentView

urlpatterns = [
    path("comments/<int:post_id>/", CommentView.as_view(), name="comments"),
]
