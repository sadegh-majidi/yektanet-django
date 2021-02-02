from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from ..models import Ad


class AdSerializer(ModelSerializer):
    advertiser = serializers.ReadOnlyField(source='advertiser.username')

    def validate_link(self, value):
        if not value.startswith('http'):
            raise ValidationError('Links should start with http')
        return value

    class Meta:
        model = Ad
        fields = ['title', 'image', 'link', 'advertiser']
