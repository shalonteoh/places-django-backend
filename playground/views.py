from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, ExpressionWrapper, CharField
from django.db.models.aggregates import Count, Avg
from django.db.models.functions import Concat
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from countries.models import Place
from tags.models import TaggedPlace

# Create your views/templates here.
# View function takes request and -> return response
# request handler


def home(request):
    # Object returns an interface to the db.
    # 'all()' return a query set that do not return result immediately
    # query_set = Place.objects.all()

    # 'get(pk=1)' return an object directly. Use try catch to handle object non-found
    # place = Place.objects.get(pk=1)

    # 'filter(pk=0).first return first object from query.
    # queryset = Place.objects.filter(rating__gt=4)
    # queryset = Place.objects.filter(name__icontains='penang')

    # Use Q + | to get OR filter
    # Use Q + & ~ to get AND NOT filter
    # Use F to reference a field
    # Use 'order_by' to sort and '-' to sort descending
    # Use [:] to limit response
    # Use 'ExpressionWrapper' to separate long code
    full_address = ExpressionWrapper(Concat('address__street', Value(', '), 'address__city', Value(
        ', '), 'address__postcode', Value(', '), 'address__state__name'), output_field=CharField())

    queryset = Place.objects \
        .values('id', 'name', 'address__city', 'address__country__name') \
        .filter(
            Q(rating__gt=4) & ~Q(status='I')
        ).annotate(
            # Concat
            full_address=full_address
        ).order_by('name', '-rating')[:3]

    result = Place.objects \
        .filter(
            Q(rating__gt=4) & ~Q(status='I')
        ).aggregate(
            count=Count('id'), average_rating=Avg('rating'))

    # Find content type ID for the model using custom manager
    TaggedPlace.objects.get_tags_for(Place, 1)

    return render(request, 'home.html', {'places': list(queryset), 'result': result})


def createPlace(request):
    place = Place()
    place.name = 'Pasir Buaya'
    place.description = 'beach'
    place.lat = 5.438918
    place.lon = 100.180263
    place.rating = 3
    place.status = 'A'
    place.slug = 'pasir-buaya'
    place.save()

    return render(request, 'place.html', {'place': place})


def updatePlace(request):
    # place = Place.objects.get(pk=8)
    # place.description = 'Beach'
    # place.save()

    # Don't have to query the object first
    place = Place.objects.filter(pk=1).update(description='Beach')

    return render(request, 'place.html', {'place': place})


def deletePlace(request):

    # Revert transaction when caught error
    with transaction.atomic():
        # Delete single object
        place = Place.objects.get(pk=8)
        place.delete()

        # Delete multiple object
        # Place.objects.filter(status='I').delete()

    return render(request, 'place.html', {'place': place})
