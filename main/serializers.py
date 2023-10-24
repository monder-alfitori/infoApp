from rest_framework import serializers
from .models import Info, Tag, Party


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class InformationSerializer(serializers.ModelSerializer):
    party = PartySerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Info
        fields = '__all__'