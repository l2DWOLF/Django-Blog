from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .models import *
from .serializers import *


## Posts View ## 
class PostsView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
## Posts Manage View ##
class PostsManageView(GenericAPIView, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self,request, pk):
        return self.retrieve(request, pk)

    def put(self,request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)