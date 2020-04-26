from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count, Q
from .models import Bookmark, Snapshot


class SnapshotAdmin(admin.ModelAdmin):
    readonly_fields = ['bookmark']
    date_hierarchy = 'created_at'
    list_display = [
        'status_code',
        'created_at',
    ]


admin.site.register(Snapshot, SnapshotAdmin)


class SnapshotInline(admin.StackedInline):
    model = Snapshot
    extra = 0


class StatusCodeFilter(SimpleListFilter):
    title = 'status_code'
    parameter_name = 'status_code'

    def lookups(self, request, model_admin):
        status_codes = Snapshot.objects.values_list(
            'status_code', flat=True).order_by('status_code').distinct()
        return [(code, code) for code in status_codes]

    def queryset(self, request, queryset):
        with_status_code = Count('snapshots', filter=Q(snapshots__status_code=self.value()))
        queryset = queryset.annotate(status_code_count=with_status_code).filter(status_code_count__gt=0)
        return queryset


class BookmarkAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = [
        'status_code',
        'title',
        'url',
        'user',
        'selection',
        'folder',
        'created_at',
    ]
    list_filter = [
        'folder',
        StatusCodeFilter,
    ]
    inlines = [
        SnapshotInline
    ]


admin.site.register(Bookmark, BookmarkAdmin)
