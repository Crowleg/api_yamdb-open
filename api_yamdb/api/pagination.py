from rest_framework import pagination


class UserPagination(pagination.PageNumberPagination):
    """Класс пагинации для пользователя."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
