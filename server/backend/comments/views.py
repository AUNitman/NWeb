from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CommentSerializer
from rest_framework.response import Response
from .models import Comment
from users.models import User
from django.conf import settings
import jwt
from datetime import datetime 
from posts.models import Post


class CommentView(APIView):
    def post(self, request, post_id):
        print(request)
        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            exp_timestamp = decoded_token["exp"]
            user_id = decoded_token["user_id"]
            if datetime.now().timestamp() > exp_timestamp:
                return Response(status=401)
        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError,
            KeyError,
        ):
            return Response(status=401)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=404)

        data = {
            "post_id": post_id,
            "content": request.data["content"],
            "user_id": user_id,
        }

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"value": 404}, status=404)
        data = []
        for comment in comments:
            user = User.objects.get(id=comment.user_id)
            comment_data = {
                "id": comment.id,
                "content": comment.content,
                "date": comment.created_at,
                "avatar": user.avatar.url if user.avatar else None,
                "username": user.username,
            }
            data.append(comment_data)

        return Response(data)


# Create your views here.
