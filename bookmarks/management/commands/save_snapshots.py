import os
import csv
from pprint import pprint
from datetime import datetime
import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User
from bookmarks.models import Bookmark


class Command(BaseCommand):
    help = "Saves Bookmark Snapshots from HTTP requests"

    def add_arguments(self, parser):
        parser.add_argument(
            "-o", "--offset", type=int, help="Query Offset",
        )
        parser.add_argument(
            "-l", "--limit", type=int, help="Query Limit",
        )

    def handle(self, *args, **kwargs):
        offset = kwargs["offset"] if kwargs["offset"] else 0
        limit = (kwargs["limit"] + offset) if kwargs["limit"] else (10 + offset)

        bookmarks = Bookmark.objects.annotate(Count("snapshots")).filter(
            snapshots__count=0
        )[offset:limit]

        for bookmark in bookmarks:
            self.stdout.write(
                self.style.SUCCESS(
                    'Saving Snapshot for Bookmark: "%s"' % bookmark.title
                )
            )
            bookmark.save_snapshot()
