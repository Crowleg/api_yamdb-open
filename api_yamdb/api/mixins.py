from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .pagination import UserPagination
from .permissions import CommentPermission, IsAdmin, IsStaffOrOwner
from .serializers import (
    ProfileSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer
)

User = get_user_model()


class CreateListDestroyViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс миксин создания и удаления."""

    permission_classes = [IsStaffOrOwner]
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class CommentMixin(viewsets.ModelViewSet):
    """Миксин для комментариев."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [CommentPermission]
    serializer_class = CommentSerializer


class ReviewMixin(viewsets.ModelViewSet):
    """Миксин для отзывов."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [CommentPermission]
    serializer_class = ReviewSerializer


class ProfileMixins(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для профиля."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя."""
        return self.request.user


class UserMixins(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'patch', 'delete', 'post']
