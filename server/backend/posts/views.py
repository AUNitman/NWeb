from django.contrib import admin
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "theme", "created_at")
    search_fields = ("title", "theme")
   

admin.site.register(Post, PostAdmin)


class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        data = []
        for post in posts:
            obj = {
                "title": post.title,
                "image": "http://localhost:8000" + post.image.url
                if post.image
                else None,
                "theme": post.theme,
                "id": post.id,
            }
            data.append(obj)
        return Response({"posts": data})


class PostIDView(APIView):
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({"value": 404}, status=404)

        return Response(
            {
                "title": post.title,
                "content": post.content,
                "image": "http://localhost:8000" + post.image.url
                if post.image
                else None,
                "theme": post.theme,
                "created_at": post.created_at,
            }
        )
