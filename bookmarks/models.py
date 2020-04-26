import json
import requests
from opengraph_py3 import OpenGraph
from dragnet import extract_content
from dragnet.blocks import BlockifyError
from django.db import models
from django.contrib.auth.models import User


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

    @property
    def status_code(self):
        return self.snapshots.first().status_code if self.snapshots.exists() else None

    def save_snapshot(self):
        try:
            r = requests.get(self.url)
        except requests.exceptions.SSLError:
            print('SSLError')
            return None

        snapshot = {
            'bookmark': self,
            'content': r.text,
            'headers_json': json.dumps({item[0]: item[1] for item in r.headers.items()}),
            'status_code': r.status_code,
        }

        try:
            ogp = OpenGraph(html=r.content)
            snapshot['opengraph_json'] = ogp.to_json()
        except AttributeError:
            print('OpenGraph Error')
            pass

        try:
            snapshot['parsed_content'] = extract_content(r.content)
        except BlockifyError:
            print('BlockifyError')
            pass

        return Snapshot.objects.create(**snapshot)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Snapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    bookmark = models.ForeignKey(
        Bookmark, on_delete=models.CASCADE, related_name="snapshots"
    )
    content = models.TextField(blank=True)
    headers_json = models.TextField(blank=True)
    parsed_content = models.TextField(blank=True)
    status_code = models.IntegerField(blank=True)
    opengraph_json = models.TextField(blank=True)

    @property
    def headers(self):
        return json.loads(self.headers_json)

    @property
    def opengraph(self):
        return json.loads(self.opengraph_json)

    def __str__(self):
        return self.bookmark.title

    class Meta:
        ordering = ["-created_at"]