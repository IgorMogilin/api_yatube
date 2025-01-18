from rest_framework.exceptions import PermissionDenied


class AuthorPermissionMixin:
    """Определяет авторство дляя работы с объектом."""

    def perform_update(self, serializer):
        """Обновляет объект, если пользователь - автор."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет объект, если пользователь - автор."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)
