from django.contrib import admin
from django.urls import include, path
# from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bookmarks.views import (
    BookmarkCreateAPIView,
    BookmarkRetrieveUpdateAPIView,
    UnreadListAPIView,
    StarredListAPIView,
    ArchiveListAPIView,
    CommonTagsListAPIView,
    TagListAPIView,
    SearchListAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("bookmarks/", BookmarkCreateAPIView.as_view()),
    path("bookmarks/<int:pk>/", BookmarkRetrieveUpdateAPIView.as_view()),
    path("bookmarks/unread/", UnreadListAPIView.as_view()),
    path("bookmarks/unread/", UnreadListAPIView.as_view()),
    path("bookmarks/starred/", StarredListAPIView.as_view()),
    path("bookmarks/archive/", ArchiveListAPIView.as_view()),
    path("bookmarks/tag/", CommonTagsListAPIView.as_view()),
    path("bookmarks/tag/<tag>/", TagListAPIView.as_view()),
    path("bookmarks/search/<query>/", SearchListAPIView.as_view()),
]
