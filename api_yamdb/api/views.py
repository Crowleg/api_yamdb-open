from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from .filters import TitlesFilter
from .mixins import (CommentMixin, CreateListDestroyViewset, ProfileMixins,
                     ReviewMixin, UserMixins)
from .permissions import Titlepermission
from .serializers import (CategorySerializer, GenreSerializer,
                          SignUserSerializer, TitleReadonlySerializer,
                          TitleSerializer, TokenSerializer)

User = get_user_model()


class SignupViewSet(viewsets.GenericViewSet):
    """Вьюсет для регистрации пользователя или обновления кода."""

    serializer_class = SignUserSerializer
    permission_classes = (AllowAny,)

    def send_confirm(self, user):
        """Отправка кода подтверждения на почту."""
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {user.confirmation_code}',
            settings.EMAIL_SENDER,
            [user.email],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        """Создание или обновление кода подтверждения для пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_confirm(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(viewsets.GenericViewSet):
    """Вьюсет для получения JWT токена через username и confirmation_code."""

    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Обработка запроса на создание JWT токена."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class ProfileViewSet(ProfileMixins):
    """Вьюсет для работы с профилем пользователя."""


class UserViewSet(UserMixins):
    """Вьюсет для работы с пользователями."""


class GenreViewSet(CreateListDestroyViewset):
    """Вью для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateListDestroyViewset):
    """Вью для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вью для произведений."""

    queryset = (
        Title.objects.all().annotate(
            rating=Avg('reviews__score')
        ).order_by('name')
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = [Titlepermission]
    http_method_names = ('get', 'patch', 'post', 'delete')

    def get_serializer_class(self):
        """Получение произведений."""
        if self.action in ('retrieve', 'list'):
            return TitleReadonlySerializer
        return TitleSerializer


class ReviewViewSet(ReviewMixin):
    """Вью для отзывов."""

    def get_title(self):
        """Получить произведение."""
        return get_object_or_404(
            Title.objects.all(),
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Получить отзывы к произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Сохранить отзыв."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(CommentMixin):
    """Вью для комментариев."""

    def get_review(self):
        """Получить отзыв."""
        return get_object_or_404(
            Review.objects.all(),
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        """Получить комментарии к отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Сохранить отзыв."""
        serializer.save(author=self.request.user, review=self.get_review())
