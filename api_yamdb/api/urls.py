from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ProfileViewSet, ReviewViewSet, SignupViewSet, TitleViewSet,
                    TokenViewSet, UserViewSet)

app_name = 'api'
router_v1 = routers.DefaultRouter()

router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'titles\/(?P<title_id>\d+)\/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles\/(?P<title_id>\d+)\/reviews'
                   r'\/(?P<review_id>\d+)\/comments',
                   CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet, basename='users')

auth_patterns = [
    path('signup/', SignupViewSet.as_view({'post': 'create'}), name='signup'),
    path('token/', TokenViewSet.as_view({'post': 'create'}), name='token'),
]

urlpatterns = [
    path('v1/users/me/',
         ProfileViewSet.as_view({'get': 'retrieve',
                                 'patch': 'partial_update'}),
         name='me'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
