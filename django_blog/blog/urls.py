from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register('userprofiles', UserProfilesViewSet, basename='userprofiles')
router.register('article', ArticlesViewSet, basename='article')
router.register('comments', CommentsViewSet, basename='comment')
router.register('article-likes', ArticlesLikeViewSet, basename='article-likes')
router.register('comment-likes', CommentsLikeViewSet, basename='comment-likes')

urlpatterns = [
    path('', include(router.urls)),
]
