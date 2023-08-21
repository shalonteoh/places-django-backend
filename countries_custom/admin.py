from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from countries.admin import PlaceAdmin
from tags.models import TaggedPlace
from countries.models import Place


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedPlace
    extra = 0
    min_num = 1


class CustomPlaceAdmin(PlaceAdmin):
    inlines = [TagInline]


admin.site.unregister(Place)
admin.site.register(Place, CustomPlaceAdmin)
