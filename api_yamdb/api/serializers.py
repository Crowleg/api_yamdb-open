from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError

from reviews.constants import TITLE_NAME_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import USER_BASE_LENGTH, USER_EMAIL_LENGTH
from users.validators import validate_username
from .base_serializers import BaseCommentSerializer

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля."""

    role = serializers.CharField(read_only=True)

    class Meta:
        """Мета-класс для сериализатора профиля."""
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)

    def validate(self, data):
        """Проверка уникальности username и email при обновлении."""
        if 'username' in data:
            if User.objects.exclude(
                pk=self.instance.pk
            ).filter(
                username=data['username']
            ).exists():
                raise ValidationError({
                    'username': 'Username already exists'
                })
        if 'email' in data:
            if User.objects.exclude(
                pk=self.instance.pk
            ).filter(
                email=data['email']
            ).exists():
                raise ValidationError({
                    'email': 'Email already exists'
                })

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        allow_blank=False,
        max_length=USER_BASE_LENGTH,
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        allow_blank=False,
        required=True,
        max_length=USER_EMAIL_LENGTH
    )

    class Meta:
        """Мета-класс для сериализатора пользователя."""

        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio'
        )

    def validate_username(self, value):
        """Проверка уникальности username."""
        request = self.context.get('request')
        if request and request.method in ['PATCH', 'POST']:
            if User.objects.filter(username=value).exists():
                raise ValidationError('Username already exists')
        return value

    def validate_email(self, value):
        """Проверка уникальности email."""
        request = self.context.get('request')
        if request and request.method in ['PATCH', 'POST']:
            if User.objects.filter(email=value).exists():
                raise ValidationError('Email already exists')
        return value


class SignUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(
        allow_blank=False,
        max_length=USER_BASE_LENGTH,
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        allow_blank=False,
        required=True,
        max_length=USER_EMAIL_LENGTH
    )

    class Meta:
        """Мета-класс для сериализатора пользователя."""

        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        """Создание нового пользователя."""
        return User.objects.create_user(**validated_data)

    def update_confirmation_code(self, user):
        """Обновление кода подтверждения пользователя."""
        user.confirmation_code = User.objects.generate_confirmation_code()
        user.save()
        return user

    def save(self, **kwargs):
        """Сохранение пользователя."""
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        user_exists = User.objects.filter(
            username=username,
            email=email
        ).exists()
        if user_exists:
            user = User.objects.get(username=username, email=email)
            self.update_confirmation_code(user)
        else:
            user = self.create(self.validated_data)
        return user

    def validate(self, data):
        """Проверка уникальности username и email."""
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            return data
        if (
            User.objects.filter(username=username).exists()
            and User.objects.filter(email=email).exists()
        ):
            raise ValidationError({
                'username': 'Пользователь с таким username уже существует.',
                'email': 'Пользователь с таким email уже существует.'
            })
        if User.objects.filter(username=username).exists():
            raise ValidationError({
                'username': 'Пользователь с таким username уже существует.'
            })
        if User.objects.filter(email=email).exists():
            raise ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=USER_BASE_LENGTH,
        write_only=True
    )
    confirmation_code = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        """Мета-класс для сериализатора токена."""

        model = User
        fields = ('username', 'confirmation_code', 'token')

    def validate(self, data):
        """Проверка корректности кода подтверждения и username."""
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound({
                'username': 'Пользователь не найден.'
            })
        if data['confirmation_code'] != user.confirmation_code:
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )
        return {'user': user}


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        """Мета-класс для сериализатора жанров."""
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        """Мета-класс для сериализатора категорий."""

        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleReadonlySerializer(serializers.ModelSerializer):
    """Сериализатор произведений для List и Retrieve."""

    rating = serializers.IntegerField(read_only=True, default=0)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        """Мета-класс для сериализатора произведений."""

        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для Create, Partial_Update и Delete."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True
    )
    name = serializers.CharField(
        max_length=TITLE_NAME_LENGTH,
    )

    class Meta:
        """Мета-класс для сериализатора произведений."""

        fields = '__all__'
        model = Title

    def validate_year(self, value):
        """Валидация года произведения."""
        if value > timezone.now().year:
            raise ValidationError(
                'Год выпуска %(value)s больше текущего.'
            )
        return value

    def validate_genre(self, value):
        """Валидация жанров."""
        if not value:
            raise ValidationError(
                'Пустой список для поля `genre`.'
            )
        return value


class ReviewSerializer(BaseCommentSerializer):
    """Сериализатор для Отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta(BaseCommentSerializer.Meta):
        """Мета-класс для сериализатора Отзывов."""

        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        """Проверка уникальности отзыва"""
        if not self.context.get('request').method == 'POST':
            return data
        if Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context.get('view').kwargs.get('title_id')
        ).exists():
            raise ValidationError(
                'Отзыв уже существует.'
            )
        return data


class CommentSerializer(BaseCommentSerializer):
    """Сериализатор для Комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Мета-класс для сериализатора Комментариев."""
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
