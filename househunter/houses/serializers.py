from rest_framework import serializers
from houses.models import House

class HouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = House
        fields = ['zillow_id', 'address', 'city', 'state', 'zipcode']
