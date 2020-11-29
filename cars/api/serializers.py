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


class ModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['name', 'year', 'foreign_id']


class TrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ['name', 'nice_name', 'slug', 'foreign_id']


class TrimModelSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)

    class Meta:
        model = Trim
        fields = ['name', 'nice_name', 'slug', 'foreign_id', 'model']


class TrimWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = ['name', 'nice_name', 'foreign_id']
