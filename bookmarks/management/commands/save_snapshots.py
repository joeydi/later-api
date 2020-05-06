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
    help = 'Saves Bookmark Snapshots from HTTP requests'

    def handle(self, *args, **kwargs):
        # Get the next 100 Bookmarks that don't have a Snapshot
        bookmarks = Bookmark.objects.annotate(Count('snapshots')).filter(snapshots__count=0)[2:1000]

        for bookmark in bookmarks:
            self.stdout.write(self.style.SUCCESS('Saving Snapshot for Bookmark: "%s"' % bookmark.title))
            bookmark.save_snapshot()
