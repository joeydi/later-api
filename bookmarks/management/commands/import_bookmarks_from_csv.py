import os
import csv
from pprint import pprint
from datetime import datetime
import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.contrib.auth.models import User
from bookmarks.models import Bookmark


class Command(BaseCommand):
    help = 'Imports Bookmarks from Instapaper export CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to the export file')
        parser.add_argument('user_id', type=str,
                            help='User ID to assign the Bookmarks')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if not os.path.isfile(file_path):
            raise CommandError('File does not exist: "%s"' % file_path)

        user_id = kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise CommandError('User does not exist: "%s"' % user_id)

        if not os.path.isfile(file_path):
            # self.stdout.write(self.style.ERROR('File does not exist: "%s"' % file_path))
            # return False
            raise CommandError('File does not exist: "%s"' % file_path)

        self.stdout.write(self.style.SUCCESS('Reading file: "%s"' % file_path))

        with open(file_path) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if Bookmark.objects.filter(url=row['URL'], user=user).exists():
                    self.stdout.write(self.style.WARNING('Bookmark already exists: "%s"' % row['Title']))
                    continue

                created_at = datetime.fromtimestamp(int(row['Timestamp']), pytz.UTC)
                bookmark = {
                    'created_at': created_at,
                    'updated_at': created_at,
                    'user': user,
                    'url': row['URL'],
                    'title': row['Title'],
                    'selection': row['Selection'],
                    'folder': row['Folder'],
                }

                self.stdout.write(self.style.SUCCESS('Importing bookmark: "%s"' % row['Title']))
                Bookmark.objects.create(**bookmark)
