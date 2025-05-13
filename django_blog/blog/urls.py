from django.urls import path
from .views import * 

urlpatterns = [
    path('', APIMap.as_view(), name="map"),
    path('posts/', PostsView.as_view(), name='posts'),
    path('posts/<int:pk>', PostsManageView.as_view(), name='posts-manage'),
]
