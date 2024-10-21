from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseComment(models.Model):
    """Базовая модель комментария."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        db_index=True
    )
    text = models.TextField(
        'Текст',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
