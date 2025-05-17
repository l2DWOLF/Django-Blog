from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import DjangoModelPermissions
from core.permissions import IsAdminOrModerator, IsOwnerOrReadOnly
from core.utils import parse_int
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
    permission_classes = [DjangoModelPermissions]

# Comments Model View Set #
class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        root_comments = []
        comments = res.data
        comments_dict = {comment["id"]:comment for comment in comments}
# [tree structure nested comments/replies sorting]: 
# if comment reply_to isn't null, get the parent/article of reply, 
# if parent has no replies create replies list object, 
# append the comment as a reply to the parent.
# n*2
        for comment in comments:
            parent_id = comment['reply_to']
            if parent_id is None:
                root_comments.append(comment)
            else:
                parent = comments_dict.get(parent_id)
               # if parent and parent["article"] == comment["article"]:
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