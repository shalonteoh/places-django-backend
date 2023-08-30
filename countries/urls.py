from pprint import pprint
from django.conf.urls import include
from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('places', views.PlaceViewSet, basename='place')
router.register('trips', views.TripViewSet, basename='trip')
router.register('members', views.MemberViewSet, basename='member')

places_router = routers.NestedDefaultRouter(router, 'places', lookup='place')
places_router.register('visitors', views.VisitorViewSet,
                       basename='place-visitors')
places_router.register(
    'addresses', views.AddressViewSet, basename='place-address')

trips_router = routers.NestedDefaultRouter(router, 'trips', lookup='trip')
trips_router.register('places', views.TripPlaceViewSet, basename='trip-places')

# URLConf
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(places_router.urls)),
    path(r'', include(trips_router.urls)),
]
