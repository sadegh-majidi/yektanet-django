from rest_framework.serializers import ModelSerializer
from ..models import Click


class ClickSerializer(ModelSerializer):

    class Meta:
        model = Click
        fields = ['time', 'user_ip', 'ad']
