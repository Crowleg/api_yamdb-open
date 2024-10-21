from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Административный интерфейс для пользователей."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('role',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def get_queryset(self, request):
        """Возвращает набор объектов, доступных для администрирования."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        return qs.filter(role='user')

    def has_change_permission(self, request, obj=None):
        """Определяет, имеет ли пользователь право изменять объект."""
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        if obj and obj.role == 'user':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        """Определяет, имеет ли пользователь право удалять объект."""
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        if obj and obj.role == 'user':
            return True
        return False

    def save_model(self, request, obj, form, change):
        """Сохраняет объект и устанавливает роль."""
        if not obj.pk:
            obj.role = form.cleaned_data['role']
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для категорий."""
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административный интерфейс для жанров."""
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Административный интерфейс для произведений."""
    list_display = ('name', 'year', 'category')
    search_fields = ('name', 'year', 'category__name')
    filter_horizontal = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административный интерфейс для отзывов."""
    list_display = ('title', 'author', 'score', 'pub_date')
    search_fields = ('title__name', 'author__username', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административный интерфейс для комментариев."""
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = (
        'review__title__name', 'author__username', 'text', 'pub_date'
    )
