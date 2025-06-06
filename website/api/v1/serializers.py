from rest_framework import serializers
from website.models import StatusDiscoverImage

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model= StatusDiscoverImage
        fields= "__all__"