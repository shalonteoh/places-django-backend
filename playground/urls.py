from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('home/', views.home),
    # path('place/', views.createPlace),
    # path('place/', views.updatePlace),
    # path('place/', views.deletePlace),
]
