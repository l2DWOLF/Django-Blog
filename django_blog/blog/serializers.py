import re
from rest_framework.serializers import ModelSerializer, HiddenField, SerializerMethodField
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.contrib.auth.models import User
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
    
class CurrentUserDefault():
    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context['request']
        return request.user.userprofile

# Model Serializers # 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name',
                    'last_name']
        extra_kwargs = {
            'password': {'write_only': False, 'required': True},
            'id': {'read_only': True},
            'username': {'required': True, 'min_length': 3},
            'email': {'required': True, 'min_length': 8}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ArticleSerializer(TaggitSerializer, ModelSerializer):
    tags = TagFieldSerializer(style={'base_template': 'textarea.html'})
    author = HiddenField(default=CurrentUserDefault)
    author_id = SerializerMethodField()
    author_name = SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
    
    def get_author_id(self, obj):
        return obj.author.id
    def get_author_name(self,obj):
        return obj.author.user.username

class CommentSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault)
    author_name = SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_author_name(self,obj):
        return obj.author.user.username

class ArticleLikeSerializer(ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = '__all__'

class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'