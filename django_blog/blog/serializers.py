import re
import json
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, HiddenField, SerializerMethodField, ValidationError
import rest_framework.views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer 
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.contrib.auth.models import User, Group
from blog.models import CustomUser, UserProfile, Article, Comment, ArticleLike, CommentLike
from core.utils import to_lower_strip
from blog.management.commands.seeding_tools import admin_defaults



# Custom Field Serializers #
def req_src_validator(request, method):
    if not request:
        return False
    
    if method == 'api':
        return request.path.startswith('/api/')

    if method == 'html':
        return not request.path.startswith('/api/')

    return False


class TagFieldSerializer(TagListSerializerField):
    def to_internal_value(self, value):
        request = self.context.get('request')
        is_api = req_src_validator(request, 'api')
        is_html = req_src_validator(request, 'html')

        if is_html:
            print("HTML request source — skipping tag processing")
            return super().to_internal_value(value)

        if is_api:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except Exception:
                    value = [tag.strip()
                            for tag in value.split(',') if tag.strip()]
                    
            elif isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
                value = [tag.strip()
                        for tag in value[0].split(',') if tag.strip()]

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
        token['is_staff'] = user.is_staff
        token['is_mod'] = user.groups.filter(name="moderators").exists()
        return token
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

# Model Serializers # 
class UserSerializer(ModelSerializer):
    is_mod = serializers.BooleanField(default=False)
    is_admin = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_mod', 'is_admin']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True, 'min_length': 3},
            'password': {'write_only': True, 'required': True},
            'email': {'required': True, 'min_length': 8},
            'first_name': {'required': False, 'min_length': 2},
            'last_name': {'required': False, 'min_length': 2}
        }

    def validate(self, attrs):
        attrs['username'] = to_lower_strip(attrs['username'])
        attrs['email'] = to_lower_strip(attrs['email'])
        if attrs.get('first_name'):
            attrs['first_name'] = to_lower_strip(attrs['first_name'])
        if attrs.get('last_name'):
            attrs['last_name'] = to_lower_strip(attrs['last_name'])

        password = attrs.get('password')
        if any(attr in password for attr in [
            attrs.get('username'), attrs.get('email'),
            attrs.get('first_name'), attrs.get('last_name')
        ] if attr):
            raise ValidationError("Password can't contain personal your email, first or last name.")
        return attrs
    
    def validate_password(self, value):
        if len(value)  < 8 :
            raise ValidationError('Password Must contain 8 or more characters')
        return value
    
    def create(self, validated_data):
        is_mod = validated_data.pop('is_mod', False)
        is_admin = validated_data.pop('is_admin', False)
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        
        if is_admin:
            user.is_staff = True
        user.save()
        if is_mod or is_admin:
            try:
                mod_group = Group.objects.get(name="moderators")
            except Group.DoesNotExist:
                print("error adding mod to mods group")
            user.groups.add(mod_group)
        
        return user
        
    def update(self, instance:CustomUser, validated_data):
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


class ArticleLikeSerializer(ModelSerializer):
    username = serializers.CharField(source='user.user.username', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ArticleLike
        fields = '__all__'


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class ArticleSerializer(TaggitSerializer, ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())
    author_id = SerializerMethodField()
    author_name = SerializerMethodField()
    likes = SerializerMethodField()
    tags = TagFieldSerializer()

    published_at = serializers.DateTimeField(
        format="%B %d, %Y, %I:%M %p", required=False)
    updated_at = serializers.DateTimeField(
        format="%B %d, %Y, %I:%M %p", required=False)
    created_at = serializers.DateTimeField(
        format="%B %d, %Y, %I:%M %p", required=False)

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'title': {'error_messages': {'required': 'Title is required.', 'blank': 'Please enter a title.'}},
            'tags': {'error_messages': {'required': 'Tags cannot be empty.'}},
            'status': {'error_messages': {'required': 'Status is required.', 'blank': 'Please enter a status.'}},
        }

    def get_author_id(self, obj):
        return obj.author.id

    def get_author_name(self, obj):
        return obj.author.user.username
    
    def get_likes(self, obj):
        likes = obj.likes.all()
        return ArticleLikeSerializer(likes, many=True).data


class CommentSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())
    author_name = SerializerMethodField()
    replies = SerializerMethodField()

    published_at = serializers.DateTimeField(
        format="%B %d, %Y, %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(
        format="%B %d, %Y, %I:%M %p", read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_author_name(self, obj):
        return obj.author.user.username

    def get_replies(self, obj):
        replies = Comment.objects.filter(reply_to=obj)
        return CommentSerializer(replies, many=True).data
