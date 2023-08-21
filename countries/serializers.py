from rest_framework import serializers
from .models import Place, Address, Visitor


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
