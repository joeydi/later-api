from rest_framework import viewsets, permissions, generics
from django.db import models
from .models import Bookmark
from .serializers import BookmarkSerializer, TagSerializer
from .permissions import IsOwner


class BookmarkCreateAPIView(generics.CreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.bookmarks.all()

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
        return Bookmark.tags.most_common(extra_filters={"bookmark__user": user})


class SearchListAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        query = self.kwargs["query"]
        # results = user.bookmarks.annotate(search=SearchVector("title"),).filter(
        #     search=query
        # )

        return user.bookmarks.filter(title__search=query)
