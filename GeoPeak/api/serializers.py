from rest_framework import serializers
from .models import Peak

__all__ = ["PeakSerialiser"]

class PeakSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Peak
        fields = ("id", "name", "lat", "long", "altitude")