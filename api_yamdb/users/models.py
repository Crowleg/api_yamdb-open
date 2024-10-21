from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from .managers import CustomUserManager
from .validators import validate_username
from .constants import (
    USER_BASE_LENGTH,
    USER_PASS_LENGTH,
    USER_ROLE_LENGTH,
    USER_ROLES_CHOICES,
    USER_CODE_LENGTH,
    USER_EMAIL_LENGTH,
    USER_ROLE_ADMIN,
    USER_ROLE_MODERATOR
)


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""
    username = models.CharField(
        max_length=USER_BASE_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[validate_username],
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        max_length=USER_EMAIL_LENGTH,
    )
    role = models.CharField(
        max_length=USER_ROLE_LENGTH,
        choices=USER_ROLES_CHOICES,
        default='user',
        verbose_name='Роль',
    )
    first_name = models.CharField(
        max_length=USER_BASE_LENGTH,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=USER_BASE_LENGTH,
        blank=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе',
    )
    confirmation_code = models.CharField(
        max_length=USER_CODE_LENGTH,
        blank=True,
        verbose_name='Код подтверждения',
    )
    password = models.CharField(
        max_length=USER_PASS_LENGTH,
        verbose_name='Пароль',
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус сотрудника',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный статус',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Статус суперпользователя',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        """Мета-класс для модели пользователя."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'role')

    def __str__(self):
        """Строковое представление модели пользователя."""
        return self.username

    def save(self, *args, **kwargs):
        """Обновление роли пользователя."""
        if self.is_superuser:
            self.role = USER_ROLE_ADMIN
        super().save(*args, **kwargs)

    @property
    def is_moderator(self):
        """Проверка пользователя на роль модератора."""
        return self.role == USER_ROLE_MODERATOR

    @property
    def is_admin(self):
        """Проверка пользователя на роль администратора."""
        return self.role == USER_ROLE_ADMIN or self.is_superuser
