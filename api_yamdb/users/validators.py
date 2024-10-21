from django.core.exceptions import ValidationError
import re


def validate_username(value):
    """Кастомный валидатор для проверки username."""
    if value == "me":
        raise ValidationError(
            "Использование 'me' в качестве username недопустимо."
        )
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError(
            "Поле 'username' может содержать только буквы, цифры "
            "и символы @ . + - _."
        )
