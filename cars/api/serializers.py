from rest_framework import serializers

from ..models import Make


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['name', 'slug']
