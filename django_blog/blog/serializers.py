import re
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HiddenField, SerializerMethodField, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer 
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.contrib.auth.models import User
from blog.models import UserProfile, Article, Comment, ArticleLike, CommentLike
from core.utils import to_lower_strip


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

# Token Serializers # 
class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id 
        token['username'] = user.username
        token['is_admin'] = user.is_superuser
        token['is_mod'] = user.groups.filter(name="moderators").exists()
        return token
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

# Model Serializers # 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True, 'min_length': 3},
            'password': {'write_only': False, 'required': True},
            'email': {'required': True, 'min_length': 8},
            'first_name': {'required': False, 'min_length': 2},
            'last_name': {'required': False, 'min-length': 2}
        }

    def validate(self, attrs):
        for key in attrs:
            attrs[key] = to_lower_strip(attrs[key])
        password = attrs['password']
        print(attrs)

        if any(attr in password for attr in [attrs['username'], attrs['email'], attrs['first_name'], attrs['last_name']] if attr):
            raise ValidationError("Password can't contain your username or email or first or last name.")
        return super().validate(attrs)
    
    def validate_password(self, value):
        if len(value)  < 8 :
            raise ValidationError('Password Must contain 8 or more characters')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance:User, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(password)
        instance.save()
        return instance

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ArticleSerializer(TaggitSerializer, ModelSerializer):
    tags = TagFieldSerializer(style={'base_template': 'textarea.html'})
    author = HiddenField(default=CurrentUserDefault())
    author_id = SerializerMethodField()
    author_name = SerializerMethodField()
    published_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")
    updated_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")
    created_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")

    class Meta:
        model = Article
        fields = '__all__'
    
    def get_author_id(self, obj):
        return obj.author.id
    def get_author_name(self,obj):
        return obj.author.user.username

class CommentSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())
    author_name = SerializerMethodField()
    replies = SerializerMethodField()

    published_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")
    updated_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")

    class Meta:
        model = Comment
        fields = '__all__'

    def get_author_name(self,obj):
        return obj.author.user.username
    def get_replies(self, obj):
        replies = Comment.objects.filter(reply_to=obj)
        return CommentSerializer(replies, many=True).data

class ArticleLikeSerializer(ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = '__all__'

class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'