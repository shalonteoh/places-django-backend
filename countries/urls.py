from pprint import pprint
from django.conf.urls import include
from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('places', views.PlaceViewSet, basename='place')

places_router = routers.NestedDefaultRouter(router, 'places', lookup='place')
places_router.register('visitors', views.VisitorViewSet,
                       basename='place-visitors')
places_router.register(
    'addresses', views.AddressViewSet, basename='place-address')

# URLConf
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(places_router.urls))
]
