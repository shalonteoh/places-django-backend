from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from countries.models import Place

# Register your models here.


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label', 'tag_place']
    list_per_page = 10
    search_fields = ['label__istartswith']

    @admin.display(ordering='tag_place')
    def tag_place(self, tag):
        url = (reverse('admin:countries_place_changelist')
               + '?'
               + urlencode({
                   'tag__id': str(tag.id)
               }))
        return format_html('<a href="{}">{}</a>', url, tag.tag_place)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            tag_place=Count('taggedplace__id')
        )
