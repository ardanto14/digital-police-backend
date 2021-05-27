from rest_framework.serializers import ModelSerializer
from .models import History, City

class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
        depth = 2


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"