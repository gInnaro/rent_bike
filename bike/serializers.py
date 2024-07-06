from rest_framework import serializers
from .models import Bicycle

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ('id', 'name', 'status')