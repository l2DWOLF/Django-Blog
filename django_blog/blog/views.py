from django.shortcuts import render
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from .serializers import *

# API Map View # 
class APIMap(APIView):
    """Blog API Map"""
    def get(self, request):
        return Response({
            "posts": reverse('posts', request=request),
            "posts-manage": reverse('posts-manage', kwargs = {"pk": 1}, request=request)
        })

# Posts View #
class PostsView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
# Posts Manage View # 
class PostsManageView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()