from rest_framework import serializers
from .models import Bookmark
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "name",
        ]

class BookmarkSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

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
            "tags"
        ]
