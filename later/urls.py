from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from bookmarks.views import (
    BookmarkViewSet,
    UnreadViewSet,
    StarredViewSet,
    ArchiveViewSet,
)

router = routers.DefaultRouter()
router.register(r"bookmarks", BookmarkViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("bookmarks/unread/", UnreadViewSet.as_view()),
    path("bookmarks/starred/", StarredViewSet.as_view()),
    path("bookmarks/archive/", ArchiveViewSet.as_view()),
    path("", include(router.urls)),
]
