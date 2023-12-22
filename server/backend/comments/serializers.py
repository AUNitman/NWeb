from posts.models import Post
from users.models import User
from .models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Comment
        fields = [
            "content",
            "post_id",
            "user_id",
        ]

    def create(self, validated_data):
        print('vdsa', validated_data)
        post_id = validated_data["post_id"]
        user_id = validated_data["user_id"]
        content = validated_data["content"]
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Invalid post_id")
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user id")
         
        comment = Comment.objects.create(
            content=content,
            post=post,
            user=user,
        )
        return comment
