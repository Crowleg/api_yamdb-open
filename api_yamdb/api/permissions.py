from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrOwner(BasePermission):
    """
    Позволяет редактировать объект только его владельцу или админ составу.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
                or request.user == obj)


class Titlepermission(BasePermission):
    """Права доступа для работы с произведениями."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj
            )
        )


class CommentPermission(BasePermission):
    """Права доступа для работы с комментариями."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_moderator
                or request.user.is_admin
                or request.user == obj.author
            )
        )


class IsAdmin(BasePermission):
    """
    Проверка наличия роли администратора.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminAllowAnyRead(IsAdmin):
    """
    Проверка наличия роли администратора.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            super().has_permission(self, request, view)
        )
