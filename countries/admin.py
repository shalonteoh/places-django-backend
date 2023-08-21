from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models import Value, Case, When
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


class AddressFilter(admin.SimpleListFilter):
    title = 'rating'
    parameter_name = 'rating'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            ('<3', 'Bad'),
            ('>=3&&<4', 'Average'),
            ('>=4&&<5', 'Good'),
            ('5', 'Perfect')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<3':
            return queryset.filter(rating__lt=3)
        elif self.value() == '>=3&&<4':
            return queryset.filter(rating__gte=3, rating__lt=4)
        elif self.value() == '>=4&&<5':
            return queryset.filter(rating__gte=4, rating__lt=5)
        elif self.value() == '5':
            return queryset.filter(rating=5)
        else:
            return queryset


# Register your models here.
# Change model interface (Customize option @django admin)


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    exclude = ['transit']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display = ['name', 'place_address', 'place_rating']
    list_editable = []
    list_filter = [AddressFilter, 'last_update']
    list_per_page = 5
    list_select_related = ['address']  # Eager loading to optimize query
    search_fields = ['name__istartswith',
                     'place_address']  # Add lookup type

    @admin.display(ordering='place_address')
    def place_address(self, place):
        # Redirect to another page
        url = (reverse('admin:countries_address_changelist')
               + '?'
               + urlencode({
                   'place__id': str(place.id)
               }))
        return format_html('<a href="{}">{}</a>', url, place.place_address)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            place_address=Concat('address__city',
                                 Case(
                                     When(
                                         address__city__isnull=True,
                                         then=Value('')
                                     ),
                                     When(
                                         address__state__name__isnull=True,
                                         then=Value('')
                                     ),
                                     default=Value(', ')
                                 ),
                                 'address__state__name'
                                 )
        )

    @admin.display(ordering='rating')  # Allow sorting for computed field
    def place_rating(self, place):
        if place.rating == 5:
            return 'Perfect'
        elif place.rating >= 4:
            return 'Good'
        elif place.rating >= 3:
            return 'Average'
        else:
            return 'Bad'


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    autocomplete_fields = ['state', 'country', 'place']  # Customize form
    list_display = ['street', 'city', 'country']
    list_select_related = ['country']  # Eager loading to optimize query
    list_per_page = 5


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
