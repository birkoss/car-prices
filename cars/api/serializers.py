from rest_framework import serializers

from ..models import Make, Model, Trim


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['name', 'slug']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['name', 'year', 'slug', 'foreign_id']


class TrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ['name', 'nice_name', 'slug', 'foreign_id']
