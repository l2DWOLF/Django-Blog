from rest_framework.serializers import ModelSerializer
from .models import UserProfile, Post, Comment, PostLike, CommentLike


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'