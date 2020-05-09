import json
import requests
from lxml import etree
from urllib.parse import urlparse
from dragnet import extract_content
from dragnet.blocks import BlockifyError
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from favicon.favicon import tags as favicon_tags

from .utils import TextRank4Keyword, LaterOpenGraph


class Bookmark(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    url = models.URLField(max_length=2048)
    title = models.CharField(blank=True, max_length=255)
    selection = models.TextField(blank=True)
    folder = models.CharField(blank=True, max_length=255, default="Unread")
    tags = TaggableManager(blank=True)

    @property
    def status_code(self):
        return self.snapshots.first().status_code if self.snapshots.exists() else None

    @property
    def domain(self):
        return urlparse(self.url).hostname

    @property
    def description(self):
        return (
            self.snapshots.first().opengraph.get("description")
            if self.snapshots.exists()
            else None
        )

    @property
    def favicon(self):
        return self.snapshots.first().favicon if self.snapshots.exists() else None

    def save_snapshot(self):
        try:
            r = requests.get(self.url)
        except (
            requests.exceptions.SSLError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ) as e:
            print(e)
            return None

        snapshot = {
            "bookmark": self,
            "content": r.text,
            "headers_json": json.dumps(
                {item[0]: item[1] for item in r.headers.items()}
            ),
            "status_code": r.status_code,
        }

        try:
            ogp = LaterOpenGraph(html=r.text)
            snapshot["opengraph_json"] = ogp.to_json()
        except AttributeError:
            print("OpenGraph Error")
            pass

        try:
            snapshot["parsed_content"] = extract_content(r.text)
        except BlockifyError:
            print("dragnet extract_content: BlockifyError")
            snapshot["parsed_content"] = ""
            pass

        try:
            tags = favicon_tags(self.url, r.text)
            tags = sorted(tags, key=lambda i: i.width + i.height, reverse=True)
            snapshot["favicon"] = tags[0].url
            print(snapshot["favicon"])
        except IndexError:
            print("No Favicon Found")
            pass

        try:
            tr4w = TextRank4Keyword()
            tr4w.analyze(snapshot["parsed_content"])
            keywords_weighted = tr4w.node_weight.items()
            keywords_sorted = sorted(
                keywords_weighted, key=lambda item: item[1], reverse=True
            )
            tags = [k.lower() for (k, v) in keywords_sorted if len(k) < 100][:9]
            self.tags.add(*tags)
        except MemoryError:
            print("MemoryError while parsing keywords")
            pass

        # If the bookmark does not yet have a title, grab it from the document title
        if not self.title:
            try:
                parser = etree.XMLParser(recover=True)
                document = etree.fromstring(r.text, parser)
                self.title = document.find(".//title").text
                self.save()
            except ValueError:
                print("Error parsing document...")
                pass
            except AttributeError:
                print("No title tag found...")
                pass

        # If we still don't have a title, grab it from the opengraph tags
        if not self.title and ogp.get("title"):
            self.title = ogp.get("title")
            self.save()

        return Snapshot.objects.create(**snapshot)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


@receiver(models.signals.post_save, sender=Bookmark)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.save_snapshot()


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
    favicon = models.URLField(blank=True, max_length=2048)

    @property
    def headers(self):
        return json.loads(self.headers_json)

    @property
    def opengraph(self):
        return json.loads(self.opengraph_json) if self.opengraph_json else None

    def __str__(self):
        return self.bookmark.title

    class Meta:
        ordering = ["-created_at"]
