from rest_framework.serializers import ModelSerializer
from ..models import View


class ViewSerializer(ModelSerializer):

    class Meta:
        model = View
        fields = ['time', 'user_ip', 'ad']
