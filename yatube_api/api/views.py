from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Сохраняет новый объект Post с установленным автором."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновляет существующий объект Post, если пользователь - автор."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет объект Post, если текущий пользователь является автором."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обьектов модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self):
        """Получает запись Post по ID из URL."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает все комментарии для заданной записи Post."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Сохраняет комментарий с автором и связанной записью Post."""
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        """Обновляет существующий комментарий, если пользователь - автор."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет комментарий, если текущий пользователь является автором."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)
