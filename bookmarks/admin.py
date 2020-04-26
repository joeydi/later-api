from django.contrib import admin
from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = [
        'title',
        'url',
        'user',
        'selection',
        'folder',
        'created_at',
    ]


admin.site.register(Bookmark, BookmarkAdmin)
