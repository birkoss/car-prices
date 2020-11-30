from rest_framework import serializers

from cars.api.serializers import TrimModelSerializer

from ..models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['data', 'hash']


class PriceTrimSerializer(serializers.ModelSerializer):
    trim = TrimModelSerializer(read_only=True)

    class Meta:
        model = Price
        fields = ['data', 'hash', 'trim']
