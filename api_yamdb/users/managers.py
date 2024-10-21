import random
import string

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер для модели пользователя."""

    def generate_confirmation_code(self, length=6):
        """Генерация случайного кода подтверждения для пользователя."""
        return ''.join(random.choices(string.digits, k=length))

    def create_user(self, username, email, role='user',
                    password=None, **extra_fields):
        """Создание пользователя с уникальными username и email."""
        if not username:
            raise ValueError('У пользователя должен быть username.')
        if not email:
            raise ValueError('У пользователя должен быть email.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role,
            confirmation_code=self.generate_confirmation_code(),
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username=username, email=email, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'admin'
        user.set_password(password)
        user.save(using=self._db)
        return user
