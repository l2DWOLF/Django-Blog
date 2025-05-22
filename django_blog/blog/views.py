from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from core.permissions import IsOwnerOrModelPermissions
from core.authentication import generate_jwt_tokens
from core.utils import parse_int
from .models import *
from .serializers import *

# Auth View Set # 
class AuthViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def list(self, request):
        return Response({
            "login": reverse('auth-login', request=request),
            "register": reverse('auth-register', request=request),
            "logout": reverse('auth-logout', request=request)
        })
    
    @action(detail = False, methods=['post', 'get'])
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        jwt = generate_jwt_tokens(user)
        login(request, user)
        return Response({"token": token.key, 'jwt': jwt})

    @action(detail = False, methods=['post', 'get'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        jwt = generate_jwt_tokens(user)
        login(request, user)
        return Response({"token": token.key, 'jwt': jwt})

    @action(detail = False, methods=['post', 'get'], 
            permission_classes = [IsAuthenticated])    
    def logout(self, request):
        try:
            logout(request)
            request.user.auth_token.delete()
        except Exception as e: 
            print(e)
        return Response({"message": f"you're now logged out {request.user.username}, see you soon!"})


# Users Model View Set #
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# UserProfiles Model View Set # 
class UserProfilesViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_class = [IsOwnerOrModelPermissions]

# Articles Model View Set # 
class ArticlesViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrModelPermissions]

# Comments Model View Set #
class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrModelPermissions]
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        root_comments = []
        comments = res.data
        comments_dict = {comment["id"]:comment for comment in comments}
        # n*2
        for comment in comments:
            parent_id = comment['reply_to']
            if parent_id is None:
                root_comments.append(comment)
            else:
                parent = comments_dict.get(parent_id)
                if "replies" not in parent:
                    parent["replies"] = []
                parent["replies"].append(comment)
        res.data = root_comments
        return res

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

# Articles Like Model View Set #
class ArticlesLikeViewSet(ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer
# Comments Like Model View Set # 
class CommentsLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer


""" # API Map View # 
class APIMap(APIView):
    ###Blog API Map###
    def get(self, request):
        return Response({
            "posts": reverse('posts', request=request),
            "posts-manage": reverse('posts-manage', kwargs = {"pk": 1}, request=request)
        }) """

""" # Posts View Set # 
class PostsViewSet(ViewSet):
    ###Example View Set###

    def list(self, request):
        posts = Post.objects.all()
        return Response(f'list: {posts}')
    def create(self, request):
        return Response('create')
    def retrieve(self, request, pk=None):
        return Response('retrieve')
    def update(self, request, pk=None):
        return Response('update')
    def partial_update(self, request, pk=None):
        return Response('partial update')
    def destroy(self, request, pk=None):
        return Response('destroy/delete')
# Posts (List) View #
class PostsView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
# Posts Manage (RetrieveUpdateDestroy) View # 
class PostsManageView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all() """