from rest_framework import serializers

from reviews.models import Comment


class BaseCommentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        """Мета-класс для Комментариев."""

        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'pub_date',)
