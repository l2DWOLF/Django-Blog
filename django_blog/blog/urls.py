from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register('posts', PostsViewSet, basename='post')

urlpatterns = [
    path('', APIMap.as_view(), name="map"),
    path('router/', include(router.urls)),
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<int:pk>', PostsManageView.as_view(), name='posts-manage'),
]
