from rest_framework import serializers
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            "id",
            "created_at",
            "url",
            "domain",
            "title",
            "description",
            "selection",
            "folder",
            "favicon",
        ]
