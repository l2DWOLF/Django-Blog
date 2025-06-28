from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from core.permissions import IsOwnerOrModelPermissions, IsOwnerOrReadOnly, IsAdminOrOwner, IsAdminOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from core.authentication import generate_jwt_tokens
from core.utils import nest_comments, parse_int
from blog.throttling import *
from .models import *
from .serializers import *


# Auth View Set #
class AuthViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttling_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_rates = {'anon': '5/minute', 'user': '15/minute'}

    def list(self, request):
        return Response({
            "login": reverse('auth-login', request=request),
            "register": reverse('auth-register', request=request),
            "logout": reverse('auth-logout', request=request)
        })

    @action(detail=False, methods=['post', 'get'])
    def login(self, request):
        login_data = { 
            'username': request.data.get('username'),
            'password': request.data.get('password')
        }
        serializer = AuthTokenSerializer(
            data=login_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        jwt = generate_jwt_tokens(user)
        login(request, user)
        return Response({"token": token.key, 'jwt': jwt})

    @action(detail=False, methods=['post', 'get'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        jwt = generate_jwt_tokens(user)
        login(request, user)
        return Response({"token": token.key, 'jwt': jwt})

    @action(detail=False, methods=['post', 'get'],
            permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            logout(request)
            if request.user.is_authenticated:
                request.user.auth_token.delete()
            
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            print(e)

        return Response({"message": f"you're now logged out {request.user.username}, see you soon!"})
# Refresh Token View # 
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

# Users Model View Set #
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrOwner]

# UserProfiles Model View Set #
class UserProfilesViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrModelPermissions]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrReadOnly()]
        return super().get_permissions()

# Articles Model View Set #
class ArticlesViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrModelPermissions]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['author', 'title',
                        'content', 'published_at', 'updated_at']
    search_fields = ['title', 'content']
    mapping = {
        'create': [CreateArticleUserThrottle, CreateArticleAnonThrottle],
        'list': [ListArticlesUserThrottle, ListArticlesAnonThrottle]
    }

    def get_throttles(self):
        throttles = self.mapping.get(self.action, [])
        return [throttle() for throttle in throttles]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrReadOnly()]
        if self.action == 'get_comments_for_article':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments_for_article(self, request, pk=None):
        article = self.get_object()
        comments = Comment.objects.filter(article=article, status='publish', reply_to=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Comments Model View Set #
class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrModelPermissions]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        reply_to = data.get('reply_to')
        article_id = parse_int(data.get('article'))
    # validate replies article match
        if reply_to:
            replied = Comment.objects.get(id=reply_to)
            if replied and replied.article.id != article_id:
                return Response({"error": "Comment reply Must be under the Same Article"}, status=400)
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()

# Articles Like Model View Set #
class ArticlesLikeViewSet(ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer
    permission_classes = [IsAdminOrReadOnly]
# Comments Like Model View Set #
class CommentsLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAdminOrReadOnly]
