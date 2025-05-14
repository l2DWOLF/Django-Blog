from rest_framework.serializers import ModelSerializer
from .models import UserProfile, Article, Comment, ArticleLike, CommentLike


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleLikeSerializer(ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = '__all__'

class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'