from rest_framework import serializers
from .models import Bookmark
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    num_times = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = [
            "name",
            "num_times",
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Bookmark
        fields = [
            "user",
            "id",
            "created_at",
            "url",
            "domain",
            "title",
            "description",
            "selection",
            "folder",
            "favicon",
            "tags",
        ]
