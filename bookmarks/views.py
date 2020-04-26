from rest_framework import viewsets, permissions, generics
from .models import Bookmark
from .serializers import BookmarkSerializer
from .permissions import IsOwner


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnreadViewSet(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Unread")


class StarredViewSet(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Starred")


class ArchiveViewSet(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Archive")


class TagViewSet(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        tag = self.kwargs['tag']
        return user.bookmarks.filter(tags__name__in=[tag])

