from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может видеть и редактировать только свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешает GET-запросы любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверка, является ли пользователь модератором. Модераторы не могут создавать и удалять продукты.
        """
        if request.method in ['PUT', 'PATCH']:
            return request.user.groups.filter(name='moderators').exists()
        return request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()


class IsProductAuthor(permissions.BasePermission):
    """
    Пользователь может удалять продукт только, если он его автор.
    """
    message = "This action is authorized only to the owner."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course'):
            course_author = obj.course.author
        else:
            course_author = obj.author

        return request.user == course_author
