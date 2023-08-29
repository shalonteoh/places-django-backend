from decimal import Decimal
from django.contrib import admin
from django.core.validators import DecimalValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from uuid import uuid4

# Create your models here.


class Place(models.Model):
    PLACE_STATUS = [
        ('A', 'Active'),
        ('I', 'Inactive'),
    ]
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[DecimalValidator(9, 6)],
        blank=True
    )
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        blank=True
    )
    status = models.CharField(max_length=1, choices=PLACE_STATUS, default='A')
    transit = models.ManyToManyField('Transit')
    created_at = models.DateTimeField(auto_now_add=True)
    status_change_at = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    # Search engine optimization
    slug = models.SlugField(blank=True)

    # Show place name instead of default name on admin site
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Transit(models.Model):
    TRANSIT_MODES = [
        ('C', 'Car'),
        ('CB', 'Commercial Bus'),
        ('PB', 'Public Bus'),
        ('IT', 'Intercity Train'),
        ('CT', 'City Train'),
        ('F', 'Flight'),
        ('W', 'Walk'),
    ]
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    mode = models.CharField(max_length=2, choices=TRANSIT_MODES, default='W')


class Member(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Visitor(models.Model):
    VISIT_TYPES = [
        ('L', 'Local'),
        ('H', 'Holiday'),
        ('B', 'Business'),
        ('E', 'Expert'),
    ]
    user = models.ForeignKey(Member,
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    review = models.TextField()
    visit_type = models.CharField(
        max_length=1, choices=VISIT_TYPES, default='H')
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='visitor_set')
    created_at = models.DateTimeField(auto_now_add=True)


class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    # Show country name instead of default name on admin site
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "countries"


class State(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    # Show state name instead of default name on admin site
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

# One address for each place


class Address(models.Model):
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    state = models.ForeignKey(
        State, on_delete=models.PROTECT, related_name='state_set', null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True)
    place = models.OneToOneField(
        Place, on_delete=models.CASCADE, primary_key=True, related_name='address_set')

    def __str__(self) -> str:
        return self.street

    class Meta:
        ordering = ['street']
        verbose_name_plural = "addresses"


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Member,
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL)

    class Meta:
        permissions = [
            ('duplicate_trip', 'Can duplicate trip')
        ]


class TripPlace(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='trip_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    duration = models.DecimalField(
        null=True,
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.1'))])
    created_at = models.DateTimeField(auto_now_add=True)

    # Only allow one place in each trip
    class Meta:
        unique_together = [['trip', 'place', 'date']]
