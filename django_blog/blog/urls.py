from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from blog.views import * 

router = DefaultRouter()
router.register('admin', UsersViewSet, basename='admin')
router.register('auth', AuthViewSet, basename='auth')
router.register('userprofiles', UserProfilesViewSet, basename='userprofile')
router.register('articles', ArticlesViewSet, basename='article')
router.register('comments', CommentsViewSet, basename='comment')
router.register('article-likes', ArticlesLikeViewSet, basename='article-like')
router.register('comment-likes', CommentsLikeViewSet, basename='comment-like')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', auth_views.obtain_auth_token),
]
