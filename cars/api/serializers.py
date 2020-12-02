from rest_framework import serializers

from ..models import Make, Model, Trim


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name', 'slug']


class ModelSerializer(serializers.ModelSerializer):
    make = MakeSerializer(read_only=True)

    class Meta:
        model = Model
        fields = ['id', 'name', 'year', 'slug', 'foreign_id', 'make']


class ModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['name', 'year', 'foreign_id']


class TrimSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)

    class Meta:
        model = Trim
        fields = ['id', 'name', 'nice_name', 'slug', 'foreign_id', 'model']


class TrimWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ['name', 'nice_name', 'foreign_id']
