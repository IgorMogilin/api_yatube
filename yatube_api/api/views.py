from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from api.utils.mixins.author_permission_mixin import AuthorPermissionMixin
from posts.models import Comment, Group, Post


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Сохраняет новый объект Post с установленным автором."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обьектов модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
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
