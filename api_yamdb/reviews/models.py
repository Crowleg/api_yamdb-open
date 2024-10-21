from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.basemodels import BaseComment
from .constants import (
    TITLE_NAME_LENGTH,
    CATEGORY_NAME_LENGTH,
    CATEGORY_SLUG_LENGTH,
    GENRE_NAME_LENGTH,
    GENRE_SLUG_LENGTH,
    REVIEW_SCORE_MIN,
    REVIEW_SCORE_MAX
)


class Category(models.Model):
    """Модель категории произведений."""

    name = models.CharField(
        'Категория',
        max_length=CATEGORY_NAME_LENGTH
    )
    slug = models.SlugField(
        unique=True,
        max_length=CATEGORY_SLUG_LENGTH
    )

    class Meta:
        """Мета-класс для категории."""

        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Строковое представление модели категории."""
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        'Жанр',
        max_length=GENRE_NAME_LENGTH
    )
    slug = models.SlugField(
        unique=True,
        max_length=GENRE_SLUG_LENGTH
    )

    class Meta:
        """Мета-класс для жанров."""

        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Строковое представление модели жанров."""
        return self.name


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""

    name = models.CharField(
        verbose_name='Произведение',
        max_length=TITLE_NAME_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        verbose_name='Жанр',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        db_index=True,
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        """Мета-класс для модели произведений."""

        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Строковое представление модели произведений."""
        return self.name


class Review(BaseComment):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        db_index=True
    )
    score = models.IntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(REVIEW_SCORE_MIN),
            MaxValueValidator(REVIEW_SCORE_MAX)
        ]
    )

    class Meta(BaseComment.Meta):
        """Мета-класс для модели отзыва."""

        ordering = ('title',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        """Строковое представление модели отзыва."""
        return self.text


class Comment(BaseComment):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta(BaseComment.Meta):
        """Мета-класс для модели комментария."""

        ordering = ('review',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        """Строковое представление модели комментария."""
        return self.text
