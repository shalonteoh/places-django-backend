from itertools import count
from rest_framework import serializers
from .models import Member, Place, Address, TripPlace, Visitor, Trip


class AddressSerializer(serializers.ModelSerializer):
    state_id = serializers.IntegerField(required=False)
    state = serializers.StringRelatedField()
    country_id = serializers.IntegerField(required=False)
    country = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = [
            'street',
            'city',
            'postcode',
            'state',
            'state_id',
            'country',
            'country_id',
        ]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PlaceSerializer(serializers.ModelSerializer):
    # Like defining field in model. Not all field in model return in API
    # DOC: django-rest-framework.org/api-guide/fields
    address = AddressSerializer(
        source='address_set',
        read_only=True
    )
    place_link = serializers.HyperlinkedIdentityField(
        view_name='place-detail',
        read_only=True
    )

    # visitors = serializers.HyperlinkedRelatedField(
    #     view_name='place-visitors-list',
    #     source='visitor_set',
    #     lookup_field='place',
    #     lookup_url_kwarg='place_pk',
    #     read_only=True
    # )

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'description',
            'lat',
            'lon',
            'rating',
            'slug',
            'place_link',
            'address',
            # 'visitors',
        ]

    # Override create method
    def create(self, validated_data):
        place = Place(**validated_data)  # Unpack validated data
        place.status = 'A'
        place.save()
        return place

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class VisitorSerializer(serializers.ModelSerializer):

    place = serializers.HyperlinkedRelatedField(
        view_name='place-detail',
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Visitor
        fields = [
            'id',
            'place',
            'created_at',
            'review',
            'rating',
            'visit_type',
        ]

    def create(self, validated_data):
        place_id = self.context['place_id']
        return Visitor.objects.create(place_id=place_id, **validated_data)


class TripPlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'description',
            'lat',
            'lon',
        ]


class TripPlaceSerializer(serializers.ModelSerializer):
    place = TripPlaceDetailSerializer()

    class Meta:
        model = TripPlace
        fields = [
            'id',
            'place',
            'date',
            'duration',
            'created_at'
        ]


class CreateOrUpdateTripPlaceSerializer(serializers.ModelSerializer):
    place_id = serializers.IntegerField()

    class Meta:
        model = TripPlace
        fields = [
            'id',
            'place_id',
            'duration',
            'date'
        ]

    def validate_place_id(self, value):
        if not Place.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No place with the given ID was found')
        return value

    def validate_date(self, value):
        if TripPlace.objects.filter(
            place_id=self.instance.place_id,
            date=value
        ).exists():
            raise serializers.ValidationError(
                'Place already added in the date, no change performed'
            )

        return value

    def save(self, **kwargs):
        trip_place_id = self.instance.id
        trip_id = self.context['trip_id']
        place_id = self.validated_data['place_id']
        duration = self.validated_data['duration']
        date = self.validated_data['date']

        # PATCH
        if trip_place_id is not None:
            trip_place = TripPlace.objects.get(pk=trip_place_id)
            trip_place.duration = duration
            trip_place.date = date
            trip_place.save()
            self.instance = trip_place
        else:
            try:
                trip_place = TripPlace.objects.get(trip_id=trip_id,
                                                   place_id=place_id,
                                                   date=date)
                # PATCH
                trip_place.duration = duration
                trip_place.save()
                self.instance = trip_place
            except TripPlace.DoesNotExist:
                # POST
                self.instance = TripPlace.objects.create(
                    trip_id=trip_id, **self.validated_data)

        return self.instance


class TripSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    places = TripPlaceSerializer(
        source='trip_places',
        many=True,
        read_only=True
    )
    total_places = serializers.IntegerField(
        source='trip_places.count',
        read_only=True
    )
    total_duration = serializers.SerializerMethodField(
        method_name='calculate_total_duration',
        read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            'id',
            'places',
            'total_places',
            'total_duration',
            'created_at'
        ]

    def calculate_total_duration(self, trip: Trip):
        return sum([place.duration for place in trip.trip_places.all()])


class MemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'id',
            'user_id',
            'birth_date',
            'joined_at'
        ]
