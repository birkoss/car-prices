from rest_framework import serializers

from cars.api.serializers import TrimSerializer

from ..models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['data', 'hash', 'msrp', 'taxes', 'delivery']


class PriceTrimSerializer(serializers.ModelSerializer):
    trim = TrimSerializer(read_only=True)

    class Meta:
        model = Price
        fields = ['data', 'hash', 'trim']
