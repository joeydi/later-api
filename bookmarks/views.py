from rest_framework import viewsets, permissions, generics
from .models import Bookmark
from .serializers import BookmarkSerializer
from .permissions import IsOwner


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnreadViewSet(generics.ListAPIView):
    queryset = Bookmark.objects.filter(folder='Unread')
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class StarredViewSet(generics.ListAPIView):
    queryset = Bookmark.objects.filter(folder='Starred')
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class ArchiveViewSet(generics.ListAPIView):
    queryset = Bookmark.objects.filter(folder='Archive')
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]