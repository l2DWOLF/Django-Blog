from django.shortcuts import render
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

# UserProfiles Model View Set # 
class UserProfilesViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# Articles Model View Set # 
class ArticlesViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Comments Model View Set #
class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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