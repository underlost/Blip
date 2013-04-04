from __future__ import absolute_import

from django.contrib import admin
from .models import EntryType, Entry


admin.site.register(Entry,
    list_display=["entry_type", "pub_date", "is_private"],
    list_filter=["entry_type", "is_private"],
    raw_id_fields=['owner'],
    list_per_page=500,
)

admin.site.register(EntryType,
    prepopulated_fields={'slug': ('name',)},
)
