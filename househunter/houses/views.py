from rest_framework import viewsets
from houses.models import House
from houses import serializers

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
