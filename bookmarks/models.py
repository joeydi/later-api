from django.db import models
from django.contrib.auth import User


class Bookmark(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookmarks"
    )
    url = models.URLField()
    title = models.CharField(blank=True, max_length=255)
    selection = models.CharField(blank=True, max_length=255)
    folder = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]