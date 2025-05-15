import re
from rest_framework.serializers import ModelSerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from blog.models import UserProfile, Article, Comment, ArticleLike, CommentLike


# Custom Field Serializers #
def req_src_validator(request, method):
    if (request
        and hasattr(request, 'accepted_renderer')
            and request.accepted_renderer.format == method):
        return True
    return False
class TagFieldSerializer(TagListSerializerField):
    def to_internal_value(self, value):
        request = self.context.get('request')

        is_api = req_src_validator(request, 'api')
        if (
                is_api
                and isinstance(value, list)
                and len(value) == 1
                and isinstance(value[0], str)):
            value = re.split(r'[, .\s]+', value[0])
        
        is_html = req_src_validator(request, 'html')
        if is_html: 
            print("html request source")

        return super().to_internal_value(value)

# Model Serializers # 
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ArticleSerializer(TaggitSerializer, ModelSerializer):
    tags = TagFieldSerializer(style={'base_template': 'textarea.html'})

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