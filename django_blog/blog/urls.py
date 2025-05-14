from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register('userprofiles', UserProfilesViewSet, basename='userprofiles')
router.register('posts', PostsViewSet, basename='post')
router.register('comments',CommentsViewSet, basename='comment')
router.register('post-likes', PostsLikeViewSet, basename='post-likes')
router.register('comment-likes', CommentsLikeViewSet, basename='comment-likes')

urlpatterns = [
    path('router/', include(router.urls)),
]
