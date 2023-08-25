from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from countries.filters import PlaceFilter
from .models import Place, Address, Visitor
from .serializers import PlaceSerializer, AddressSerializer, VisitorSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.select_related(
        'address_set', 'address_set__state', 'address_set__country').order_by('id')
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PlaceFilter
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, pk):
        place = get_object_or_404(Place, pk=pk)  # Catch 404 exception
        if 'address' in request.data:
            address, _ = Address.objects.get_or_create(place_id=pk)
            address_serializer = AddressSerializer(
                address, data=request.data['address'],
                context={'request': request}
            )
            address_serializer.is_valid(raise_exception=True)
            address_serializer.save()
            del request.data['address']
        serializer = PlaceSerializer(
            place, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.select_related('state', 'country')
        return queryset.filter(place_id=self.kwargs['place_pk'])

    def get_serializer_context(self):
        return {'request': self.request, 'place_id': self.kwargs['place_pk']}

    def destroy(self, request, *args, **kwargs):
        if Address.objects.filter(place_id=kwargs['pk']).count() > 0:
            return Response({
                'error': 'Address associated with place cannot be deleted'
            })
        return super().destroy(request, *args, **kwargs)


class VisitorViewSet(ModelViewSet):
    serializer_class = VisitorSerializer

    def get_queryset(self):
        return Visitor.objects.filter(place_id=self.kwargs['place_pk'])

    def get_serializer_context(self):
        return {'request': self.request, 'place_id': self.kwargs['place_pk']}
