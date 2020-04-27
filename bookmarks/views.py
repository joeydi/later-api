from rest_framework import viewsets, permissions, generics
from django.db import models
from .models import Bookmark
from .serializers import BookmarkSerializer, TagSerializer
from .permissions import IsOwner


class BookmarkRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.all()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UnreadListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Unread")


class StarredListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Starred")


class ArchiveListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.filter(folder="Archive")


class TagListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        tag = self.kwargs["tag"]
        return user.bookmarks.filter(tags__name__in=[tag])


class CommonTagsListAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Bookmark.tags.most_common(extra_filters={'bookmark__user': user})
