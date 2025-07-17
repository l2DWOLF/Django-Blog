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
from blog.management.commands.seeding_tools import user_defaults
from .models import *
from .serializers import *


# Auth View Set #
class AuthViewSet(ViewSet):
    queryset = CustomUser.objects.all()
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

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(
                {"backend_error": [
                    "Wrong username or password, please try again."]},
                status=status.HTTP_400_BAD_REQUEST
            )

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

        UserProfile.objects.get_or_create(user=user)

        token, _ = Token.objects.get_or_create(user=user)
        jwt = generate_jwt_tokens(user)
        login(request, user)
        return Response({"token": token.key, 'jwt': jwt})

    @action(detail=False, methods=['post', 'get'],
            permission_classes=[])
    def logout(self, request):
        try:
            logout(request)
            if request.user.is_authenticated:
                request.user.auth_token.delete()
            
            refresh_token = request.data.get("refresh")
            try:
                if refresh_token:
                    try: 
                        token = RefreshToken(refresh_token)
                        token.blacklist()
                        print("[LOGOUT] Refresh token blacklisted successfully.")
                    except Exception as e:
                        print("[LOGOUT] expired token.", e)
            except Exception as e:
                print("[LOGOUT] Unexpected error during logout:", e)
                return Response({"detail": "Logout failed", "error": str(e)}, status=400)
        except Exception as e:
            print(e)
        return Response({"message": f"you're now logged out {request.user.username}, see you soon!"})
    
# Refresh Token View # 
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

# Users Model View Set #
class UsersViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrOwner]

    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_account(self, request):
        user = request.user
        user_profile = user.userprofile 

        if request.user.id != user.id and not request.user.is_superuser:
            return Response({"detail": "you do not have permission to edit this account."}, status=403)

        user_data = request.data.get("user", {})
        profile_data = request.data.get("userprofile", {})

        user_serializer = UserSerializer(user, data=user_data, partial=True, context={'request': request})
        profile_serializer = UserProfileSerializer(user_profile, data=profile_data, partial=True, context={'request': request})

        user_is_valid = user_serializer.is_valid()
        profile_is_valid = profile_serializer.is_valid()

        if user_is_valid and profile_is_valid:
            user_serializer.save()
            profile_serializer.save()
            return Response({
                "user": user_serializer.data,
                "userprofile": profile_serializer.data   
            }, status=status.HTTP_200_OK)
        
        return Response({
            "backend_error": [
                *[f"user.{k}: {v[0]}" for k,
                    v in user_serializer.errors.items()],
                *[f"profile.{k}: {v[0]}" for k,
                    v in profile_serializer.errors.items()],
            ]
        }, status=status.HTTP_400_BAD_REQUEST)

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
    search_fields = ['author__user__username', 'title', 'content']
    mapping = {
        'create': [CreateArticleUserThrottle, CreateArticleAnonThrottle],
        'list': [ListArticlesUserThrottle, ListArticlesAnonThrottle]
    }

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
        data = request.data.copy() 
        reply_to = data.get('reply_to')
        article_id = parse_int(data.get('article'))

        if reply_to:
            try:
                replied = Comment.objects.get(id=reply_to)
                if replied.article.id != article_id:
                    return Response({"error": "Comment reply must be under the same article."}, status=400)
            except Comment.DoesNotExist:
                return Response({"error": "Reply-to comment not found."}, status=404)

        if 'author' not in data:
            data['author'] = request.user.userprofile.id

        serializer = self.get_serializer(
            data=data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print("🚨 Validation Error:", e.detail)
            return Response(e.detail, status=400)

        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Articles Like Model View Set #
class ArticlesLikeViewSet(ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        article_id = request.data.get("article")
        status_value = request.data.get("status")

        if not article_id or not status_value:
            return Response({"detail": "Article and status are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

        existing_like = ArticleLike.objects.filter(
            user=user_profile, article=article).first()

        # Toggle behavior
        if existing_like:
            if existing_like.status == status_value:
                existing_like.delete()
                return Response({"detail": f"{status_value} removed."}, status=status.HTTP_204_NO_CONTENT)
            else:
                existing_like.status = status_value
                existing_like.save()
                return Response(self.get_serializer(existing_like).data, status=status.HTTP_200_OK)

        # No existing like/dislike → create new
        serializer = self.get_serializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        article_like = serializer.save(user=user_profile)
        return Response(self.get_serializer(article_like).data, status=status.HTTP_201_CREATED)




# Comments Like Model View Set #
class CommentsLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAdminOrReadOnly]
