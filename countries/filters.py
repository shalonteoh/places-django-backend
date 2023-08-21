from django_filters.rest_framework import FilterSet
from countries.models import Place


class PlaceFilter(FilterSet):
    class Meta:
        model = Place
        fields = {
            'address_set__state': ['exact'],
            'rating': ['lt', 'gt']
        }
