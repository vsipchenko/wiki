from rest_framework import serializers

from .models import Version


class PageVersionSerializer(serializers.ModelSerializer):
    """
    Page version serializer.
    """

    class Meta:
        model = Version
        fields = ('page_id', 'id', 'title', 'text', 'is_active')
        read_only_fields = ('id', 'page_id', 'is_active')


class PageVersionActivateInput(serializers.Serializer):
    """
    Schema for input validation used by PageVersionActivateView.
    """
    version_id = serializers.IntegerField(min_value=1)
