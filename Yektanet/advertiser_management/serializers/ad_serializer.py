from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from ..models import Ad


class AdSerializer(ModelSerializer):
    advertiser = serializers.ReadOnlyField(source='advertiser.username')

    def create(self, validated_data):
        if not validated_data['link'].startswith('http'):
            raise ValidationError('Links should start with http')
        return super().create(validated_data)

    class Meta:
        model = Ad
        fields = ['title', 'image', 'link', 'advertiser']
